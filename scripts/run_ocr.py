from pathlib import Path
import subprocess,concurrent.futures,json,time
R=Path(__file__).resolve().parents[1]
M=json.loads((R/'corpus/manifest.json').read_text())
jobs=[]
for d in M:
 if d['text_chars']==0:
  for start in range(1,d['pages']+1,80):jobs.append((d,start,min(d['pages'],start+79)))
def run(job):
 d,a,b=job;print('START',d['id'],a,b,flush=True)
 p=subprocess.run([str(R/'scripts/ocr_pdf'),str(R/d['path']),str(R/'corpus/ocr'/d['id']),str(a),str(b)],capture_output=True,text=True)
 print('DONE',d['id'],a,b,p.returncode,p.stderr[:500],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(run,jobs))
for d in M:
 if d['text_chars']==0:
  folder=R/'corpus/ocr'/d['id'];pages=[(folder/f'{n:04d}.txt').read_text() if (folder/f'{n:04d}.txt').exists() else '' for n in range(1,d['pages']+1)]
  (R/'corpus'/(d['id']+'.txt')).write_text('\f'.join(pages)+'\f')
  with (R/'corpus'/(d['id']+'.jsonl')).open('w') as f:
   for i,t in enumerate(pages):f.write(json.dumps({'page':i+1,'text':t,'ocr':True},ensure_ascii=False)+'\n')
  d['ocr']=True;d['text_chars']=sum(len(p.strip()) for p in pages);d['blank_pages']=[i+1 for i,p in enumerate(pages) if len(p.strip())<40];d['ocr_pages_completed']=len(list(folder.glob('*.txt')))
(R/'corpus/manifest.json').write_text(json.dumps(M,indent=2,ensure_ascii=False))
