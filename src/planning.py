"""Preparation and diagnostics only; no model fitting and no historical writes."""
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
import yaml


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_configs(root):
    names=['temporal_specifications','agregacao_nacional','validacao_holdout','diagnosticos_posteriores','sensibilidades']
    return {n:yaml.safe_load((Path(root)/'configs'/f'{n}.yaml').read_text()) for n in names if (Path(root)/'configs'/f'{n}.yaml').exists()}


def validate_panel(panel):
    p=panel.copy();p['time']=pd.to_datetime(p.time)
    if p.duplicated(['geo','time']).any() or p.isna().any().any():raise ValueError('Duplicate key or missing values')
    if p.geo.nunique()!=40 or p.time.nunique()!=156 or len(p)!=6240:raise ValueError('Expected 40 x 156 panel')
    p=p.sort_values(['geo','time']).reset_index(drop=True)
    if not p.groupby('geo').time.diff().dropna().eq(pd.Timedelta(days=7)).all():raise ValueError('Broken calendar')
    if not p.groupby('geo').population.nunique().eq(1).all() or not p.population.gt(0).all():raise ValueError('Invalid population')
    if not np.isfinite(p.select_dtypes('number')).all().all():raise ValueError('Nonfinite data')
    return p


def aggregate_national(panel,config):
    p=validate_panel(panel);op=config['operators'];groups=p.groupby('time',sort=True)
    result=groups[op['sum']].sum()
    population=p.groupby('geo').population.first().sum()
    for col in op['population_weighted_mean']:
        result[col]=(p[col]*p.population).groupby(p.time).sum()/population
    result['population']=population
    result.insert(0,'geo','National')
    for col in op['sum']:
        if not np.isclose(result[col].sum(),p[col].sum(),rtol=config['conservation_rtol'],atol=config['conservation_atol']):raise ValueError(f'Conservation failed: {col}')
    return result.reset_index()


def make_masks(geos,dates,seed):
    geos=sorted(geos);dates=pd.DatetimeIndex(sorted(dates));G,T=len(geos),len(dates)
    if (G,T)!=(40,156):raise ValueError('Expected 40 x 156 coordinates')
    rng=np.random.default_rng(seed);go=rng.permutation(G);to=rng.permutation(T)
    A=np.zeros((G,T),dtype=bool)
    for j,t in enumerate(to): A[go[(8*j+np.arange(8))%G],t]=True
    rng=np.random.default_rng(seed+1);B=np.zeros(T,dtype=bool)
    for start in range(0,155,5):B[int(rng.choice(np.arange(start+1,start+4)))]=True
    rng=np.random.default_rng(seed+2);D=np.zeros(T,dtype=bool)
    for start in range(0,150,10):
        choices=np.arange(start+1,min(start+9,T-1));choices=choices[~B[choices]]
        D[int(rng.choice(choices))]=True
    return A,B,D


def temporal_weights(T,positions):
    k=np.asarray(positions)
    if len(k)==0 or len(np.unique(k))!=len(k) or np.any(np.diff(k)<=0) or k.min()<0 or k.max()>=T:raise ValueError('Invalid knots')
    if len(k)==1:return np.ones((T,1))
    return np.stack([np.interp(np.arange(T),k,np.eye(len(k))[i]) for i in range(len(k))],axis=1)


def temporal_support(T,positions,holdout):
    W=temporal_weights(T,positions);h=np.asarray(holdout)
    if h.dtype!=bool or h.shape not in [(T,),(40,T)]:raise ValueError('Invalid boolean mask')
    train=~h if h.ndim==1 else (~h).any(axis=0)
    rank=int(np.linalg.matrix_rank(W[train]))
    return {'rank':rank,'knots':len(positions),'full_rank':rank==len(positions),'min_column_training_mass':float(W[train].sum(axis=0).min())}


def masked_kpi(y,holdout):
    """Isolate truth outside model input; this does not itself validate Meridian."""
    y=np.asarray(y,float);h=np.asarray(holdout)
    if y.ndim!=2 or h.shape!=y.shape or h.dtype!=bool:raise ValueError('Expected matched GEO x time boolean mask')
    if not np.isfinite(y[~h]).all() or not (~h).any(axis=1).all():raise ValueError('No valid training observations')
    means=np.sum(np.where(h,0,y),axis=1)/(~h).sum(axis=1)
    return np.where(h,means[:,None],y)


def metrics(y,pred):
    y=np.asarray(y,float);pred=np.asarray(pred,float)
    if y.shape!=pred.shape or not y.size or not np.isfinite(y).all() or not np.isfinite(pred).all():raise ValueError('Invalid aligned observations')
    e=y-pred;den=np.abs(y).sum();sst=np.square(y-y.mean()).sum()
    return dict(mae=float(np.abs(e).mean()),rmse=float(np.sqrt(np.square(e).mean())),wmape_pct=float(100*np.abs(e).sum()/den) if den>0 else None,r2=float(1-np.square(e).sum()/sst) if sst>0 else None)


def residuals(y,expected):
    y=np.asarray(y,float);expected=np.asarray(expected,float)
    if y.shape!=expected.shape:raise ValueError('Misaligned residuals')
    return y-expected


def aggregate_draws(draws):
    """Input chain x draw x geo x time; retain joint chain/draw coordinates."""
    a=np.asarray(draws,float)
    if a.ndim!=4 or not np.isfinite(a).all():raise ValueError('Expected finite chain x draw x geo x time')
    return a.sum(axis=2)


def predictive_intervals(draws,y,level=.9):
    a=np.asarray(draws,float);y=np.asarray(y,float)
    if a.ndim!=3 or a.shape[-1]!=y.size or not 0<level<1 or not np.isfinite(a).all() or not np.isfinite(y).all():raise ValueError('Invalid predictive input')
    low,high=np.quantile(a,[(1-level)/2,(1+level)/2],axis=(0,1))
    return {'low':low,'high':high,'coverage':float(np.mean((y>=low)&(y<=high))),'width':float(np.mean(high-low))}


def calendar_acf(dates,values,lags):
    """Descriptive pairwise correlation at true weekly lags, no calendar compression."""
    idx=pd.DatetimeIndex(dates);x=np.asarray(values,float)
    if idx.has_duplicates or not idx.is_monotonic_increasing or len(idx)!=len(x):raise ValueError('Invalid dates')
    full=pd.date_range(idx.min(),idx.max(),freq='7D')
    if not idx.isin(full).all():raise ValueError('Off-grid date')
    s=pd.Series(x,index=idx).reindex(full).to_numpy();rows=[]
    for lag in lags:
        if lag<=0 or lag>=len(s):raise ValueError('Invalid lag')
        a,b=s[:-lag],s[lag:];ok=np.isfinite(a)&np.isfinite(b);n=int(ok.sum())
        value=float(np.corrcoef(a[ok],b[ok])[0,1]) if n>=3 and np.ptp(a[ok])>0 and np.ptp(b[ok])>0 else None
        rows.append(dict(lag=lag,pairs=n,correlation=value))
    return rows


def contribution_change(reference,alternative,min_abs_reference):
    if min_abs_reference<=0:raise ValueError('Specify substantive positive denominator floor')
    a,b=np.asarray(reference,float),np.asarray(alternative,float)
    if not a.size or not b.size or not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('Invalid draws')
    delta=float(b.mean()-a.mean());den=abs(a.mean())
    return dict(reference_mean=float(a.mean()),alternative_mean=float(b.mean()),reference_median=float(np.median(a)),alternative_median=float(np.median(b)),difference=delta,relative_pct=100*delta/den if den>=min_abs_reference else None,reference_interval=np.quantile(a,[.05,.95]).tolist(),alternative_interval=np.quantile(b,[.05,.95]).tolist())


def classify_mcmc(rhat=None,bulk_ess=None,tail_ess=None,divergences=None):
    if any(v is None for v in [rhat,bulk_ess,tail_ess,divergences]):return 'INCONCLUSIVO'
    vals=np.array([rhat,bulk_ess,tail_ess,divergences],float)
    if not np.isfinite(vals).all():return 'INCONCLUSIVO'
    if divergences>0 or rhat>1.01:return 'PROBLEMATICO'
    if min(bulk_ess,tail_ess)<400:return 'REQUER_INVESTIGACAO'
    return 'SATISFATORIO'
