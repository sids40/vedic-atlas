/* Domain acceptance checks for the source-based reading guide. Run with Node.js. */
'use strict';
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const context={window:{}};
vm.createContext(context);
for(const name of ['atlas-data.js','atlas-pages.js','guide-topics.js','guide-engine.js']){
  vm.runInContext(fs.readFileSync(path.join(root,'output',name),'utf8'),context,{filename:name});
}
const {ATLAS,PAGES,GUIDE_TOPICS,VedicGuide}=context.window;
const nodes=new Map(ATLAS.nodes.map(n=>[n.id,n]));
const documents=new Map(ATLAS.documents.map(d=>[d.id,d]));
const guide=VedicGuide.create({atlas:ATLAS,pages:PAGES,topics:GUIDE_TOPICS});
const clean=s=>String(s||'').replace(/\s+/g,' ').trim();
const cases=[];
function checkQuote(doc,page,quote){
  assert(documents.has(doc),'Unknown source document: '+doc);
  assert(Number.isInteger(Number(page))&&page>=1&&page<=documents.get(doc).pages,'Invalid source page: '+doc+':'+page);
  if(quote){
    const prefix=clean(quote).replace(/(?:…|\.\.\.)$/,'');
    assert(clean(PAGES[doc][page-1]).includes(prefix),'Quotation is not on its cited page: '+doc+':'+page+' '+prefix);
  }
}
function validAnswer(answer){
  assert(answer&&typeof answer.intro==='string');
  assert(Array.isArray(answer.results)&&answer.results.length<=5,'Too many results');
  for(const result of answer.results){
    assert(nodes.has(result.id),'Unknown result node: '+result.id);
    assert(typeof result.summary==='string'&&result.summary.length<=600,'Missing or excessive summary');
    if(result.doc)checkQuote(result.doc,result.page,result.quote);
    if(nodes.get(result.id).type==='commentary')assert.equal(result.kind,'commentary','Commentary is not identified');
  }
  for(const edge of answer.connections||[]){
    assert(nodes.has(edge.source)&&nodes.has(edge.target),'Unknown connected node');
    for(const evidence of edge.evidence||[])checkQuote(evidence.doc,evidence.page,evidence.quote);
  }
}
function run(name,question,test,options){
  const start=Date.now();
  const response=guide.ask(question,options);
  validAnswer(response);
  test(response);
  cases.push({name,question,result:'PASS',elapsedMs:Date.now()-start,resultIds:response.results.map(r=>r.id)});
  return response;
}
run('Topic chooser','I am new here. Help me pick a topic',a=>{
  assert.equal(a.intent,'topics');assert(a.topics.length>=6);assert.equal(a.results.length,0);
});
run('Cross-PDF narrative references','Give me a brief summary of Nachiketa and references',a=>{
  const ids=new Set(a.results.map(r=>r.id));assert(ids.has('u-story-nachiketas-and-death'));assert(ids.has('p-varaha-purana-8-10-1'));
  assert(a.connections.length>=1);assert(new Set(a.results.map(r=>r.doc)).size>=2);
});
run('Cross-family comparison','Compare creation across the Vedas and Upanishads',a=>{
  const categories=new Set(a.results.map(r=>nodes.get(r.id).category));
  assert(categories.has('Vedas')&&categories.has('Upanishads'));
  assert(!categories.has('Puranas'));assert(a.results.some(r=>r.id==='rv-10-129'));
});
run('Work-limited references','Only Rigveda references for creation',a=>{
  assert(a.results.length>0);assert(a.results.every(r=>r.doc==='rigveda'));
});
run('Brahman distinct from creator','What is Brahman?',a=>{
  assert(a.results.length>0);assert(a.results.every(r=>r.id!=='concept-brahma'));
});
run('Creator Brahma ranking','What is Brahma?',a=>{
  assert(a.results.length>0);assert(a.results.every(r=>r.id!=='u-brahma-upanishad'));
  assert(a.results.some(r=>r.id==='concept-brahma'||/creator|creation/i.test(r.summary)));
});
run('Mixed Brahma and Brahman distinction','What is the difference between Brahma and Brahman?',a=>{
  assert(a.results.some(r=>r.id==='concept-brahma'),'Creator figure omitted');
  assert(a.results.some(r=>r.id==='concept-brahman'||/brahman/i.test(r.title)),'Brahman omitted');
});
run('Explicitly named Brahma Upanishad preserved','Summarize Brahma Upanishad',a=>{
  assert(a.results.some(r=>r.id==='u-brahma-upanishad'));
});
run('Direct primary-text summary','Summarize Katha Upanishad',a=>{
  assert(a.results.some(r=>r.id==='u-katha-upanishad'));
});
run('Exact hymn reference','Summarize RV 10.129',a=>{
  assert.equal(a.results[0].id,'rv-10-129');assert.equal(a.results[0].page,724);
});
run('Modern commentary classification','Show modern commentaries on Katha',a=>{
  assert(a.results.some(r=>r.kind==='commentary'),'Existing modern commentary not found');
});
run('Compare two collection families','Compare the Upanishads and the Puranas',a=>{
  assert.equal(a.intent,'compare');assert(a.results.length>=2);assert.equal(a.missing,undefined);
});
run('Selected book summary','Summarize this book',a=>{
  assert.equal(a.intent,'summary');assert.equal(a.results[0].id,'p-shiva');
},{focusId:'p-shiva'});
run('Selected text deictic question','What is this about?',a=>{
  assert.equal(a.intent,'summary');assert.equal(a.results[0].id,'u-katha-upanishad');
},{focusId:'u-katha-upanishad'});
run('Scoped topical PDF fallback','Where is Shiva in Yajurveda?',a=>{
  assert(a.results.length>0);assert(a.results.every(r=>r.doc==='yajurveda'));
  assert(a.results.every(r=>r.id!=='v-yajurveda'),'Topic request returned only the work heading');
});
run('Omnibus PDF work boundaries','Where is offerer in Samaveda?',a=>{
  assert(a.results.length>0);assert(a.results.every(r=>r.kind==='page'));
  for(const r of a.results){
    const descendants=ATLAS.nodes.filter(n=>{let p=n;for(let i=0;i<15&&p;i++,p=nodes.get(p.parent))if(p.id==='v-samaveda')return true;return false;});
    assert(descendants.some(n=>n.doc===r.doc&&r.page>=n.page&&r.page<=(n.endPage||n.page)),'Fallback escaped the Samaveda section of an omnibus');
  }
});
run('Selected work cross-book connections','Connect this with other books',a=>{
  assert(a.results.some(r=>r.id==='p-shiva'));assert(a.results.some(r=>r.doc==='padma-puran'||r.doc==='kurma-puran'));assert(new Set(a.results.map(r=>r.doc)).size>=2);assert(a.connections.length>0);
},{focusId:'p-shiva'});
run('Honest missing source','Find the Quantum Unicorn Upanishad',a=>{
  assert.equal(a.missing,true);assert.equal(a.results.length,0);assert(a.topics.length>0);
});
const first=run('Conversation seed','Nachiketa',a=>assert(a.results.length>0));
run('Follow-up retains topic','Tell me more',a=>{
  assert(a.context.terms.includes('nachiketa'));assert(a.results.length>0);
  assert(a.results.some(r=>/nachiketa|katha/i.test(r.title)));
},{history:[{question:'Nachiketa',response:first}]});
run('HTML-like question remains inert','<script>globalThis.guideInjected=true</script> Quantum Unicorn',a=>{
  assert.equal(context.guideInjected,undefined);
});
for(const topic of GUIDE_TOPICS){assert(nodes.has(topic.id));for(const step of topic.steps)assert(nodes.has(step.id));}
const report={result:'PASS',engine:'source-based in-browser retrieval',cases,topicPaths:GUIDE_TOPICS.length,validatedSourceReferences:true};
console.log(JSON.stringify(report,null,2));
