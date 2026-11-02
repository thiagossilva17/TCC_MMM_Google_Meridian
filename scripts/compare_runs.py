"""Compara tabelas de execução isolada com artefatos preservados."""
from pathlib import Path
import argparse,json
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def compare(run):
 rows=[]
 for f in sorted((ROOT/'outputs/tables').glob('*.csv')):
  other=run/'outputs/tables'/f.name
  if not other.exists():rows.append({'file':f.name,'status':'missing'});continue
  try:
   a=pd.read_csv(f);b=pd.read_csv(other)
   pd.testing.assert_frame_equal(a,b,check_dtype=False,check_exact=False,rtol=1e-7,atol=1e-7)
   rows.append({'file':f.name,'status':'equivalent','rows':len(a),'byte_equal':f.read_bytes()==other.read_bytes()})
  except Exception as e:rows.append({'file':f.name,'status':'different','detail':str(e)[:1800]})
 return rows
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('run',type=Path);args=ap.parse_args();rows=compare(args.run.resolve())
 out=ROOT/'docs/proveniencia/comparacao_reexecucao.json';out.write_text(json.dumps({'rtol':1e-7,'atol':1e-7,'tables':rows},ensure_ascii=False,indent=2))
 print(pd.Series([r['status'] for r in rows]).value_counts().to_string())
 for r in rows:
  if r['status']!='equivalent':print(r)
