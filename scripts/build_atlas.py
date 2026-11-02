from pathlib import Path
import json,re,collections,xml.etree.ElementTree as ET,unicodedata,datetime
R=Path(__file__).resolve().parents[1]; O=R/'output';O.mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text())
manifest=load(R/'corpus/manifest.json');docs={d['id']:d for d in manifest}
PAGES={d['id']:[json.loads(l)['text'] for l in (R/'corpus'/(d['id']+'.jsonl')).read_text().splitlines()] for d in manifest}
nodes=[{'id':'root','title':'Vedic literature · supplied collection','type':'root','summary':'An evidence-linked map of the supplied Veda, Upanishad, Purana, and practical-guide PDFs. Explore works, hymns, narratives, shared concepts, source editions, and every PDF page.','aliases':[],'tags':[]}]
families=[('vedas','Vedas','Four Vedic traditions','Hymns, ritual formulas, chants, and selected translations. The files have different scopes and sometimes overlap.'),('upanishads','Upanishads','108 Upanishads','The supplied Muktika-ordered collection, with the ten modern commentaries kept distinct from translations.'),('puranas','Puranas','18 named Puranas','Narrative, devotional, cosmological, ritual, and pilgrimage material. Many supplied files are retellings or partial volumes.'),('bonus','Bonus','Practical guides','The supplied Ayurveda, yoga, and Vastu guides, organized separately from the scriptural texts.'),('concepts','Concepts','Ideas & recurring figures','Navigation through shared names and themes. Textual mentions and editorial comparisons do not establish historical borrowing or identical doctrine.')]
for id,cat,title,s in families:nodes.append({'id':'family-'+id,'title':title,'type':'family','parent':'root','summary':s,'category':cat,'aliases':[],'tags':[]})
edges=[];notes=[]
for filename in ['vedas.json','upanishads.json','puranas.json','scanned-puranas.json','bonus.json']:
 f=R/'analysis'/filename
 if not f.exists():continue
 a=load(f);nodes+=a.get('nodes',[]);edges+=a.get('edges',[])
 for n in a.get('notes',[]):notes.append({'title':filename.split('.')[0].replace('-',' ').capitalize(),'text':n if isinstance(n,str) else n.get('text',str(n))})
# Last writer can enrich a work without duplicating its identity.
byid={}
for n in nodes:
 if n['id'] in byid:byid[n['id']].update(n)
 else:byid[n['id']]=n
nodes=list(byid.values())
for n in nodes:
 n.setdefault('aliases',[]);n.setdefault('tags',[]);n.setdefault('evidence',[])
 if n.get('parent')=='family-connections':n['parent']='family-concepts';n['type']='concept';n['category']='Concepts'
 if n.get('doc') in docs:n.setdefault('category',docs[n['doc']]['category'])
 if re.search('extract|heuristic|OCR',str(n.get('method',''))+' '+str(n.get('indexMethod','')),re.I):n['machine']=True
# A separate witness per source preserves overlaps and complete page coverage.
for d in manifest:
 works=[n for n in nodes if n.get('doc')==d['id'] and n.get('type') in ['text','guide','volume'] and (str(n.get('parent','')).startswith('family-') or n.get('type')=='volume')]
 volume=next((n for n in works if n.get('type')=='volume'),None)
 parent=volume['id'] if volume else works[0]['id'] if len(works)==1 else 'family-'+d['category'].lower()
 if d['id'] in ['four-vedas-english-translation','the-4-vedas-in-1']:parent='family-vedas'
 docid='doc-'+d['id']
 nodes.append({'id':docid,'title':d['title']+' · source PDF','type':'document','parent':parent,'doc':d['id'],'page':1,'endPage':d['pages'],'category':d['category'],'summary':f"Supplied source witness: {d['pages']} PDF pages. "+('Text recognized from a scan; recognition errors may remain.' if d.get('ocr') else 'Embedded text extracted with page boundaries retained.'),'aliases':[],'tags':[],'evidence':[]})
 for page,text in enumerate(PAGES[d['id']],1):
  first=next((line.strip() for line in text.splitlines() if len(line.strip())>=8 and not re.fullmatch(r'[\d\W]+',line.strip())), 'Source page')
  if len(first)>68:first=first[:65]+'…'
  nodes.append({'id':f"page-{d['id']}-{page}",'title':f'PDF p. {page} · {first}','type':'page','parent':docid,'doc':d['id'],'page':page,'category':d['category'],'summary':'A source-page navigation record. Read the extracted text or open the original page to verify the passage.','aliases':[],'tags':[],'evidence':[],'machine':True})
# Controlled cross-text index. Patterns establish mentions, not semantic equivalence.
CONCEPTS=[
('agni','Agni',['Fire'],r'\bAgni\b','Named deity and ritual fire; compare the role in each passage.'),
('indra','Indra',[],r'\bIndra\b','A recurring named deity; the narrative and theological role varies by text.'),
('soma','Soma',[],r'\bSoma\b','A recurring deity, offering, and sacred substance in the supplied translations.'),
('surya','Surya / Sun',['Surya','Sun'],r'\b(?:Surya|S[uū]rya)\b','Solar names and imagery; inspect each source for the particular figure or meaning.'),
('varuna','Varuna',[],r'\bVaru[nṇ]a\b','A recurring named deity.'),
('usha','Ushas / Dawn',['Ushas','Dawn'],r'\b(?:Ushas|U[sṣ]as)\b','Dawn hymns and related named imagery.'),
('rudra','Rudra',[],r'\bRudra\b','A recurring divine name; relationship with Shiva must be read in context.'),
('shiva','Shiva',['Siva','Shiv'],r'\b(?:Shiva|Siva|[ŚŚ]iva|Mahadeva)\b','Shiva-centered narratives, devotion, and teaching.'),
('vishnu','Vishnu',[],r'\bVi(?:sh|s|ṣ)[nṇ]u\b','Vishnu-centered narratives, devotion, and cosmology.'),
('brahma','Brahma',['Brahmā'],r'\bBrahm[aā]\b(?!n)','The creator figure; this name is kept distinct from Brahman.'),
('brahman','Brahman',[],r'\bBrahman\b','The term Brahman. Its occurrence alone does not resolve a passage’s philosophical interpretation.'),
('atman','Atman',['Atma','Self'],r'\b(?:Atman|[AĀ]tman|Atma|[AĀ]tma)\b','The self; compare each text’s own formulation.'),
('om','Om',['Aum','Pranava'],r'\b(?:Om|Aum|Pranava)\b','Sacred sound, invocation, and contemplative interpretation.'),
('creation','Creation',['Cosmology','Cosmogony'],r'\b(?:creation|cosmogony|cosmology)\b','Accounts and inquiries concerning origins; these are comparison points, not one uniform creation narrative.'),
('purusha','Purusha',['Purusa'],r'\bPuru(?:sh|s|ṣ)a\b','The term Purusha, with different uses across hymns and philosophical passages.'),
('prajapati','Prajapati',[],r'\bPraj[aā]pati\b','A recurring creator and lord-of-creatures figure.'),
('sacrifice','Sacrifice / Yajna',['Sacrifice','Yajna','Yajña','Ritual'],r'\b(?:sacrifice|yajna|yajña)\b','Ritual action, offerings, and their interpretations.'),
('dharma','Dharma',[],r'\bdharma\b','Duty, order, or teaching as formulated in a particular source.'),
('karma','Karma',['Karman'],r'\bkarm(?:a|an)\b','Action and its results in the supplied passages.'),
('moksha','Liberation / Moksha',['Moksha','Liberation','Kaivalya','Mukti'],r'\b(?:moksha|moksa|mukti|kaivalya|liberation)\b','Terms and paths of liberation; compare doctrinal differences.'),
('yoga','Yoga',[],r'\byoga\b','Yoga teachings and practices, including distinct modern guide material.'),
('meditation','Meditation / Dhyana',['Meditation','Dhyana'],r'\b(?:meditation|dhyana|dhy[aā]na)\b','Contemplative instructions and their stated aims.'),
('prana','Prana',['Breath','Pranayama'],r'\b(?:prana|pr[aā][nṇ]a|pranayama)\b','Vital breath and practices described in context.'),
('knowledge','Knowledge / Vidya',['Knowledge','Jnana','Vidya'],r'\b(?:knowledge|jnana|vidya)\b','Knowledge and learning; this broad theme does not imply a single school.'),
('renunciation','Renunciation',['Sannyasa','Sannyasin'],r'\b(?:renunciation|sannyasa|sannyasin)\b','Renunciant discipline and its interpretations.'),
('devotion','Devotion / Bhakti',['Devotion','Bhakti'],r'\b(?:devotion|bhakti)\b','Devotional narratives, praise, and practices.'),
('devi','Devi / Goddess',['Devi','Goddess','Shakti','Sakti'],r'\b(?:Devi|Dev[iī]|Shakti|[ŚS]akti|goddess)\b','Goddess names, narratives, and traditions; individual identities remain distinct.'),
('durga','Durga',[],r'\bDurg[aā]\b','The named goddess Durga.'),
('lakshmi','Lakshmi',['Laksmi'],r'\bLak(?:sh|s|ṣ)m[iī]\b','The named goddess Lakshmi.'),
('sarasvati','Sarasvati',['Saraswati'],r'\bSarasva(?:t|th)[iī]\b','River and goddess references, with context-dependent roles.'),
('parvati','Parvati',['Uma','Sati'],r'\b(?:Parvati|P[aā]rvat[iī]|Uma|Um[aā])\b','Parvati and Uma references; Sati narratives are separately identified in their texts.'),
('krishna','Krishna',['Krsna'],r'\b(?:Krishna|Krshna|Krsna|Kṛṣṇa)\b','Krishna narratives and teachings.'),
('rama','Rama',[],r'\bR[aā]ma\b','The name Rama; check the passage to distinguish Ramachandra, Parashurama, or another usage.'),
('ganesha','Ganesha',['Ganapati','Ganesa'],r'\b(?:Ganesha|Ganesa|Ganapati)\b','The named deity Ganesha / Ganapati.'),
('yama','Yama',[],r'\bYama\b','The named figure Yama; yoga’s ethical restraints may use the same spelling.'),
('nachiketa','Nachiketa',['Nachiketas','Naciketas'],r'\bNa(?:ch|c)iketa[s]?\b','The seeker associated with Yama; compare the Upanishadic dialogue and later retelling.'),
('yajnavalkya','Yajnavalkya',[],r'\bYajnavalkya\b','Dialogues and teachings associated with this named sage.'),
('maitreyi','Maitreyi',[],r'\bMaitreyi\b','The named interlocutor in teachings on self and immortality.'),
('gargi','Gargi',[],r'\bGargi\b','The named interlocutor in philosophical debate.'),
('svetaketu','Svetaketu',['Shvetaketu'],r'\b(?:Svetaketu|Shvetaketu)\b','The named pupil in teaching dialogues.'),
('uddalaka','Uddalaka',[],r'\bUddalaka\b','The named teacher in Upanishadic dialogue.'),
('narada','Narada',['Narad'],r'\bN[aā]rada?\b','A recurring sage and dialogue figure.'),
('dhruva','Dhruva',[],r'\bDhruva\b','Dhruva’s narrative and associated devotional motifs.'),
('prahlada','Prahlada',['Prahlad'],r'\bPrahl[aā]da?\b','Prahlada narratives and devotion.'),
('daksha','Daksha',['Daksa'],r'\bDak(?:sh|s|ṣ)a\b','Daksha narratives, including sacrifice traditions.'),
('manu','Manu',[],r'\bManu\b','Manu figures and narrative contexts; the name can refer to different Manus.'),
('matsya','Matsya / Fish',['Matsya','Fish incarnation','Flood'],r'\b(?:Matsya|flood|fish incarnation)\b','Fish and flood narratives; compare source-specific details.'),
('varaha','Varaha / Boar',['Varaha','Boar incarnation'],r'\bVar[aā]ha\b','The boar incarnation and associated narrative traditions.'),
('vamana','Vamana',['Vamana incarnation','Trivikrama'],r'\b(?:V[aā]mana|Trivikrama)\b','Vamana and three-stride motifs; shared themes do not alone establish direct derivation.'),
('narasimha','Narasimha',['Nrisimha'],r'\b(?:Narasimha|Nrisimha)\b','Man-lion narratives and worship.'),
('parashurama','Parashurama',['Parasurama'],r'\bPara(?:sh|s|ś)ur[aā]ma\b','The Rama of the Bhrigu lineage; not automatically identical to every occurrence of Rama.'),
('churning','Churning of the ocean',['Ocean churning','Samudra Manthan','Amrita'],r'\b(?:churning|amrita|amṛta)\b','Ocean churning and nectar themes. Nectar mentions alone may occur in other contexts.'),
('ganga','Ganga',['Ganges'],r'\b(?:Gang[aā]|Ganges)\b','The river Ganga and associated sacred narratives.'),
('tirtha','Pilgrimage / Tirtha',['Pilgrimage','Tirtha'],r'\b(?:pilgrimage|tirtha|t[iī]rtha)\b','Sacred places and pilgrimage instructions.'),
('vrata','Vows / Vrata',['Vrata','Vows','Fasting'],r'\b(?:vrata|fasting)\b','Vows, fasts, and ritual observances.'),
('death','Death and afterlife',['Death','Afterlife','Rebirth'],r'\b(?:afterlife|rebirth|transmigration)\b','Teachings and narratives concerning death, return, and liberation.'),
('gunas','Gunas / Prakriti',['Gunas','Prakriti'],r'\b(?:gunas?|prakriti)\b','Terms concerning qualities and nature in philosophical passages.'),
('consciousness','Consciousness',['Waking','Dream','Sleep','Turiya'],r'\b(?:consciousness|turiya|tur[iī]ya)\b','Consciousness and states of experience; compare the precise context.'),
('ayurveda','Ayurveda',['Medicine'],r'\b(?:ayurveda|ayurvedic)\b','References to Ayurveda; the modern home-remedy booklet is a separate practical guide.'),
('vastu','Vastu',['Architecture'],r'\bVastu\b','Spatial and architectural topics; modern advice is kept distinct from scriptural passages.')]
existing={n['id'] for n in nodes};concepts=[]
for slug,title,aliases,pattern,summary in CONCEPTS:
 c={'id':'concept-'+slug,'title':title,'type':'concept','parent':'family-concepts','category':'Concepts','summary':summary+' This hub combines literal keyword matches with explicitly tagged editorial connections.','aliases':aliases,'tags':[],'evidence':[],'pattern':pattern}
 nodes.append(c);concepts.append(c)
# Link concepts only to indexed records explicitly tagged with one of their names.
norm=lambda s:re.sub('[^a-z0-9]+','',unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().lower())
tagmap={norm(a):c for c in concepts for a in [c['title'],*c['aliases'],c['id'].replace('concept-','')]}
for n in list(nodes):
 if n['type'] in ['page','document','concept','family','root']:continue
 seen=set()
 for tag in n.get('tags',[]):
  c=tagmap.get(norm(tag))
  if c and c['id'] not in seen:
   seen.add(c['id']);edges.append({'source':n['id'],'target':c['id'],'type':'theme','summary':'Editorial theme tag on this indexed entry; compare the source in context.','evidence':n.get('evidence',[])[:1]})
# Literal mention index preserves every matched PDF page; representative evidence remains inspectable.
for c in concepts:
 pat=re.compile(c.pop('pattern'),re.I)
 for d in manifest:
  hits=[];evidence=[]
  for p,text in enumerate(PAGES[d['id']],1):
   m=pat.search(text)
   if m:
    hits.append(p)
    if len(evidence)<2:
     quote=re.sub(r'\s+',' ',text[max(0,m.start()-65):m.end()+110]).strip();evidence.append({'doc':d['id'],'page':p,'quote':quote})
  if hits:
   edges.append({'source':c['id'],'target':'doc-'+d['id'],'type':'mentions','summary':f"Literal name/term matches on {len(hits)} PDF pages; includes front matter and commentary where present. Search the source to inspect context.",'pages':hits,'evidence':evidence})
   if len(c['evidence'])<2:c['evidence']+=evidence[:1]
# Every node is connected by a contains edge; source entries also point to their page witness.
byid={n['id']:n for n in nodes}
for n in nodes:
 if n.get('parent'):
  if n['parent'] not in byid:raise ValueError(('Missing parent',n['id'],n['parent']))
  edges.append({'source':n['parent'],'target':n['id'],'type':'contains','evidence':[]})
 if n.get('doc') in docs and n.get('page') and n['type'] not in ['page','document']:
  pid=f"page-{n['doc']}-{n['page']}"
  if pid not in byid:raise ValueError(('Bad page',n['id'],pid))
  edges.append({'source':n['id'],'target':pid,'type':'source','summary':'Source witness at the indexed starting page.','evidence':[{'doc':n['doc'],'page':n['page']}]})
# Traditional Veda affiliations are the compilation's own labels, not Samhita containment.
for n in nodes:
 if n.get('vedaAffiliation'):
  a=n['vedaAffiliation'].lower();v='rigveda' if 'rig' in a else 'samaveda' if 'sama' in a else 'atharvaveda' if 'atharva' in a else 'yajurveda' if 'yajur' in a else None
  if v and 'v-'+v in byid:edges.append({'source':n['id'],'target':'v-'+v,'type':'traditional-affiliation','summary':'Vedic affiliation given by the supplied Upanishad compilation. This is not containment in the independent Samhita PDF.','evidence':[{'doc':n['doc'],'page':n.get('vedaAffiliationPage',n['page'])}]})
unique={}
for e in edges:
 if e['source'] not in byid or e['target'] not in byid:raise ValueError(('Invalid edge',e))
 key=(e['source'],e['target'],e.get('type','related'))
 if key not in unique:unique[key]=e
edges=list(unique.values())
notes=[{'title':'Scope of completeness','text':'All 30 supplied PDFs and all 7,984 physical PDF pages are represented. All 108 catalogued Upanishads and the machine-indexed Vedic and Purana headings are navigable. Curated narrative summaries and semantic links are selective, not an exhaustive scholarly annotation of every embedded story or verse.'},{'title':'How to read a connection','text':'Contains means an organizational parent. Source points to a PDF page. Mentions means a literal term match, including front matter or modern commentary where present. Theme and comparison links are editorial. Traditional affiliation follows the supplied compilation; none of these relations proves historical derivation.'},{'title':'Page references','text':'Every reference uses one-based PDF page numbers, not printed page or verse numbers. A section and its following commentary can begin or end on the same physical page.'},{'title':'Text recognition','text':'Matsya, Brahmanda, and the yoga guide required local OCR. OCR can misread names, numbers, accents, and columns. Open the original scan to check any quotation.'}]+notes
stats={'nodes':len(nodes),'edges':len(edges),'documents':len(manifest),'pages':sum(d['pages'] for d in manifest),'types':dict(collections.Counter(n['type'] for n in nodes)),'relations':dict(collections.Counter(e['type'] for e in edges))}
A={'title':'Vedic Atlas','version':1,'created':'2026-11-02','scope':'Supplied input files only; semantic annotations are selective.','stats':stats,'documents':manifest,'nodes':nodes,'edges':edges,'notes':notes}
(O/'atlas.json').write_text(json.dumps(A,ensure_ascii=False,separators=(',',':')))
(O/'atlas-data.js').write_text('window.ATLAS='+json.dumps(A,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n')
(O/'atlas-pages.js').write_text('window.PAGES='+json.dumps(PAGES,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';\n')
ns='http://graphml.graphdrawing.org/xmlns';ET.register_namespace('',ns);gml=ET.Element('{'+ns+'}graphml')
for key,target in [('title','node'),('type','all'),('summary','all'),('doc','node'),('page','node'),('evidence','all')]:ET.SubElement(gml,'{'+ns+'}key',{'id':key,'for':target,'attr.name':key,'attr.type':'string'})
g=ET.SubElement(gml,'{'+ns+'}graph',{'id':'vedic-atlas','edgedefault':'directed'})
for n in nodes:
 el=ET.SubElement(g,'{'+ns+'}node',{'id':n['id']})
 for k in ['title','type','summary','doc','page','evidence']:
  if n.get(k):ET.SubElement(el,'{'+ns+'}data',{'key':k}).text=json.dumps(n[k],ensure_ascii=False) if isinstance(n[k],list) else str(n[k])
for i,e in enumerate(edges):
 el=ET.SubElement(g,'{'+ns+'}edge',{'id':'e'+str(i),'source':e['source'],'target':e['target']})
 for k in ['type','summary','evidence']:
  if e.get(k):ET.SubElement(el,'{'+ns+'}data',{'key':k}).text=json.dumps(e[k],ensure_ascii=False) if isinstance(e[k],list) else str(e[k])
ET.ElementTree(gml).write(O/'atlas.graphml',encoding='utf-8',xml_declaration=True)
(O/'statistics.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
