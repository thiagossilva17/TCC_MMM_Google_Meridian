from pathlib import Path
import sys,json,importlib.util
import numpy as np
import pandas as pd
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.planning import *


@pytest.fixture
def config():return load_configs(ROOT)


@pytest.fixture
def panel():return pd.read_csv(ROOT/'data/processed/geo_time_panel.csv')


def test_protected_files():
    m=json.loads((ROOT/'docs/planejamento/preservation_manifest.json').read_text())
    for path,sha in m['protected_files'].items():assert digest(ROOT/path)==sha,path


def test_aggregation_conservation_and_population(config,panel):
    before=panel.copy(deep=True);a=aggregate_national(panel,config['agregacao_nacional'])
    assert a.shape==(156,18) and a.time.is_unique
    for col in config['agregacao_nacional']['operators']['sum']:
        np.testing.assert_allclose(a.set_index('time')[col],panel.groupby('time')[col].sum(),rtol=1e-12)
    assert a.population.nunique()==1
    assert a.population.iloc[0]==panel.groupby('geo').population.first().sum()
    assert 'revenue_per_conversion' not in a
    for col in config['agregacao_nacional']['operators']['population_weighted_mean']:
        first=panel[panel.time==panel.time.min()]
        assert a[col].iloc[0]==pytest.approx(np.average(first[col],weights=first.population))
    pd.testing.assert_frame_equal(before,panel)
    saved=pd.read_csv(ROOT/'data/processed/national_weekly.csv',parse_dates=['time'])
    pd.testing.assert_frame_equal(a,saved,check_dtype=False,rtol=1e-12)


@pytest.mark.parametrize('failure',['duplicate','missing','population','nonfinite','date'])
def test_invalid_panel(panel,failure):
    p=panel.copy()
    if failure=='duplicate':p=pd.concat([p,p.iloc[:1]])
    if failure=='missing':p=p.iloc[1:]
    if failure=='population':p.loc[0,'population']*=2
    if failure=='nonfinite':p.loc[0,'conversions']=np.inf
    if failure=='date':p.loc[0,'time']='2020-01-01'
    with pytest.raises(ValueError):validate_panel(p)


def test_masks_materialized_invariant(config,panel):
    p=validate_panel(panel);seed=config['validacao_holdout']['seed'];args=(p.geo.unique(),p.time.unique(),seed)
    A,B,D=make_masks(*args)
    for x,y in zip((A,B,D),make_masks(*args)):np.testing.assert_array_equal(x,y)
    assert A.dtype==bool and A.shape==(40,156) and A.sum()==1248
    assert (A.sum(0)==8).all() and set(A.sum(1))=={31,32}
    assert B.sum()==31 and D.sum()==15 and not (B&D).any()
    assert not B[0] and not B[-1] and not (B[1:]&B[:-1]).any()
    saved=pd.read_csv(ROOT/config['validacao_holdout']['A']['file'])
    assert saved.geo.drop_duplicates().tolist()==sorted(p.geo.unique())
    np.testing.assert_array_equal(saved.holdout.to_numpy().reshape(40,156),A)
    b=pd.read_csv(ROOT/config['validacao_holdout']['B']['file']);np.testing.assert_array_equal(b.holdout,B);np.testing.assert_array_equal(b.development,D)
    assert b.time.tolist()==[str(pd.Timestamp(t).date()) for t in sorted(p.time.unique())]
    m=json.loads((ROOT/'configs/holdouts/holdout_manifest.json').read_text())
    for path,sha in m['sha256'].items():assert digest(ROOT/path)==sha
    # Shuffle coordinates and perturb KPI: selection remains coordinate-only.
    shuffled=p.sample(frac=1,random_state=4);shuffled.conversions=0
    for x,y in zip((A,B,D),make_masks(shuffled.geo.unique(),shuffled.time.unique(),seed)):np.testing.assert_array_equal(x,y)


def test_rank_and_weights(config,panel):
    p=validate_panel(panel);A,B,D=make_masks(p.geo.unique(),p.time.unique(),config['validacao_holdout']['seed'])
    for c in config['temporal_specifications']['candidates']:
        W=temporal_weights(156,c['positions']);np.testing.assert_allclose(W.sum(1),1)
        assert np.all(W>=0)
        for h in [B,B|D]:assert temporal_support(156,c['positions'],h)['full_rank']==c['experiment_B']
    assert temporal_support(156,list(range(156)),A)['full_rank']
    # Verify full additive time+geo design support for A, independent of KPI.
    W=temporal_weights(156,list(range(156)));g,t=np.where(~A)
    design=np.column_stack([W[t],np.eye(40)[g,1:]])
    assert np.linalg.matrix_rank(design)==195


def test_configs_references_api_and_states(config):
    assert len(config)==5
    ids=[x['id'] for x in config.values()];assert len(ids)==len(set(ids))
    t=config['temporal_specifications'];s=config['sensibilidades'];a=json.loads((ROOT/'docs/planejamento/meridian_api_audit.json').read_text())
    assert set(t['model_spec'])<=set(a['fields']['ModelSpec'])
    assert set(t['priors']['parameters'])<=set(a['fields']['PriorDistribution'])
    assert t['aks']['knots'] is None and t['aks']['enable_aks']
    assert all(not x['enable_aks'] and len(x['positions'])==x['knots'] for x in t['candidates'])
    candidates={x['id'] for x in t['candidates']}|{t['aks']['id']};exps=s['experiments'];eids={e['id'] for e in exps}
    assert len(eids)==len(exps)
    for e in exps:
        assert e['status'] in ['not_executed','conditional']
        assert e['reference'] is None or e['reference'] in eids
        assert set(e['depends_on'])<=eids
        assert e['diagnostics_ref']==config['diagnosticos_posteriores']['id']
        alt=e['alternative']
        if 'temporal' in alt:assert alt['temporal'] in candidates
        if 'model_spec_patch' in alt:assert set(alt['model_spec_patch'])<=set(a['fields']['ModelSpec'])
        if 'prior_patch' in alt:assert set(alt['prior_patch'])<=set(a['fields']['PriorDistribution'])
    assert config['validacao_holdout']['temporal_ref']==t['id']
    assert config['validacao_holdout']['aggregation_ref']==config['agregacao_nacional']['id']
    assert config['diagnosticos_posteriores']['holdout_ref']==config['validacao_holdout']['id']
    assert s['temporal_ref']==t['id'] and s['holdout_ref']==config['validacao_holdout']['id']
    assert s['diagnostics_ref']==config['diagnosticos_posteriores']['id']
    assert s['reference_prior']==t['priors']['id']
    for e in exps:
        assert e['data_ref']==config['agregacao_nacional']['id']
        assert e['mask_ref'] in ['HOLDOUT-A','HOLDOUT-B']
        assert e['metrics_ref']==s['stability']['id']


def test_masked_kpi_invariance():
    y=np.arange(24,dtype=float).reshape(3,8);h=np.zeros_like(y,bool);h[:,[1,5]]=True
    a=masked_kpi(y,h);changed=y.copy();changed[h]=1e100
    np.testing.assert_array_equal(a,masked_kpi(changed,h))
    np.testing.assert_array_equal(a[~h],y[~h])
    with pytest.raises(ValueError):masked_kpi(y,np.ones_like(h))
    with pytest.raises(ValueError):masked_kpi(y,h.astype(int))


def test_metrics_hand_computation_and_degenerate():
    m=metrics([1,2,3],[2,2,1]);assert m['mae']==1;assert m['rmse']==pytest.approx(np.sqrt(5/3));assert m['wmape_pct']==50;assert m['r2']==-1.5
    assert metrics([0,0],[1,1])['wmape_pct'] is None
    assert metrics([1,1],[0,0])['r2'] is None
    with pytest.raises(ValueError):metrics([1],[1,2])
    with pytest.raises(ValueError):metrics([np.nan],[1])
    np.testing.assert_array_equal(residuals([1,3],[2,2]),[-1,1])


def test_draw_aggregation_quantiles_preserve_dependence():
    # Perfectly anticorrelated geos: sums constant, sum of marginal limits wrong.
    d=np.array([[[[0.],[10.]],[[10.],[0.]]]])
    a=aggregate_draws(d);np.testing.assert_array_equal(a,[[[10.],[10.]]])
    q=predictive_intervals(a,[10.]);assert q['coverage']==1 and q['width']==0
    assert np.quantile(d,.05,axis=(0,1)).sum()<q['low'][0]
    with pytest.raises(ValueError):aggregate_draws(np.zeros((2,3)))


def test_calendar_gaps_are_not_compressed():
    dates=pd.to_datetime(['2024-01-01','2024-01-08','2024-01-22','2024-01-29'])
    rows=calendar_acf(dates,[1,2,4,5],[1,2]);assert rows[0]['pairs']==2;assert rows[1]['pairs']==1
    assert rows[0]['correlation'] is None
    complete=calendar_acf(pd.date_range('2024-01-01',periods=8,freq='7D'),np.arange(8),[1])[0]
    assert complete['correlation']==pytest.approx(1)
    with pytest.raises(ValueError):calendar_acf(dates[::-1],[1,2,3,4],[1])
    with pytest.raises(ValueError):calendar_acf(dates,[1,2,3,4],[0])


def test_contribution_denominator_and_mcmc_states():
    assert contribution_change([0,0],[1,2],.1)['relative_pct'] is None
    assert contribution_change([2,2],[3,3],.1)['relative_pct']==50
    assert classify_mcmc()=='INCONCLUSIVO'
    assert classify_mcmc(1.,500,500,0)=='SATISFATORIO'
    assert classify_mcmc(1.02,500,500,0)=='PROBLEMATICO'
    assert classify_mcmc(1.,500,500,1)=='PROBLEMATICO'
    assert classify_mcmc(1.,200,500,0)=='REQUER_INVESTIGACAO'
    assert classify_mcmc(np.nan,500,500,0)=='INCONCLUSIVO'


def test_matrix_is_generated():
    spec=importlib.util.spec_from_file_location('matrix',ROOT/'scripts/render_experiment_matrix.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    assert (ROOT/'docs/MATRIZ_EXPERIMENTAL.md').read_text()==module.render()
