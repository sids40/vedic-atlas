from pathlib import Path
import json,re,unicodedata
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'corpus/manifest.json').read_text())
manifest=[d for d in manifest if d['category']=='Puranas']
slug=lambda t:re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower()).strip('-')
N=[];E=[];notes=[]
P={d['id']:[json.loads(l) for l in (R/'corpus'/(d['id']+'.jsonl')).read_text().splitlines()] for d in manifest}
worknames={'agni-puranas':'Agni Purana','bhavisya-puranas':'Bhavishya Purana','brahma-puran':'Brahma Purana','brahma-vaivart-puran':'Brahma Vaivarta Purana (supplied title)','garuda-purana':'Garuda Purana','kurma-puran':'Kurma Purana','linga-purana':'Linga Purana','markandeya-puran':'Markandeya Purana','matsyapurana-english':'Matsya Purana','narad-puran':'Narada Purana','padma-puran':'Padma Purana','shrimad-bhagwat-puran':'Bhagavata Purana','the-skanda-purana':'Skanda Purana — Part I, Kedara section','vamana-puran':'Vamana Purana','varaha-purana':'Varaha Purana','brahmaand-purana':'Brahmanda Purana'}
work_summaries={
'agni-puranas':'An encyclopedic supplied retelling: avatars, Rama and Krishna, ritual, sacred geography, kingship, grammar, medicine, yoga and knowledge of Brahman.',
'bhavisya-puranas':'A short supplied devotional selection presenting claims about predictions of religions, kings and teachers. These are claims made by this edition; the map does not establish their date or historical accuracy.',
'brahma-puran':'A five-page supplied overview of the iconography and symbolic attributes of Brahma, Sarasvati, Vishnu and Lakshmi; not an exhaustive Brahma Purana edition.',
'brahma-vaivart-puran':'The introduction advertises the four khands and Radha–Krishna, while the numbered body surveys creation, dynasties and pilgrimage narratives. The supplied title is retained without certifying alignment with a complete canonical edition.',
'garuda-purana':'A supplied overview of Vishnu, Garuda, creation, mantras, astrology, ancestral rites, Rama, Krishna, devotion, self-realization and death.',
'kurma-puran':'Vishnu as Kurma frames teachings on creation, Shiva and Vishnu, Parvati, dynasties, sacred places, ritual and the Ishvara Gita; the supplied retelling explicitly compares narrative variants.',
'linga-purana':'A supplied five-part retelling centered on Shiva, the linga, creation, yoga, devotion, sacred geography and narratives of Dhruva, Andhaka, Jalandhara and Upamanyu.',
'markandeya-puran':'A supplied retelling framed by Jaimini and the wise birds: Harishchandra, Madalasa and Alarka, Dattatreya, cosmic cycles and the Goddess narratives embedded under Savarni Manu.',
'matsyapurana-english':'The supplied 488-page PDF initially has no extractable text layer; image/OCR coverage must be consulted before treating its stories as fully indexed.',
'narad-puran':'A supplied Narada retelling with Markandeya, Ganga, Sagara, Saudasa and Bali. Its opening page also contains a carryover from Linga Purana, excluded from Narada narrative classification.',
'padma-puran':'A supplied five-khanda overview connecting creation, moral tales, sacred places, Rama’s horse sacrifice, Vishnu’s avatars and Krishna.',
'shrimad-bhagwat-puran':'A supplied twelve-chapter retelling centered on devotion: Parikshit and Shukadeva, Kapila, Dhruva, Prahlada, Gajendra and an extensive Krishna narrative.',
'the-skanda-purana':'This supplied PDF is Part I only: Maheshvarakhanda, Kedarakhanda, chapters 1–35, followed by an index. It covers Daksha, ocean churning, Bali, Shiva–Parvati, Karttikeya and Shiva worship.',
'vamana-puran':'A supplied retelling containing Vamana and Bali alongside Shiva–Sati, the Goddess, Nara–Narayana, Kurukshetra pilgrimage, Andhaka and Gajendra.',
'varaha-purana':'A supplied eleven-section retelling framed by Varaha and Prithvi: creation, deities, vows, pilgrimage, ancestors, Nachiketa and the nature of realization.',
'brahmaand-purana':'The supplied 248-page PDF initially has no extractable text layer; image/OCR coverage must be consulted before treating its stories as fully indexed.'}
for logical,title,docs in [('p-shiva','Shiva Mahapurana',['shiv-maha-purana-1','shiv-maha-purana-2']),('p-vishnu','Vishnu Purana',['vishnu-puran-1','vishnu-puran-2'])]:
 N.append({'id':logical,'title':title,'type':'text','parent':'family-puranas','doc':docs[0],'page':1,'endPage':len(P[docs[0]]),'summary':('Two supplied files form a split retelling; their boundary pages overlap. ' + ('Shiva worship, cosmic manifestations, Sati–Parvati, Ganesha, Karttikeya, demons, lingas and yoga.' if logical=='p-shiva' else 'Creation, Dhruva and Prahlada, geography, Vedic branches, dynasties and Krishna.')),'aliases':[],'tags':['Shiva' if logical=='p-shiva' else 'Vishnu'],'evidence':[{'doc':docs[0],'page':1,'quote':P[docs[0]][0]['text'][:240]}]})
for d in manifest:
 doc=d['id'];title=worknames.get(doc,('Shiva Mahapurana' if doc.startswith('shiv-') else 'Vishnu Purana')+' — supplied volume '+doc[-1]);par='p-shiva' if doc.startswith('shiv-') else 'p-vishnu' if doc.startswith('vishnu-') else 'family-puranas'
 N.append({'id':'p-'+doc,'title':title,'type':'volume' if par!='family-puranas' else 'text','parent':par,'doc':doc,'page':1 if doc!='narad-puran' else 2,'endPage':d['pages'],'summary':work_summaries.get(doc,'A split supplied retelling; follow the page links for the passage in this volume.'),'aliases':[],'tags':[],'evidence':[] if not d['text_chars'] else [{'doc':doc,'page':1,'quote':P[doc][0]['text'][:220]}]})
# Work-level citations begin on a readable page in that work, excluding Narada's Linga carryover.
for work in N:
 if work.get('type') not in ['text','volume'] or not work.get('doc'):continue
 doc=work['doc'];start=2 if doc=='narad-puran' else 1
 candidates=[p for p in P[doc] if p['page']>=start and len(p['text'].strip())>40]
 if candidates and doc not in ['matsyapurana-english','brahmaand-purana']:
  first=candidates[0];work['page']=first['page'];work['evidence']=[{'doc':doc,'page':first['page'],'quote':first['text'][:220]}]
# Match body headings with actual PDF page locations. Parent based on numbered hierarchy.
for d in manifest:
 doc=d['id'];pages=P[doc]
 if not d['text_chars'] or doc in ['the-skanda-purana','matsyapurana-english','brahmaand-purana']:continue
 headings=[]
 for p in pages:
  lines=p['text'].splitlines(keepends=True);offset=0
  for line in lines:
   m=re.match(r'^\s*(\d+(?:\.\d+){1,4})\s*([A-Za-z‘“][^\n]{1,150})\s*$',line)
   if m:
    code,title=m.groups();title=title.strip()
    if doc=='narad-puran' and not code.startswith('18.'):offset+=len(line);continue
    headings.append({'code':code,'title':title,'page':p['page'],'offset':offset,'line':line.strip(),'kind':'numbered'})
   elif 8<=len(line.strip())<=130 and re.fullmatch(r"[A-Z0-9 ,:;’'()\-/&–]+",line.strip()) and len(re.findall('[A-Z]',line))>=8:
    title=line.strip().title()
    if re.search(r'\b(?:THE|OF|TO|BIRTH|KILLING|SALVATION|ARRIVAL|DEPARTURE|MARRIAGE|WORSHIP|MIGRATION|FLUTE|LIFTING|STEALING|GOPIS|GOVARDHAN|KALIYA|PRADYUMN|SUDAMA|SYAMANTAK|BHRAMAR|GEET|NAMING|BREAKING|SENDING|BATTLES|ATTACHMENT|IMPORTANCE|APPEARANCE|MEETING|DIVISION|DECLINE|INCARNATION|TALE|TALES|PURIFICATION|KING|KINGDOM|GENEALOGY)\b',line.strip()) and not re.match(r'^(OM|Meaning|Downloaded|This Purana|END OF)',line.strip(),re.I):headings.append({'code':'upper-'+str(p['page'])+'-'+str(offset),'title':title,'page':p['page'],'offset':offset,'line':line.strip(),'kind':'upper'})
   offset+=len(line)
 # Build source slices after heading to next actual heading.
 for i,h in enumerate(headings):
  if any(x['code']==h['code'] for x in headings[:i]):continue
  next_h=headings[i+1] if i+1<len(headings) else None
  text=pages[h['page']-1]['text'][h['offset']:]
  if next_h and next_h['page']==h['page']:text=text[:next_h['offset']-h['offset']]
  elif next_h:
   for p in pages[h['page']:next_h['page']-1]:text+='\n'+p['text']
   text+='\n'+pages[next_h['page']-1]['text'][:next_h['offset']]
  else:
   for p in pages[h['page']:]:text+='\n'+p['text']
  body=re.sub(r'\s+',' ',text.split('\n',1)[1] if '\n' in text else '').strip()
  body=re.sub(r'^This (?:chapter|Section) contains[^.]*\.\s*','',body,flags=re.I)
  summary=body[:320]
  if len(body)>320:summary=summary.rsplit(' ',1)[0]+'…'
  if not summary:summary='Section heading in the supplied retelling. Open the PDF page for context.'
  if doc=='bhavisya-puranas':summary='This supplied section asserts: '+summary
  typ='hymn' if re.search(r'geet|gita|stotra|thousand names|sahastranaam|eulogi',h['title'],re.I) else 'story' if re.search(r'tale|birth|king |kills|killing|incarnat|avatar|marri|battle|curse|salvation|manifest|sati|dhruv|prahlad|prithu|nachiketa|yayati|gautama|markandeya|brahma.s head|doves|hunter|demon|alark|madalasa|beggar|kirat|upamanyu',h['title'],re.I) else 'section'
  par='p-'+doc
  if h['kind']=='numbered':
   parent_code=h['code'].rsplit('.',1)[0]
   if any(x['code']==parent_code for x in headings):par='p-'+doc+'-'+parent_code.replace('.','-')
  else:
   prev=[x for x in headings[:i] if x['kind']=='numbered']
   if prev:par='p-'+doc+'-'+prev[-1]['code'].replace('.','-')
  ident='p-'+doc+'-'+h['code'].replace('.','-')
  N.append({'id':ident,'title':h['title'],'type':typ,'parent':par,'doc':doc,'page':h['page'],'endPage':next_h['page'] if next_h else d['pages'],'summary':summary,'aliases':[],'tags':[],'evidence':[{'doc':doc,'page':h['page'],'quote':h['line']+' '+body[:190]}],'sourceCode':h['code'],'method':'extracted heading with passage opening'})
# Skanda chapter boundaries: printed chapter start + four front matter pages.
skanda=[(1,'Daksha’s Insolence',1),(2,'Sati’s Arrival at Daksha’s Sacrifice',7),(3,'Virabhadra Comes to the Yajna',13),(4,'Virabhadra Fights Vishnu and Others',20),(5,'Meritoriousness of Devotion to Shiva',26),(6,'Curse to Brahma and Others',42),(7,'Worship of the Linga',47),(8,'The Story of a Thief; Incarnation of Rama',53),(9,'The Churning of the Ocean',64),(10,'Shiva Swallows the Poison',74),(11,'Ganesha Worship and Manifestation of Lakshmi',82),(12,'Devas Taste the Divine Nectar',90),(13,'The Fight between Devas and Asuras',96),(14,'Resuscitation of Dead Daityas',106),(15,'Nahusha and Yayati: Indrahood and Fall',109),(16,'Dadhichi’s Gift of His Body',118),(17,'Vritra Killed; Bali Prepares for War',126),(18,'Vamana Arrives at Bali’s Sacrifice',151),(19,'Shukra Curses Bali; Vamana Grants a Boon',169),(20,'Shiva Linga and Manifestation of Bhavani',176),(21,'Parvati’s Penance',181),(22,'Shiva Reveals Himself to Parvati',196),(23,'Shiva’s Marriage',207),(24,'Marriage Ceremony: Accommodating the Devas',214),(25,'The Marriage Ritual',220),(26,'Shiva–Parvati Marriage Festivities',227),(27,'Birth of Kumara Karttikeya',232),(28,'Preparations for War',242),(29,'The Battle against Taraka',247),(30,'Taraka Is Slain',254),(31,'The Greatness of Shivalinga',258),(32,'The Burning of Kala',268),(33,'The Greatness of Shivaratri',277),(34,'Shiva Loses to Parvati at Dice',287),(35,'Parvati as Shabari Brings Shiva Back',301)]
for i,(ch,title,printed) in enumerate(skanda):
 pg=printed+4
 N.append({'id':'p-skanda-ch-'+str(ch),'title':title,'type':'story' if ch not in [5,7,20,24,25,31,33] else 'section','parent':'p-the-skanda-purana','doc':'the-skanda-purana','page':pg,'endPage':skanda[i+1][2]+3 if i+1<len(skanda) else 310,'summary':'Chapter '+str(ch)+' of the supplied Kedarakhanda: '+title+'. The contents list supplies the title and printed-page location.','aliases':[],'tags':[],'sourceCode':str(ch),'method':'contents list, printed-to-PDF page offset checked','evidence':[{'doc':'the-skanda-purana','page':pg,'quote':re.sub(r'\s+',' ',P['the-skanda-purana'][pg-1]['text'][P['the-skanda-purana'][pg-1]['text'].find('CHAPTER'):])[:240]}]})
# A few interpreted summaries replace passage openings. Each uses a heading-attested source boundary.
curated={
('varaha-purana','8.10.1'):'Nachiketa visits Yama’s realm after repeatedly asking his father to whom he will be given. This retelling concerns the afterlife and conduct; compare it with the Katha Upanishad without assuming the versions are identical.',
('markandeya-puran','7.9.8.1'):'Suratha and the merchant Samadhi ask Medha why attachment persists after betrayal. Medha introduces Mahamaya through the account of Vishnu, Madhu and Kaitabha.',
('markandeya-puran','7.9.8.2'):'The defeated gods combine their radiance into the Goddess, give her their weapons, and watch her destroy Mahishasura’s forces.',
('markandeya-puran','7.9.8.7'):'Raktabija multiplies from each drop of blood. The Goddess directs Kali to drink the blood, ending the multiplication and defeating him.',
('markandeya-puran','7.9.8.9'):'When Shumbha says that her strength depends on others, the Goddess absorbs the manifested powers into herself before their final battle.',
('markandeya-puran','7.9.8.12'):'Suratha seeks restoration of kingship; the merchant seeks freedom from attachment. Their different requests bring the Goddess narratives back to the opening question about worldly bonds.',
('markandeya-puran','7.4.9'):'Madalasa teaches Alarka how a king should govern: protect subjects, examine advisers, restrain desire and avoid complacency. The surrounding narrative connects family instruction with later yoga teaching.',
('markandeya-puran','7.7.3'):'Dattatreya instructs Alarka in detachment and realization. Follow the adjacent yoga sections for concentration, Om, practice and its obstacles.',
('agni-puranas','10.9.4'):'The passage distinguishes atman from body, senses and mind, then identifies the individual self with Brahman. It offers a direct philosophical bridge from a Purana to Upanishadic inquiry.',
('agni-puranas','10.1.1'):'Vishnu’s fish incarnation guides Manu through the deluge. The story connects preservation across cosmic destruction with the recurring Matsya motif.',
('agni-puranas','10.1.2'):'The tortoise incarnation supports the mountain used in the gods’ and demons’ ocean churning. Follow the other Purana versions for changes in emphasis.',
('brahma-vaivart-puran','9.19'):'Gautama’s hermitage survives a drought. A plan involving Ganesha leads him to bring a portion of Ganga from Shiva’s hair; the story explains a sacred river and place.',
('brahma-vaivart-puran','9.35'):'A devoted singer promises a brahmarakshasa that he will return after Vishnu worship. The tale connects truthfulness, devotion and the release of the demon.',
('kurma-puran','12.12'):'Daksha’s sacrifice becomes the setting for conflict with Shiva and the destructive intervention of Virabhadra. The supplied retelling explicitly comments on differences between Purana versions.',
('kurma-puran','12.31'):'A substitute or illusory Sita is distinguished from the Sita protected through divine intervention. This is a narrative variant in the supplied retelling, not a claim that every Rama tradition uses it.',
('kurma-puran','12.29'):'The Ishvara Gita section turns to Shiva’s instruction on spiritual knowledge. It offers a bridge between devotional narrative and philosophical/yogic teaching.',
('shrimad-bhagwat-puran','16.6.1'):'Ajamila’s deathbed utterance of Narayana opens a discussion of divine messengers, the name of the Lord and the relation between moral action and devotion.',
('shrimad-bhagwat-puran','16.8.2'):'Gajendra the elephant, caught by a crocodile, turns to the divine for refuge. The retelling makes surrender and deliverance central.',
('shrimad-bhagwat-puran','16.8.3'):'The gods and demons churn the ocean together. Their quest for nectar introduces cooperation, rivalry and Vishnu’s intervention.',
('shrimad-bhagwat-puran','16.4.5'):'The fable of Puranjana uses a king’s story to convey teaching about embodied life. Read the allegory alongside the text’s explicit instruction passages.',
('shrimad-bhagwat-puran','16.10.20'):'Venugeet is the song centered on Krishna’s flute. It belongs to the devotional poetry embedded within the Krishna narrative.',
('shrimad-bhagwat-puran','16.10.29'):'Gopika Geet voices the gopis’ longing in Krishna’s absence, placing a devotional song inside the sequence of disappearance and reunion.',
('shrimad-bhagwat-puran','16.10.45'):'Bhramar Geet presents the gopis’ speech associated with the bee and Uddhava’s visit. The episode links absence, memory and devotion.',
('shrimad-bhagwat-puran','16.11.4'):'Bhikshu Geet embeds a renunciant’s song in the later teachings. It connects suffering and mental discipline with the movement toward liberation.',
('shrimad-bhagwat-puran','16.12.3'):'Parikshit’s final liberation closes the frame of a king listening to Shukadeva while facing death; it returns the long narrative to the purpose of hearing it.',
('linga-purana','17.1.14'):'Brahma and Vishnu encounter the immeasurable linga. The episode connects their dispute with Shiva’s manifestation as a cosmic sign.',
('shiv-maha-purana-1','5.1.6'):'The pillar of fire interrupts the dispute of Brahma and Vishnu. Their search for its limits becomes a story about Shiva’s manifestation.',
('shiv-maha-purana-1','5.2.52'):'Sati gives up her life at Daksha’s sacrifice after the insult to Shiva; the following episodes narrate Virabhadra and the destruction of the sacrifice.',
('shiv-maha-purana-1','5.2.79'):'Shiva’s fiery response reduces Kamadeva to ashes during the attempt to awaken his desire. The episode belongs to the larger Parvati marriage sequence.',
('shiv-maha-purana-1','5.2.111'):'Shiva severs Ganesha’s head in the conflict at Parvati’s doorway. The next section tells of Ganesha’s restoration.',
('shiv-maha-purana-2','5.2.141'):'Tulsi curses Vishnu after the deception that contributes to Shankhachuda’s death. This supplied retelling should be read in its own narrative context.',
('shiv-maha-purana-2','5.4.31'):'The text distinguishes stages or forms of liberation within a Shaiva devotional framework.',
('padma-puran','2.4.5'):'Lava stops the sacrificial horse during Rama’s ashvamedha. The ensuing battle sequence moves toward the recognition of Rama’s family.',
('vamana-puran','6.23.3'):'Vamana makes his request at Bali’s sacrifice. The following scenes narrate the cosmic measure, Brahma’s worship and Bali’s descent to Patala.',
('vishnu-puran-1','3.2.12'):'Bharata’s life links kingship, attachment and rebirth; the following Jadabharata instruction turns this narrative into a teaching on the self.',
('vishnu-puran-1','3.2.15'):'Ribhu teaches Nidagha through ordinary distinctions and their limits. This offers a dialogue-centered route into the text’s spiritual teaching.',
('vishnu-puran-1','3.3.4'):'The supplied retelling traces branches of the Rig Veda. This is an explicit Purana-to-Veda textual connection rather than a shared-character link.'}
for n in N:
 key=(n.get('doc'),n.get('sourceCode'))
 if key in curated:n['summary']=curated[key];n['method']='curated reading of supplied passage'
# Shared narrative motifs: title-based joins, therefore explicit recurrences only, not historical derivation.
motifs=[
('daksha-sacrifice','Daksha’s sacrifice and Sati','sati|daksha.*(?:yag|sacrific|story|animos)|virabhadra|veerbhadra','Conflict around Daksha’s sacrifice, Sati and Shiva recurs with different details and theological emphases.'),
('cosmic-linga','The cosmic linga / pillar of fire','pillar of fire|anaal.stambh|origin of shiva linga|dispute between brahma|linga.*bhavani','Brahma–Vishnu disputes and Shiva’s immeasurable manifestation form a recurring Shaiva narrative.'),
('ocean-churning','Churning the ocean','churning|kurma$|matsya and kurma|swallows the poison|divine nectar|manifestation of lakshmi','The churning cycle links Kurma, poison, nectar and Lakshmi; not every selected passage retells the whole cycle.'),
('matsya-flood','Matsya and the deluge','matsya|matysa','Vishnu’s fish incarnation links preservation, Manu and cosmic destruction in the supplied stories.'),
('narasimha-prahlada','Narasimha and Prahlada','narasimha|nrisimha|nri.simha|prahlad|hiranyakashipu|hiranyakshipu','The supplied texts vary in their treatment of Prahlada, divine protection and Narasimha.'),
('vamana-bali','Vamana and Bali','vaman|vaaman|bali|^vali$','Vamana’s request at Bali’s sacrifice, cosmic expansion and Bali’s fate recur across these texts.'),
('varaha-earth','Varaha and the rescue of Earth','varaha|varah|liberation of earth|hiranyaksha','The boar incarnation and the preservation of Earth provide a recurring cosmological narrative.'),
('dhruva','Dhruva’s devotion','dhruv','Dhruva’s devotion, penance and divine encounter recur across supplied Purana retellings.'),
('prithu','Vena, Prithu and the Earth','prithu|king ven|^prithu$','The contrast between Vena’s kingship and Prithu’s rule links royal conduct, Earth and sustenance.'),
('ganga','The descent and sacred geography of Ganga','ganga|ganges|gautama|goutama|gautam','These episodes connect the descent of Ganga or Gautama’s river with pilgrimage; the accounts should be compared separately.'),
('rama-cycle','Rama and the Ramayana cycle','rama|ramayana|sita|shambuk|lav |ravana|ravan|rameshwar|ashvamedh','Rama’s life and related episodes occur inside several Purana retellings; they are not separate supplied Ramayana editions.'),
('krishna-cycle','Krishna and his devotees','krshna|krishna|kansa|gopis|gopika|govardhan|goverdhan|yadu|rukmini|rukmani|putana|pootana|sudama|syamantak|venu.?geet|bhramar','Krishna narrative passages link childhood, Mathura, Dvaraka, family, devotion and the close of the Yadu lineage.'),
('gajendra','Gajendra and the crocodile','gajendra','The elephant’s appeal for refuge becomes a shared devotional narrative.'),
('harishchandra','Harishchandra and truthfulness','harishchandra','The king’s trials provide a recurring narrative around truth and duty.'),
('madalasa-alarka','Madalasa, Alarka and instruction','madalasa|alark','Family narrative leads into kingship, detachment and Dattatreya’s yoga teaching.'),
('karttikeya-taraka','Karttikeya and Taraka','kartikeya|kaartikeya|karttikeya|taraka|taraka.sur|tarakasur','The birth of Shiva and Parvati’s son connects their marriage to the defeat of Taraka.'),
('ganesha','Ganesha’s manifestation','ganesh|ganapati','Ganesha’s origins and worship recur, with differing narrative settings.'),
('andhaka','Andhaka and Shiva','andhak','The demon Andhaka appears in several Shaiva narrative cycles.'),
('jalandhara','Jalandhara and Vrinda','jalandhar|jaladhar|vrinda','The Jalandhara cycle links divine battle, deception and Vrinda; distinguish it from the separate Shankhachuda–Tulsi story.'),
('tripura','The destruction of Tripura','tripurasur','Shiva’s destruction of the three cities appears in the supplied Shiva narrative.'),
('brahma-head','Brahma’s head and Bhairava','brahma.s head|shiva and brahma|bhairav|severed head','Brahma’s severed head and the consequences of killing connect Shiva/Bhairava with expiation.'),
('nandi','Nandi’s birth and devotion','nandi|shilad','Nandi’s origins and relation to Shiva recur as a devotion narrative.'),
('yayati','Yayati and desire','yayati','Yayati’s kingship, desire and family relations recur across the dynasty narratives.'),
('sagara','Sagara and his descendants','sagar|baahu|suryavansh','Sagara’s dynasty and its consequences connect kingship, sacrifice and the Ganga cycle.'),
('markandeya','Markandeya, death and cosmic vision','markandey|markandaya','Markandeya appears both as narrator and as a figure confronting death or cosmic dissolution; these roles are distinct.'),
('nachiketa','Nachiketa and Yama','nachiketa','The Varaha retelling supplies a direct comparison point with the Nachiketa dialogue in the Katha Upanishad.'),
('dadhichi-vritra','Dadhichi, Vritra and Indra','dadhichi|dadhici|vritrasur|vrittrasur|vritra','Sacrifice of Dadhichi’s body, Indra’s weapon and Vritra form an interlinked narrative cycle.'),
('yoga-instruction','Yoga and spiritual instruction','yoga|yogadhyay|ishvara gita|brahm.gita|knowledge of brahman|self.realization|shiva.gyan','These are thematic links among passages about practice and realization, not a claim that their systems or doctrines are identical.'),
('ancestor-rites','Ancestors, death and karma','shraddh|shraadh|shradha|pind|pinda|last rites|death and after|karma.*consequence|karma vipak|hell|naraka','Ritual and cosmological passages connect ancestors, death and the consequences of action within the supplied traditions.'),
('vedas-branches','Vedic transmission and branches','branches of.*veda|veda vyasa|vedavyasa|origin of vidya','These sections explicitly discuss the transmission, arrangement or branches of Vedic knowledge.')]
for mid,title,pat,desc in motifs:
 matches=[n for n in N if n['type'] not in ['text','volume'] and re.search(pat,n['title'],re.I)]
 if not matches:continue
 id='motif-'+mid
 N.append({'id':id,'title':title,'type':'theme','parent':'family-connections','summary':desc,'aliases':[],'tags':[],'evidence':[e for n in matches[:3] for e in n.get('evidence',[])[:1]]})
 for n in matches:
  n['tags'].append(title)
  E.append({'source':n['id'],'target':id,'type':'shared narrative' if mid not in ['yoga-instruction','ancestor-rites','vedas-branches'] else 'shared theme','summary':'The supplied section explicitly names this narrative or topic in its heading. Compare the passages; the link does not establish borrowing or doctrinal identity.','evidence':n.get('evidence',[])[:1]})
# Add generic concept tags from explicit wording, not invisible assumptions.
terms={'Shiva':r'\bshiv|\bsiva|rudra|linga','Vishnu':r'vishnu|viṣṇu|narayan','Devi':r'goddess|parvati|durga|bhagwati|shakti','Brahman':r'\bbrahman\b|brahma.gyana','Atman':r'\batman\b|\bself.realization','Yoga':r'\byoga\b|meditat|yogi','Bhakti':r'devot|bhakti','Karma':r'\bkarma','Dharma':r'\bdharma|duties|righteous','Creation':r'creation|origin of the universe','Liberation':r'liberat|salvation|moksha','Ritual':r'ritual|worship|vrata|yagya|yajna','Pilgrimage':r'pilgrim|tirth|teerth|sacred places','Vedic transmission':r'vedas|veda vyasa|vedavyasa|branches of'}
for n in N:
 if n['type']=='theme':continue
 test=n['title']+' '+n.get('summary','')
 n['tags']+= [k for k,p in terms.items() if re.search(p,test,re.I)]
 n['tags']=list(dict.fromkeys(n['tags']))
notes=[
'The supplied library contains 20 Purana PDFs representing 18 named Purana works. Shiva and Vishnu are each split over two overlapping files.',
'Most text-readable Purana PDFs are short English overviews or retellings with modern editorial comments. A file bearing a Purana name is not evidence that the whole Sanskrit work is present.',
'Skanda is explicitly Part I: Book I, Maheshvarakhanda, Section I, Kedarakhanda, chapters 1–35. PDF page = printed page + 4. Chapter 6 is corrected to PDF 46 (actual printed 42); the contents list incorrectly says 41.',
'Brahma Vaivarta supplied file: introductory description and numbered narrative body differ in emphasis. Retain supplied identification and avoid certifying canonical completeness.',
'Narada supplied file begins with Linga Purana carryover on PDF page 1; Narada section 18.1 begins on PDF page 2.',
'Shiva volume 1 pages 47 and volume 2 page 1 overlap at sections 5.2.126–5.2.129; Vishnu volume 1 page 39 and volume 2 page 1 overlap at section 3.4.4. Keep these witnesses separate, not additional stories.',
'Bhavishya prediction and historical assertions are the supplied edition’s claims. No external chronology or historical authentication was performed.',
'Heading extraction gives navigable source units, not verified Sanskrit verse/chapter numbering. Numbering such as 16.10.20 belongs to the supplied retelling.',
'Section summaries labeled extracted heading with passage opening are shortened source openings; curated readings are explicitly marked. Shared-narrative edges are title-attested comparison links, not historical derivation or proof of theological agreement.',
'Matsya and Brahmanda initially had no extractable text; OCR-generated headings, if added by the main analysis, must retain their OCR status. Visual title evidence identifies the Matsya scan as Matsya Puranam Part I (1916), rather than a complete Purana.'
]
# Exact normalized local witnesses: each excerpt must be a continuous substring of its cited page.
norm=lambda t:re.sub(r'\s+',' ',t).strip()
for n in N:
 for e in n.get('evidence',[]):
  raw=norm(P[e['doc']][e['page']-1]['text']);q=norm(e['quote'])
  if q and q in raw:e['quote']=q
  else:
   key=n.get('sourceCode','');pos=raw.find(key) if key else -1
   if pos<0 and n['id'].startswith('p-skanda-ch-'):pos=raw.find('CHAPTER')
   if pos<0:pos=0
   e['quote']=raw[pos:pos+240]
for e in E:
 for ev in e.get('evidence',[]):
  raw=norm(P[ev['doc']][ev['page']-1]['text'])
  if norm(ev['quote']) not in raw:ev['quote']=raw[:240]
assert all(norm(e['quote']) in norm(P[e['doc']][e['page']-1]['text']) for n in N for e in n.get('evidence',[]))
assert all(norm(ev['quote']) in norm(P[ev['doc']][ev['page']-1]['text']) for e in E for ev in e.get('evidence',[]))
(R/'analysis/puranas.json').write_text(json.dumps({'nodes':N,'edges':E,'notes':notes},ensure_ascii=False,indent=2))
(R/'analysis/puranas-notes.md').write_text('# Purana analysis and coverage\n\n'+'\n\n'.join(notes)+'\n\n'+f'Indexed {len(N)} nodes and {len(E)} explicit comparison links.\n')
print(len(N),'nodes',len(E),'edges')
from collections import Counter
print(Counter(n['type'] for n in N))
print(Counter(n.get('doc') for n in N))
