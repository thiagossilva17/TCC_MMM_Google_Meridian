"""Regenerate only new planning artifacts. Run from any working directory."""
from pathlib import Path
import sys,json
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.planning import load_configs,validate_panel,aggregate_national,make_masks,temporal_support,digest


def main():
 c=load_configs(ROOT);p=validate_panel(pd.read_csv(ROOT/c['agregacao_nacional']['source']))
 if digest(ROOT/c['agregacao_nacional']['source'])!=c['agregacao_nacional']['source_sha256']:raise ValueError('Source checksum mismatch')
 nat=aggregate_national(p,c['agregacao_nacional']);nat.to_csv(ROOT/c['agregacao_nacional']['output'],index=False)
 geos=sorted(p.geo.unique());dates=sorted(p.time.unique());A,B,D=make_masks(geos,dates,c['validacao_holdout']['seed'])
 a=pd.DataFrame({'geo':np.repeat(geos,len(dates)),'time':np.tile(dates,len(geos)),'holdout':A.ravel()})
 b=pd.DataFrame({'time':dates,'holdout':B,'development':D})
 a.to_csv(ROOT/c['validacao_holdout']['A']['file'],index=False);b.to_csv(ROOT/c['validacao_holdout']['B']['file'],index=False)
 checks={}
 for x in c['temporal_specifications']['candidates']:
  checks[x['id']]={key:temporal_support(156,x['positions'],h) for key,h in [('A',A),('B',B),('B-development',B|D)] if key!='A' or x['model']=='GEO'}
  for key,test in checks[x['id']].items():
   if x['experiment_B'] or key=='A':assert test['full_rank'],(x['id'],key,test)
 assert (A.sum(axis=0)==8).all() and A.sum(axis=1).min()>=31 and A.sum(axis=1).max()<=32
 assert B.sum()==31 and not (B&D).any() and not B[[0,155]].any()
 paths=[c['agregacao_nacional']['source'],c['agregacao_nacional']['output'],c['validacao_holdout']['A']['file'],c['validacao_holdout']['B']['file']]
 manifest=dict(seed=c['validacao_holdout']['seed'],algorithm_ref='HOLDOUT-V1',geos=geos,dates=[str(pd.Timestamp(t).date()) for t in dates],A={'shape':list(A.shape),'test_cells':int(A.sum()),'test_by_geo':A.sum(axis=1).tolist(),'test_by_week':A.sum(axis=0).tolist()},B={'test_weeks':int(B.sum()),'development_weeks':int(D.sum()),'test_dates':[str(pd.Timestamp(t).date()) for t in np.array(dates)[B]],'development_dates':[str(pd.Timestamp(t).date()) for t in np.array(dates)[D]]},temporal_support=checks,sha256={p:digest(ROOT/p) for p in paths},status='masks_materialized; full temporal rank checked; runtime leakage gate pending',versions={'numpy':np.__version__,'pandas':pd.__version__})
 (ROOT/'configs/holdouts/holdout_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'A_test_cells':int(A.sum()),'B_test_weeks':int(B.sum()),'development_weeks':int(D.sum()),'national_shape':list(nat.shape),'rank_checks':checks},indent=2))


if __name__=='__main__':main()
