from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
M={d['id']:d for d in json.loads((R/'corpus/manifest.json').read_text())}
norm=lambda t:re.sub(r'\s+',' ',t).strip()
N=[];E=[]
def pages(doc):return [json.loads(l) for l in (R/'corpus'/(doc+'.jsonl')).read_text().splitlines()]
def ev(doc,p,q=None):
 raw=pages(doc)[p-1]['text'];r=norm(raw)
 if not r:return []
 q=norm(q or r[:220]);assert q in r
 return [{'doc':doc,'page':p,'quote':q}]
def node(id,title,parent,doc,page,summary,aliases=[],tags=[],method='curated source-topic metadata',evidence=None):
 N.append({'id':id,'title':title,'type':'text' if parent=='family-bonus' else 'section','parent':parent,'doc':doc,'page':page,'endPage':M[doc]['pages'] if parent=='family-bonus' else page,'summary':summary,'aliases':aliases,'tags':tags,'method':method,'evidence':ev(doc,page) if evidence is None else evidence})
a='ayurvedic-home-remediesenglishebook';v='practical-vastu-professional-guide-1';y='common-yoga-aasana-englishebook'
node('b-ayurveda','Ayurvedic Home Remedies','family-bonus',a,1,'A supplied practical booklet with an index and 25 ingredient entries. This map catalogs the subjects and page locations; the traditional treatment claims are not evaluated here.',tags=['Ayurveda'])
node('b-vastu','Practical Vastu for Homes and Businesses','family-bonus',v,1,'A supplied modern advisory guide to existing homes, shops and offices, presented separately from scripture. Its 44 pages cover spatial principles, direction readings, layouts and correction checklists.',tags=['Vastu'])
node('b-yoga','Common Yoga Protocol','family-bonus',y,1,'A supplied illustrated Ministry of Ayush yoga guide. The 51-page scan includes introductory material, loosening practices, postures, breathing practices and the beginning of Dhyana. Topics listed later in its contents are not present at the end of this supplied file.',tags=['Yoga'],method='source identification from OCR; scan has no original text layer',evidence=ev(y,5,'COMMON YOGA PROTOCOL Ministry of Ayush, Government of India What is Yoga?'))
herbs=[('Adrak / Sonth (ginger)',['Adrak','Sonth','Ardraka','Sunthi']),('Ajvain',['Ajwain','Yavani']),('Anar (pomegranate)',['Dadima']),('Amla',['Amalaki']),('Dalchini (cinnamon)',['Tvak']),('Dhania (coriander)',['Dhanyaka']),('Elaichi (cardamom)',['Ela']),('Ghee (clarified butter)',[]),('Haldi (turmeric)',['Haridra']),('Hing (asafoetida)',['Hingu']),('Jayphal (nutmeg)',['Jatiphala']),('Jeera (cumin)',['Jiraka']),('Kalimirach (black pepper)',['Maricha']),('Karela (bitter gourd)',['Karavellaka']),('Lahsun (garlic)',['Rasona']),('Laung (clove)',['Lavanga']),('Madhu (honey)',['Honey']),('Methi (fenugreek)',['Methika']),('Nariyal (coconut)',['Narikela']),('Neem',['Nimba']),('Nimbu (lemon)',[]),('Pyaj (onion)',['Palandu']),('Pippali (long pepper)',[]),('Saunf (fennel)',['Shatapushpa']),('Tulsi',['Tulasi'])]
for i,(title,aliases) in enumerate(herbs):
 page=i+5;p=pages(a)[page-1];lines=[l.strip() for l in p['text'].splitlines() if l.strip()]
 q=' '.join(lines[:2]) if lines[1].startswith(('(','{')) else lines[0]
 node('b-ayurveda-topic-'+str(i+1),title,'b-ayurveda',a,page,'Ingredient entry '+str(i+1)+' in the supplied home-remedies booklet: '+title+'.',aliases,['Ayurveda'],evidence=ev(a,page,q))
# All Vastu PDF pages: headings are taken directly from their page, after the recurring running title.
for p in pages(v):
 ls=[l.strip() for l in p['text'].splitlines() if l.strip()]
 title=ls[1] if len(ls)>1 else 'Page '+str(p['page'])
 if p['page']==1:title='Practical Vastu for Homes and Businesses — cover'
 node('b-vastu-page-'+str(p['page']),title,'b-vastu',v,p['page'],'Source topic: '+title+'.',tags=['Vastu'],method='page heading extracted from supplied guide',evidence=ev(v,p['page'],' '.join(ls[:3])))
ytitles={1:'Cover — Yoga',2:'Unlettered scan page',3:'Contents — introduction and postures',4:'Contents — postures, breathing and later sections',5:'What is Yoga?',6:'Brief History and Development of Yoga',7:'The Fundamentals of Yoga',8:'Traditional Schools of Yoga',9:'Yogic Practices for Health and Wellness — overview',10:'Yogic Practices — explanatory continuation',11:'General Guidelines for Yoga Practice',12:'During and after the Practice',13:'Food for Thought / How Yoga Can Help',14:'Illustration page',15:'Invocation / Prayer — section opening',16:'Invocation / Prayer — Samgacchadhvam',17:'Sadilaja / Calana Kriyas — Loosening Practices',18:'Neck Movements',19:'Shoulder Movements — illustration',20:'Shoulder Movements — technique',21:'Trunk Movement',22:'Knee Movement',23:'Tadasana — Palm-tree Posture',24:'Vrksasana — Tree Posture',25:'Ardhacakrasana — Half-Wheel Posture',26:'Pada-Hastasana — Hands-to-Feet Posture',27:'Trikonasana — Triangle Posture',28:'Bhadrasana — Firm / Auspicious Posture',29:'Vajrasana — Thunderbolt Posture',30:'Ardhaustrasana — Half-Camel Posture',31:'Ustrasana — Camel Posture',32:'Sasakasana — Hare Posture',33:'Uttanamandukasana — Stretched-up Frog Posture',34:'Vakrasana / Marichyasana — Spinal Twist',35:'Makarasana — prone posture',36:'Bhujangasana — Cobra Posture',37:'Salabhasana — Locust Posture',38:'Setubandhasana — supine posture',39:'Uttanapadasana — Raised Feet Posture',40:'Ardhahalasana — Half-Plough Posture',41:'Pavanamuktasana — Wind-Releasing Posture',42:'Savasana — Corpse / Dead-Body Posture',43:'Kapalabhati — section opening',44:'Kapalabhati — source benefits and cautions',45:'Nadisodhana / Anuloma Viloma Pranayama',46:'Nadisodhana — continuation',47:'Sitali Pranayama',48:'Sitali — source cautions',49:'Bhramari Pranayama',50:'Bhramari — source benefits and cautions',51:'Dhyana — meditation'}
for p in pages(y):
 pg=p['page'];title=ytitles[pg]
 if pg in [2,14]:summary='Scan page '+str(pg)+' is included for complete file navigation; OCR provides no substantive text beyond possible running labels.'
 elif pg in [44,48,50]:summary='The supplied guide’s '+title.lower()+'. This node identifies the subject and location without endorsing the source’s health assertions.'
 else:summary='Source topic in the illustrated Common Yoga Protocol: '+title+'.'
 ls=[l.strip() for l in p['text'].splitlines() if l.strip()]
 q=' '.join(ls[:7])[:240]
 node('b-yoga-page-'+str(pg),title,'b-yoga',y,pg,summary,tags=['Yoga'],method='OCR page topic; names normalized for navigation; verify against scan',evidence=ev(y,pg,q) if q else [])
notes=['The three Bonus PDFs are practical guides, cataloged separately from the Veda, Upanishad and Purana collections.','Ayurvedic Home Remedies has 25 ingredient entries on PDF pages 5–29, preceded by four index/instruction pages. The map does not reproduce dosing instructions or assess efficacy.','Vastu is a modern 44-page advisory guide, not a supplied ancient Vastu scripture. Headings and topic labels describe this particular file.','The scanned Yoga PDF contains 51 pages and ends at the Dhyana section. Sankalpa, Shantih Patha, references, Yoga Geet and expert committee items appear in its contents, but those later sections are not included as body pages in the supplied file.','Yoga title normalization is based on OCR and the supplied contents. PDF page numbers are used throughout. Blank or illustration-dominated pages remain navigable.']
assert len(N)==123
for n in N:
 for e in n['evidence']:
  assert norm(e['quote']) in norm(pages(e['doc'])[e['page']-1]['text'])
(R/'analysis/bonus.json').write_text(json.dumps({'nodes':N,'edges':E,'notes':notes},indent=2,ensure_ascii=False))
print(len(N),'bonus nodes; all evidence exact normalized page substrings')
