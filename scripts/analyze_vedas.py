"""Build source anchored Veda navigation; no outside content or inferred borrowing."""
from pathlib import Path
import json,re,bisect,collections
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'corpus'; OUT=ROOT/'analysis'
N=[];E=[];notes=[];bodies={}; sources={}
def doc(name):
 p=[json.loads(l) for l in (C/(name+'.jsonl')).read_text().splitlines()];off=[];s=''
 for x in p:off.append(len(s));s+=x['text']+'\f'
 return p,s,off
D={n:doc(n) for n in ['rigveda','the-sama-veda','atharvaveda','yajurveda','four-vedas-english-translation','the-4-vedas-in-1']}
def page(name,offset):return bisect.bisect_right(D[name][2],offset)
def clean(s):return re.sub(r'\s+',' ',s).strip()
def tags(title):
 pats={'Agni':r'\bagni\b|fire','Indra':r'\bindr[ai]\b','Soma':r'\bsoma\b|pavamana|\bindu\b','Varuna':r'varuna','Vishnu':r'vis[h]?nu','Rudra':r'rudra|qarva|bhava','Brahman':r'brahman|brahma','Self':r'\batma|self','Creation':r'creation|cosmogon|embryo|hiranyagarbha|prajapati','Sacrifice':r'sacrific|offering|oblation|yajna','Waters':r'water|rain|river','Healing':r'heal|disease|poison|fever|remedy|remedies|herb|plants','Death':r'death|funeral|yama\b','Speech':r'speech|\bvak\b|sarasvati|learning|wisdom','Yoga':r'yoga|meditat','Dharma':r'dharma|law','Kingship':r'king|sovereign|authority','Concord':r'concord|harmony|unanimity','Marriage':r'marriage|wedding|wife|husband|love'}
 return [k for k,v in pats.items() if re.search(v,title,re.I)]
def node(id,title,type,parent,d,p,end=None,summary='',quote='',aliases=None,tg=None,method='heading-extraction',**kw):
 n={'id':id,'title':title,'type':type,'parent':parent,'doc':d,'page':p,'endPage':end or p,'summary':summary,'aliases':aliases or [],'tags':tg if tg is not None else tags(title),'evidence':[{'doc':d,'page':p,'quote':quote or title}],'indexMethod':method,**kw};N.append(n);return n
def extract_atharva_headings():
 p=[json.loads(l) for l in (C/'atharvaveda.jsonl').read_text().splitlines()]
 starts={1:171,2:207,3:254,4:312,5:390,6:451,7:558,8:641};counts={1:35,2:36,3:31,4:40,5:31,6:142,7:118};allout=[]
 for b in range(1,8):
  cs=collections.defaultdict(list); pos=0
  for x in p[starts[b]-1:starts[b+1]-1]:
   lines=x['text'].splitlines()
   for i,l in enumerate(lines):
    pos+=1
    m=re.match(r'^\s*([0-9IlioO ]{1,6})(?:\s*\([^)]*\))?\s*\.?\s{2,}([A-Z][^\n]+)',l)
    if not m:continue
    num=m[1].replace('I','1').replace('l','1').replace('i','1').replace('o','0').replace('O','0').replace(' ','')

    if not num:continue
    n=int(num); title=m[2].strip()
    if n<1 or n>counts[b]:continue
    nxt=' '.join(s.strip() for s in lines[i+1:i+6] if s.strip())
    score=0
    if re.match(r'^[\[\\|]',nxt):score+=7
    if title.endswith('.'):score+=3
    if len(title)<85:score+=2
    if len(l)-len(l.lstrip())>15:score+=1
    if re.match(r'^(For|To|Against|Praise|Prayer|A |The (?:power|Brahman|heavenly)|With|Mystic|Accompany|Extolling|Cosmogonic|Of |In |When|Homage|Invocation|Exorcism|Deterrent|Imprecation|At |Greeting|Morning|Husband|Concerning|Deprecation)',title):score+=4
    cs[n].append({'b':b,'n':n,'p':x['page'],'i':pos,'title':title,'score':score})
  # select highest plausibility constrained to an interval between robust neighboring headings
  out=[]
  for n in range(1,counts[b]+1):
   cc=cs[n]
   prev=[x for k in range(max(1,n-2),n) for x in cs[k] if x['score']>=13]
   nex=[x for k in range(n+1,min(counts[b],n+2)+1) for x in cs[k] if x['score']>=13]
   low=max([x['i'] for x in prev] or [-1]);hi=min([x['i'] for x in nex] or [10**9])
   c=[x for x in cc if low<x['i']<hi]
   if not c:c=cc
   if not c:continue
   sel=max(c,key=lambda x:x['score']);out.append(sel)
  allout+=out
 return allout
# Four works. Edition identity comes from supplied front matter.
node('v-rigveda','Rigveda','text','family-vedas','rigveda',1,750,'Ten books of hymns in the supplied English translation. All 1,028 observed HYMN headings are indexed; hymn names and occasional misspellings follow this file. A metrical glossary follows the hymns.','RIG VEDA - THE FIRST BOOK',aliases=['Rig Veda','Rg Veda'],method='curated')
node('v-samaveda','Samaveda','text','family-vedas','four-vedas-english-translation',1176,1311,'Songs arranged for ritual chanting. The supplied Griffith preface describes verses drawn mainly from the Rigveda and rearranged for ritual. The 460 song groups below use the explicit hierarchy in the indexed draft compilation; a separate Stevenson translation is also supplied.','HYMNS OF THE SAMAVEDA',aliases=['Sama Veda','Sama-Veda'],tg=['Soma','Agni','Indra','Sacrifice'],method='curated')
node('v-yajurveda','Yajurveda','text','family-vedas','yajurveda',1,1096,'Two distinct supplied presentations: the 40-chapter Tulsi Ram translation, and Keith’s numbered Taittiriya passages in the Four Vedas compilation. Their section numbering and interpretive traditions are preserved separately.','YAJURVEDA',aliases=['Yajur Veda'],tg=['Sacrifice','Agni','Rudra'],method='curated')
node('v-atharvaveda','Atharvaveda','text','family-vedas','atharvaveda',11,640,'Whitney/Lanman volume I supplies books I–VII with critical commentary, 433 hymns under its Berlin numbering. Bloomfield’s supplied anthology adds selections from later books and explicitly says it covers about one third of the entire material.','Introduction.               Books I to VII',aliases=['Atharva Veda','Atharva-Veda'],tg=['Healing','Waters','Kingship','Speech'],method='curated')
# Rig: every real HYMN heading. Number sequentially within each actual book, avoiding OCR Roman numeral errors.
p,s,off=D['rigveda'];heads=[];bookheads=list(re.finditer(r'^\s*RIG VEDA - THE ([A-Z]+) BOOK',s,re.M));prev=0
for b,mb in enumerate(bookheads,1):
 end=bookheads[b].start() if b<len(bookheads) else len(s)
 bh=list(re.finditer(r'^\s*HYMN\b[^\n]*',s[mb.end():end],re.M))
 node(f'rv-b{b}',f'Rigveda · Book {b}','section','v-rigveda','rigveda',page('rigveda',mb.start()+len(mb[0])-len(mb[0].lstrip())),page('rigveda',end-1),f'{len(bh)} observed hymn headings in this book.',clean(mb[0]))
 for h,mm in enumerate(bh,1):
  st=mb.end()+mm.start()+len(mm[0])-len(mm[0].lstrip());en=mb.end()+bh[h].start()+len(bh[h][0])-len(bh[h][0].lstrip()) if h<len(bh) else end
  heading=clean(mm[0]);title=re.sub(r'^HYMN\s+[IVXLCMD]+[\s.,]*','',heading).strip(' .')
  if not title:title=heading
  id=f'rv-{b}-{h}';n=node(id,f'RV {b}.{h} · {title}','hymn',f'rv-b{b}','rigveda',page('rigveda',st),page('rigveda',en-1),f'Hymn heading: {title}. Read the cited passage for the complete hymn.',heading,aliases=[f'Rigveda {b}.{h}',f'Rig Veda {b}.{h}'])
  bodies[id]=s[st:en];sources[id]=('rigveda',st)
# Curated guides to key hymns; these summaries are based on the actual source text.
curated={
(1,32):('Indra and Vritra','Indra defeats the dragon and releases the waters; the hymn repeatedly narrates his striking with the thunderbolt.',['Indra','Waters','Vritra','Creation']),
(1,164):('Riddle hymn and many names','A sequence of cosmological riddles, bird and wheel imagery, and the statement that sages call the One by many names.',['Creation','Speech','Brahman','Riddle']),
(1,179):('Lopamudra and Agastya','Dialogue voices negotiate desire, age, ascetic effort, and married life.',['Lopamudra','Agastya','Marriage','Dialogue']),
(3,33):('Vishvamitra and the rivers','The poet addresses the rivers Vipash and Shutudri, asking for passage; the rivers answer.',['Waters','Vishvamitra','Dialogue']),
(3,62):('Savitar and the Gayatri verse','Hymn to several deities; verse 10 asks for meditation on Savitar’s excellent glory and the stimulation of thought.',['Savitar','Gayatri','Speech','Meditation']),
(7,18):('Vasishtha, Sudas and the battle','Indra is praised for aid to Sudas amid river crossings and conflict; the names of opposing groups appear within the hymn.',['Indra','Sudas','Vasishtha','Kingship','Waters']),
(10,10):('Yama and Yami','A dialogue between Yama and Yami over the proposed union of the twins, setting desire beside limits and duty.',['Yama','Yami','Dialogue','Dharma','Marriage']),
(10,14):('Yama and the ancestors','A funeral hymn invoking Yama, the Fathers, and the path to those who have gone before.',['Yama','Ancestors','Death']),
(10,18):('Funeral and return to life','Funeral verses address death and the living, including the earth as shelter and the widow’s return to the living.',['Death','Earth','Ancestors']),
(10,34):('The gambler’s lament','A gambler describes the compelling dice, family estrangement and debt, and is advised to turn to agriculture.',['Dice','Gambling','Ethics','Agriculture']),
(10,85):('Surya’s wedding','The wedding of Surya frames marriage verses, the journey of the bride, and blessings for a shared household.',['Surya','Marriage','Ashvins']),
(10,90):('Purusha hymn','The cosmic Person is described through a primordial sacrifice whose divisions are related to the cosmos and social orders.',['Purusha','Creation','Sacrifice']),
(10,95):('Pururavas and Urvashi','Dialogue of the separated Pururavas and Urvashi, with recollection, appeal, and separation.',['Pururavas','Urvashi','Dialogue','Marriage']),
(10,108):('Sarama and the Panis','Sarama, sent by Indra, confronts the Panis over hidden cattle; the exchange turns on kinship, wealth, and the cattle’s recovery.',['Sarama','Panis','Indra','Cattle','Dialogue']),
(10,121):('Hiranyagarbha, the golden germ','A cosmological hymn asking which deity should receive the offering, beginning with the golden germ and ending with Prajapati.',['Creation','Hiranyagarbha','Prajapati','Sacrifice']),
(10,125):('Vak, the speaking power','The first-person divine speaker declares her activity among gods and beings, her sovereignty, and her pervasiveness.',['Speech','Vak','Devi']),
(10,129):('Nasadiya, the creation question','The hymn asks about existence and nonexistence before creation and ends by questioning who knows its origin.',['Creation','Nasadiya','Inquiry']),
(10,191):('Concord and shared purpose','The closing hymn calls for assembly, common speech, shared intention, and united hearts.',['Concord','Speech','Dharma'])}
for (b,h),(label,summary,tg) in curated.items():
 n=next(n for n in N if n['id']==f'rv-{b}-{h}');n['title']=f'RV {b}.{h} · {label}';n['aliases']+=[label];n['summary']=summary;n['tags']=tg;n['indexMethod']='curated';excerpt=next((clean(line) for line in bodies[n['id']].splitlines()[1:] if clean(line)),None)
 if excerpt:n['evidence'].append({'doc':'rigveda','page':page('rigveda',sources[n['id']][1]+bodies[n['id']].index(excerpt)) if excerpt in bodies[n['id']] else n['page'],'quote':excerpt})
# Sama: 460 actual groups, not draft placeholders or the table of contents.
d='the-4-vedas-in-1';p,s,off=D[d];sm=[]
for x in p[856:945]:
 for m in re.finditer(r'^\s*(3(?:\.\d+){1,4})\s*(\D[^\n]*)',x['text'],re.M):sm.append((m[1],clean(m[2]),off[x['page']-1]+m.start(),x['page']))
for i,(ref,title,st,pg) in enumerate(sm):
 en=sm[i+1][2] if i+1<len(sm) else off[945]
 id='sv-'+ref.replace('.','-');parent='v-samaveda' if ref.count('.')==1 else 'sv-'+ref.rsplit('.',1)[0].replace('.','-');typ='song' if ref.count('.')==4 else 'section'
 label=f'SV {ref[2:]} · {title}'
 n=node(id,label,typ,parent,d,pg,page(d,en-1),'A song group from the supplied indexed compilation. Its numbering is an editorial navigation scheme; the source is a draft.' if typ=='song' else 'Structural division as labelled in the supplied indexed compilation.',f'{ref} {title}')
 if typ=='song':bodies[id]=s[st:en];sources[id]=(d,st)
# Yajur Tulsi Ram chapter starts, observed special chapter title marker.
d='yajurveda';p,s,off=D[d];chs=[]
for x in p[34:]:
 if re.search(r'CHAPTERñ[IVX]+',x['text']):chs.append(x['page'])
for i,pg in enumerate(chs,1):
 ep=chs[i]-1 if i<len(chs) else len(p)
 node(f'yv-tr-{i}',f'Yajurveda · Chapter {i} (Tulsi Ram)','chapter','v-yajurveda',d,pg,ep,'Chapter in the supplied Tulsi Ram translation with Sanskrit text, transliteration and English interpretation. Verse-level navigation remains available in the source pages.',clean(re.search(r'CHAPTERñ[IVX]+',p[pg-1]['text'])[0]),tg=['Sacrifice'] if i<40 else ['Self','Brahman','Dharma'],method='heading-extraction')
# Keith numbered passages. Preserve observed source labels, document obvious source numbering anomalies.
d='four-vedas-english-translation';p,s,off=D[d];kh=[]
for x in p[617:1175]:
 for m in re.finditer(r'^\s*([ivx1]+)\.\s*([\diIl]+)\.\s*(\d+)\.?([^\n]*)',x['text'],re.M|re.I):
  # Reject prose alphabetic lines by requiring an actual three-level reference.
  r=m[1].lower().replace('1','i');a=m[2].replace('i','1').replace('I','1').replace('l','1');z=m[3]
  if r not in ['i','ii','iii','iv','v','vi','vii']:continue
  kh.append((r,int(a),int(z),off[x['page']-1]+m.start(),x['page'],clean(m[0])))
roman={'i':1,'ii':2,'iii':3,'iv':4,'v':5,'vi':6,'vii':7};seen=set()
for i,(r,a,z,st,pg,raw) in enumerate(kh):
 b=roman[r];bid=f'yv-keith-b{b}';pid=f'yv-keith-{b}-{a}';id=f'yv-keith-{b}-{a}-{z}'
 if id in seen:id+=f'-p{pg}'
 if bid not in seen:node(bid,f'Yajurveda · Keith · Kanda {b}','section','v-yajurveda',d,pg,pg,'Kanda of the supplied Keith translation; passage labels are retained as printed.',raw,tg=['Sacrifice']);seen.add(bid)
 if pid not in seen:node(pid,f'Keith {b}.{a} · Prapathaka','section',bid,d,pg,pg,'Prapathaka identified from passage labels in the supplied Keith translation.',raw,tg=['Sacrifice']);seen.add(pid)
 en=kh[i+1][3] if i+1<len(kh) else off[1175]
 body=s[st:en];opening=clean(re.sub(r'^\s*'+re.escape(raw),'',body))[:180]
 node(id,f'Keith {b}.{a}.{z} · Ritual passage','passage',pid,d,pg,page(d,en-1),'Numbered passage in the supplied Keith translation. Source numbering may contain transcription errors; the PDF reference is authoritative for locating this entry.',raw,tg=tags(body[:900]) or ['Sacrifice'])
 seen.add(id);bodies[id]=body;sources[id]=(d,st)
# Whitney headings with manual recovery for ten OCR-obscured headings. 433 Berlin-numbered hymns.
avheads=extract_atharva_headings()
fix=[(1,24,194,'Against leprosy.'),(5,6,400,'Disconnected verses.'),(7,33,580,'For blessings: to various gods.'),(7,34,580,'To Agni: against enemies.'),(7,44,586,'Extolling Indra and Vishnu.'),(7,53,593,"For some one’s health and long life."),(7,54,594,'Extolling verse and chant.'),(7,73,607,'With a heated offering to the Ashvins.'),(7,75,610,'Praise and prayer to the kine.'),(7,90,624,"To destroy some one’s virile power."),(7,109,634,'For success with the dice.')]
for b,n,pg,t in fix:
 avheads=[x for x in avheads if not(x['b']==b and x['n']==n)];avheads.append({'b':b,'n':n,'p':pg,'title':t,'manual':True})
avheads.sort(key=lambda x:(x['b'],x['n']));starts={1:171,2:207,3:254,4:312,5:390,6:451,7:558,8:641};d='atharvaveda'
for b in range(1,8):node(f'av-b{b}',f'Atharvaveda · Book {b} (Whitney)','section','v-atharvaveda',d,starts[b],starts[b+1]-1,'Hymns under the Berlin numbering in Whitney/Lanman volume I. In book VII the parenthesized Bombay numbering differs; it is not silently equated with anthology numbering.',f'Book {b}',tg=['Healing','Sacrifice'])
for i,x in enumerate(avheads):
 b,n,pg,t=x['b'],x['n'],x['p'],clean(x['title']);en=avheads[i+1]['p'] if i+1<len(avheads) else 640
 node(f'av-{b}-{n}',f'AV {b}.{n} · {t}','hymn',f'av-b{b}',d,pg,max(pg,en),'Hymn heading in the supplied Whitney translation, with separate critical and ritual commentary on the same pages. Berlin numbering is preserved.',t,aliases=[f'Atharvaveda {b}.{n}',f'Whitney {b}.{n}'],method='heading-extraction; OCR heading manually recovered' if x.get('manual') else 'heading-extraction')
# Bloomfield anthology: later-book selections retain anthology references; shared1–7 are edition variants, not new canonical hymns.
d='four-vedas-english-translation';p,s,off=D[d];anth=[]
for x in p[1314:]:
 for m in re.finditer(r'^\s*([IVX]+),\s*(\d+)\.\s*([^\n]+)',x['text'],re.M):
  rr=m[1];v=0;last=0
  for c in rr[::-1]:
   w={'I':1,'V':5,'X':10}[c];v+= -w if w<last else w;last=max(last,w)
  anth.append((v,int(m[2]),clean(m[3]),off[x['page']-1]+m.start(),x['page']))
for i,(b,h,t,st,pg) in enumerate(anth):
 en=anth[i+1][3] if i+1<len(anth) else len(s)
 if b<=7:
  # This is an edition-level variant reference; book7 numbering is explicitly different and not equated.
  continue
 bid=f'av-bloomfield-b{b}'
 if bid not in {n['id'] for n in N}:node(bid,f'Atharvaveda · Book {b} selections (Bloomfield)','section','v-atharvaveda',d,pg,page(d,en-1),'Selected hymns only; the anthology does not supply the complete book.',f'{b}, {h}. {t}',tg=['Healing'])
 node(f'av-bloomfield-{b}-{h}',f'AV {b}.{h} · {t} (Bloomfield)','hymn',bid,d,pg,page(d,en-1),'A selection in the supplied Bloomfield anthology, not a claim of complete book coverage.',f'{b}, {h}. {t}')
# Actual matching wording: each edge has the two exact source snippets, with page locations.
# This measures English verbal overlap, never a proof of Sanskrit identity or historical borrowing.
ng=collections.defaultdict(list)
for id,body in list(bodies.items()):
 if not id.startswith('rv-'):continue
 toks=list(re.finditer(r'[A-Za-z]+',body));startsrc=sources[id][1]
 for i in range(len(toks)-11):
  words=tuple(t.group().lower() for t in toks[i:i+12]);ng[words].append((id,toks[i].start(),toks[i+11].end()))
found=0
for id,body in list(bodies.items()):
 if not id.startswith('sv-'):continue
 toks=list(re.finditer(r'[A-Za-z]+',body));pairs={}
 for i in range(max(0,len(toks)-11)):
  words=tuple(t.group().lower() for t in toks[i:i+12]);hits=ng.get(words,[])
  ids=set(h[0] for h in hits)
  if len(ids)!=1:continue
  rid,a,z=hits[0]
  if rid in pairs:continue
  sd,so=sources[id];rd,ro=sources[rid]
  if page(sd,so+toks[i].start())!=page(sd,so+toks[i+11].end()-1) or page(rd,ro+a)!=page(rd,ro+z-1):continue
  evidence=[{'doc':sd,'page':page(sd,so+toks[i].start()),'quote':clean(body[toks[i].start():toks[i+11].end()])},{'doc':rd,'page':page(rd,ro+a),'quote':clean(bodies[rid][a:z])}]
  pairs[rid]={'source':id,'target':rid,'type':'shared wording','summary':'At least 12 consecutive normalized English words match in the supplied translations. This is a reading connection, not a claim of complete hymn identity or historical borrowing.','evidence':evidence,'indexMethod':'exact-phrase-matching'}
 for e in list(pairs.values())[:2]:E.append(e);found+=1
# Explicit family connection based on supplied preface.
E.append({'source':'v-samaveda','target':'v-rigveda','type':'source-described reuse','summary':'Griffith’s supplied preface says the Samaveda collection takes hymns, portions, and detached verses mainly from the Rigveda and rearranges them for ritual.','evidence':[{'doc':'four-vedas-english-translation','page':1177,'quote':'taken mainly from the Rgveda, transposed and re-arranged'}]})
# Actual thematic bridges among curated hymns; avoid pretending direct influence.
for src,tgt,reason in [('rv-1-32','rv-10-121','Both are concerned with cosmic ordering, through different poetic accounts.'),('rv-10-90','rv-10-121','Two distinct cosmogonic accounts: cosmic Person/sacrifice and golden germ.'),('rv-10-121','rv-10-129','Read two different poetic approaches to the origin of the world: offering and inquiry.'),('rv-1-164','rv-10-125','Both treat divine speech and the relation of multiplicity to a wider unity.'),('rv-10-34','av-7-109','Contrasting dice themes: the gambler’s lament versus a hymn for success with dice.'),('rv-10-191','av-3-30','Shared theme of concord and common purpose.'),('rv-10-85','rv-1-179','Marriage in a ceremonial hymn and in a dialogue over household and desire.'),('rv-10-95','rv-10-10','Two dialogues in which desire encounters limits; their figures and outcomes remain distinct.')]:
 a=next(n for n in N if n['id']==src);z=next(n for n in N if n['id']==tgt);E.append({'source':src,'target':tgt,'type':'thematic comparison','summary':reason,'evidence':a['evidence'][:1]+z['evidence'][:1],'indexMethod':'curated'})
notes=[
 'Scope is the supplied PDFs, not all recensions, manuscripts, Brahmanas, Aranyakas, Sutras, or all Hindu literature.',
 'Rigveda: all 1,028 observed HYMN headings indexed in 10 books. Machine numbering follows heading order within each book because several Roman numerals are mistyped.',
 'Samaveda: 460 actual song groups from the draft compilation body, plus 51 structural nodes. The source’s inconsistent mantra totals are not treated as established counts. Stevenson’s separate OCR translation remains available through source pages.',
 'Yajurveda: 40 Tulsi Ram chapters indexed. Keith numbered passage headings indexed separately without assuming a one-to-one match to the 40-chapter edition. Some source references are malformed (e.g. iii.6.8 between iii.5.7 and iii.5.9; iv.8.4 between iv.3.3 and iv.3.5; vii.6.16 between vii.5.15 and vii.5.17); labels are retained with source pages.',
 'Atharvaveda: Whitney/Lanman volume I supplies Books I–VII only. Its Berlin numbering has 35,36,31,40,31,142,118 hymns respectively, totaling 433. Book VII includes different parenthesized Bombay numbering; no automatic equivalence is asserted.',
 'Bloomfield anthology introduction (Four Vedas p1313) explicitly calls itself about one third of the entire material. Later-book selections are indexed; this does not make later books complete.',
 'the-4-vedas-in-1 is Issue 1, Draft 2 and has many literal “Sukta text here” placeholders in the Atharva portion. These placeholders are excluded as hymn content. Its editorial merger of recensions and speculative totals are not endorsed.',
 f'{found} Sama–Rig reading links were generated from exact 12-word English matches, with evidence on both sides. These links show translation wording overlap, not a verified philological stemma or complete identity.',
 'The first ten Rigveda key-summary examples and other curated summaries are editorial reading aids grounded in their cited passages. Other heading-only summaries do not claim a full interpretive analysis of each hymn.'
]
# Keep every displayed evidence quotation verbatim (whitespace-normalized) even when titles correct OCR.
for n in N:
 for ev in n['evidence']:
  tx=D[ev['doc']][0][ev['page']-1]['text']
  if clean(ev['quote']) in clean(tx):continue
  if n['id'].startswith('av-b') and ev['doc']=='atharvaveda':
   mm=re.search(r'Book\s+[IVX]+\.',tx)
   if mm:ev['quote']=clean(mm[0])
  elif n['id'].startswith('av-bloomfield'):
   bits=n['id'].split('-');number=bits[-1] if not bits[-1].startswith('b') else None
   if number:
    mm=re.search(r'^\s*[IVX]+,\s*'+number+r'\.\s*[^\n]+',tx,re.M)
   else:
    mm=re.search(r'^\s*[IVX]+,\s*\d+\.\s*[^\n]+',tx,re.M)
   if mm:ev['quote']=clean(mm[0])
  elif n['id'].startswith('av-') and ev['doc']=='atharvaveda':
   number=n['id'].split('-')[-1]
   mm=re.search(r'^\s*'+number+r'\s*\([^\n]+',tx,re.M)
   if mm:ev['quote']=clean(mm[0])
OUT.mkdir(exist_ok=True);(OUT/'vedas.json').write_text(json.dumps({'nodes':N,'edges':E,'notes':notes},ensure_ascii=False,indent=2))
(OUT/'vedas-notes.md').write_text('# Supplied Veda corpus: navigation and limitations\n\n'+'\n\n'.join('- '+x for x in notes)+'\n\n## Counts\n\n'+str(dict(collections.Counter(n['type'] for n in N)))+'\n')
print(json.dumps({'nodes':len(N),'edges':len(E),'types':dict(collections.Counter(n['type'] for n in N)),'atharva':len(avheads),'keith':len(kh),'sama_matches':found},indent=2))
