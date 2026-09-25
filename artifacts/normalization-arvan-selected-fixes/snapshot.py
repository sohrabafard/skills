"""Hold the selected content and tracked gate inputs without a commit."""
import hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2]
out=root/'artifacts/normalization-arvan-selected-fixes/held-snapshot.json'
roots=['skills/sohrab/alaa-input-normalization','skills/sohrab/caas-arvan-kuber','skills/sohrab/alaa-k8s-helm/scripts','scripts']
paths=sorted({p for d in roots for p in (root/d).rglob('*') if p.is_file() and '__pycache__' not in p.parts})
rows=[{'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
records=''.join(x['path']+'\0'+x['sha256']+'\n' for x in rows)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
diff=subprocess.check_output(['git','diff','--binary','HEAD','--',*roots],cwd=root)
data={'head':head,'digest':hashlib.sha256(records.encode()).hexdigest(),'tracked_diff_sha256':hashlib.sha256(diff).hexdigest(),'files':rows}
if '--check' in sys.argv:
 old=json.loads(out.read_text())
 ok=all(old[k]==data[k] for k in data)
 print('SNAPSHOT '+('PASS' if ok else 'CHANGED')+' '+data['digest'])
 sys.exit(0 if ok else 1)
data['observed_at']=datetime.now(timezone.utc).isoformat()
data['method']='SHA256 sorted repo-relative path NUL file SHA256 LF; HEAD and scoped tracked diff separately bound; workflow/evidence companions excluded'
out.write_text(json.dumps(data,indent=2)+'\n')
print('SNAPSHOT HELD '+data['digest']+' files='+str(len(rows)))
