from pathlib import Path
import subprocess, json, re, hashlib, concurrent.futures, os, shutil
ROOT=Path(__file__).resolve().parents[1]
def poppler_binary(name):
 configured=os.environ.get('POPPLER_BIN')
 if configured:
  candidate=Path(configured)/name
  if candidate.is_file():return str(candidate)
  raise SystemExit(f'{name} is missing from POPPLER_BIN: {configured}')
 installed=shutil.which(name)
 if installed:return installed
 bundled=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin'/name
 if bundled.is_file():return str(bundled)
 raise SystemExit(f'Install Poppler and put {name} on PATH, or set POPPLER_BIN.')
PDFTOTEXT=poppler_binary('pdftotext')
PDFINFO=poppler_binary('pdfinfo')
OUT=ROOT/'corpus'; OUT.mkdir(exist_ok=True)
def extract(path):
 rel=str(path.relative_to(ROOT)); slug=re.sub('[^a-z0-9]+','-',path.stem.lower()).strip('-')
 dest=OUT/(slug+'.txt')
 subprocess.run([PDFTOTEXT,'-layout',str(path),str(dest)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 raw=dest.read_text(errors='replace'); pages=raw.split('\f')
 if pages and not pages[-1].strip(): pages.pop()
 info=subprocess.run([PDFINFO,str(path)],capture_output=True,text=True).stdout
 count=re.search(r'^Pages:\s*(\d+)',info,re.M)
 count=int(count.group(1)) if count else len(pages)
 pages += ['']*max(0,count-len(pages))
 cat=path.parent.name.strip(); stats={'id':slug,'title':path.stem,'path':rel,'category':cat,'pages':count,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'text_chars':sum(len(p.strip()) for p in pages),'blank_pages':[i+1 for i,p in enumerate(pages) if len(p.strip())<40]}
 with (OUT/(slug+'.jsonl')).open('w') as f:
  for i,p in enumerate(pages):f.write(json.dumps({'page':i+1,'text':p},ensure_ascii=False)+'\n')
 return stats
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: data=list(pool.map(extract,sorted((ROOT/'inputs').rglob('*.pdf'))))
(OUT/'manifest.json').write_text(json.dumps(data,indent=2,ensure_ascii=False))
for d in data: print(d['id'],d['pages'],d['text_chars'],len(d['blank_pages']))
print('TOTAL',len(data),sum(d['pages'] for d in data),'pages')
