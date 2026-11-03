from pathlib import Path
import ast,gzip,hashlib,json,re,csv
import numpy as np
import pandas as pd
import nbformat
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def notebook():return json.loads((ROOT/'notebooks/01_EDA_COMPLETA.ipynb').read_text())
def original():return json.loads(gzip.decompress((ROOT/'docs/proveniencia/notebook_original.json.gz').read_bytes()))

def test_original_cells_and_scientific_functions():
    old=original();new=notebook();changes=json.loads((ROOT/'docs/proveniencia/alteracoes_portabilidade.json').read_text());indices={r['index'] for r in changes}
    assert len(old['cells'])==122 and len(new['cells'])==136
    for i,a in enumerate(old['cells']):
        b=new['cells'][i]
        assert {k:v for k,v in a.items() if k!='source'}=={k:v for k,v in b.items() if k!='source'}
        if i not in indices:assert a==b
        if a['cell_type']=='code' and i not in [4,9]:assert a==b
    def functions(n):
        tree=ast.parse('\n'.join(''.join(c['source']) for c in n['cells'][:122] if c['cell_type']=='code'))
        return {x.name:ast.dump(x,include_attributes=False) for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name!='code_state'}
    assert functions(old)==functions(new)
    nbformat.validate(nbformat.read(ROOT/'notebooks/01_EDA_COMPLETA.ipynb',as_version=4))

def test_migrated_hashes():
    for row in json.loads((ROOT/'docs/proveniencia/manifesto_migracao.json').read_text()):
        if row['destination'] in {'tcc/03_material_e_metodos.md','tcc/04_resultados_eda.md'}:
            # Authorized scientific edits now checked section-by-section below.
            continue
        assert digest(ROOT/row['destination'])==row['sha256_final'],row['destination']
    historical=json.loads((ROOT/'outputs/logs/run_manifest.json').read_text())
    for stage in historical['stages'].values():
        for path,h in stage.get('files',{}).items():
            if (ROOT/path).exists():assert digest(ROOT/path)==h,path

def test_academic_preservation():
    inv=json.loads((ROOT/'docs/proveniencia/inventario_inicial.json').read_text())
    hashes={r['name']:r['sha256'] for r in inv['attachments']}
    mapping={'01_Introducao_Revisada_ABNT(4).md':'tcc/01_introducao.md','02_Referencial_Teorico_Revisado_ABNT(4).md':'tcc/02_referencial_teorico.md','03_Referencias_Bibliograficas_Revisadas_ABNT(4).md':'tcc/referencias.md'}
    for name,path in mapping.items():assert digest(ROOT/path)==hashes[name]
    # Preserve initial provenance; replace obsolete whole-chapter freeze with scoped hashes.
    manifest=json.loads((ROOT/'docs/planejamento/preservation_manifest.json').read_text())
    for path,record in manifest['academic'].items():
        chunks=re.split(r'(?=^## \d+\.\d+ )',(ROOT/path).read_text(),flags=re.M)
        parts={re.match(r'## (\d+\.\d+)',v)[1] if v.startswith('## ') else 'header':hashlib.sha256(v.encode()).hexdigest() for v in chunks}
        assert parts.keys()==record['initial_sections'].keys()
        for key,value in record['initial_sections'].items():
            if key not in record['allowed_sections']:assert parts[key]==value,(path,key)
        # First-task text must survive the second-task revision exactly.
        for key in (['3.3'] if '/03_' in path else parts.keys()):
            assert parts[key]==record['after_task1_sections'][key],(path,key)


def test_data_contract_and_transformations():
    assert digest(ROOT/'data/raw/geo_all_channels.csv')=='d9ee016f7cd21f5c90b50da10a794af91a372b69f881d3caa266edd41fdafbf6'
    raw=pd.read_csv(ROOT/'data/raw/geo_all_channels.csv');p=pd.read_csv(ROOT/'data/processed/geo_time_panel.csv',parse_dates=['time'])
    assert raw.shape==(6240,20) and p.shape==(6240,19)
    assert np.array_equal(raw['Unnamed: 0'],np.arange(6240))
    raw=raw.drop(columns='Unnamed: 0');raw.time=pd.to_datetime(raw.time)
    pd.testing.assert_frame_equal(p,raw.sort_values(['geo','time']).reset_index(drop=True),rtol=1e-12,atol=1e-9)
    assert p.geo.nunique()==40 and p.time.nunique()==156
    assert not p.duplicated(['geo','time']).any() and not p.isna().any().any()
    assert (p.groupby('geo').time.diff().dropna()==pd.Timedelta(days=7)).all()

def test_editorial_figures_and_tables():
    elements=list(csv.DictReader((ROOT/'tcc/controle_de_elementos.csv').open()))
    assert len(elements)==12 and sum(x['tipo']=='figura' for x in elements)==7
    for row in elements:
        assert (ROOT/row['caminho_editorial']).exists()
        if row['caminho_editorial'] in {'tcc/03_material_e_metodos.md','tcc/04_resultados_eda.md'}:
            record=json.loads((ROOT/'docs/planejamento/preservation_manifest.json').read_text())['academic'][row['caminho_editorial']]
            assert row['hash_destino']==record['initial_sha256']
            tables=re.findall(r'^\|.*(?:\n\|.*)*',(ROOT/row['caminho_editorial']).read_text(),flags=re.M)
            assert [hashlib.sha256(t.encode()).hexdigest() for t in tables]==record['initial_table_hashes']
        else:
            assert digest(ROOT/row['caminho_editorial'])==row['hash_destino']
        if row['tipo']=='figura':assert digest(ROOT/row['origem_tecnica'])==row['hash_origem']
    raw=pd.read_csv(ROOT/'outputs/tables/within_between_variance.csv').set_index('variable')
    pc=pd.read_csv(ROOT/'outputs/tables/geo_time_r2_per_capita.csv').set_index('variable')
    text=(ROOT/'tcc/04_resultados_eda.md').read_text()
    for line in text.splitlines():
        if not re.match(r'\| `(conversions|Channel[0-4])` \|',line):continue
        parts=[s.strip() for s in line.split('|')[1:-1]]
        name=parts[0].strip('`');numbers=[float(s.replace(',','.')) for s in parts[1:]]
        if len(numbers)!=5:continue
        var=name if name=='conversions' else name+'_impression'
        expected=[raw.loc[var,'between_share'],raw.loc[var,'within_share'],raw.loc[var,'residual_geo_time_share'],pc.loc[var,'between_share'],pc.loc[var,'residual_geo_time_share']]
        np.testing.assert_allclose(numbers,np.array(expected)*100,atol=.00501,rtol=0)
    summary=pd.read_csv(ROOT/'outputs/tables/channel_summary.csv').set_index('channel');activity=pd.read_csv(ROOT/'outputs/tables/activity_intensity_summary.csv').set_index('channel')
    for line in text.splitlines():
        if not re.match(r'\| `Channel[0-4]` \|',line):continue
        parts=[s.strip() for s in line.split('|')[1:-1]]
        if len(parts)!=5:continue
        ch=parts[0].strip('`');nums=[float(s.replace(',','.')) for s in parts[1:]]
        expected=[summary.loc[ch,'spend_share']*100,summary.loc[ch,'zero_share']*100,activity.loc[ch,'max_zero_streak'],activity.loc[ch,'within_variance_activity_share']*100]
        np.testing.assert_allclose(nums,expected,atol=.00501,rtol=0)
    pairs=pd.read_csv(ROOT/'outputs/tables/substantive_pair_comparison.csv')
    row=pairs.query("left=='Channel2_impression' and right=='Channel3_impression' and method=='pearson'").iloc[0]
    np.testing.assert_allclose(row[['national','overall','within','two_way']].astype(float),[.700,.524,.504,.451],atol=.00051,rtol=0)
    kpi=pd.read_csv(ROOT/'outputs/tables/predictor_kpi_comparison.csv').query("right=='Channel3_impression' and method=='pearson'").set_index('level').correlation
    for level,val,tol in [('national',-.12,.005),('overall',.47,.005),('within',-.05,.005),('two_way',-.046,.0005)]:assert abs(kpi[level]-val)<=tol

def test_navigation_and_independence():
    for f in list((ROOT/'tcc').glob('*.md'))+list((ROOT/'docs').glob('*.md'))+[ROOT/'README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
            if target.startswith(('http','#','mailto:')):continue
            assert (f.parent/target.split('#')[0]).exists(),(f,target)
    for c in notebook()['cells']:
        src=''.join(c['source'])
        if c['cell_type']=='code':
            assert 'MMM_Google_Meridian_Project' not in src
            assert not re.search(r'from src|import src|sample_posterior\(',src)
        else:
            for target in re.findall(r'\]\(([^)]+)\)',src):
                if target.startswith('attachment:'):assert target.split(':',1)[1] in c.get('attachments',{}),target
                elif not target.startswith(('http','#','mailto:')):assert (ROOT/'notebooks'/target.split('#')[0]).exists(),target
    assert not (ROOT/'.gitmodules').exists()
    assert len(list((ROOT/'notebooks').glob('*.ipynb')))==1

def test_temporal_completeness_and_manifest():
    base=ROOT/'outputs/temporal_complement';manifest=json.loads((base/'logs/tc_execution_manifest.json').read_text())
    for name,h in manifest['files'].items():assert digest(ROOT/name)==h,name
    geo=pd.read_csv(base/'tables/tc_stationarity_geo.csv');nat=pd.read_csv(base/'tables/tc_stationarity_national.csv')
    assert len(geo)==480 and len(nat)==12 and geo.geo.nunique()==40
    assert geo.groupby(['geo','scale','test','regression']).size().eq(1).all()
    assert geo.query("test=='KPSS'").p_bound.isin(['p_ge_0.10','p_le_0.01','interpolated']).all()
    assert geo.p_value.between(0,1).all()
    assert geo.query("test=='ADF'").n_effective.lt(geo.query("test=='ADF'").n_input).all()
    media=pd.read_csv(base/'tables/tc_geo_media_persistence.csv')
    assert len(media)==40*5*3*6 and (media.pairs==media.n-media.lag).all()
    assert media.acf.dropna().between(-1,1).all()
    for ch,streak in [('Channel2',27),('Channel3',2)]:assert media.query('channel==@ch and measure=="impression"').max_zero_streak.max()==streak
    trend=pd.read_csv(base/'tables/tc_geo_trend_profile.csv');assert (trend.direction==trend.pc_direction).all()
    raw=pd.read_csv(ROOT/'data/processed/geo_time_panel.csv')
    delta=raw.groupby('time').conversions.sum().iloc[-26:].mean()-raw.groupby('time').conversions.sum().iloc[:26].mean()
    assert np.isclose(trend.delta_last_first26.sum(),delta)


def test_stable_function_fingerprint_detects_changes():
    import types,inspect
    cell=ast.parse(''.join(notebook()['cells'][9]['source']))
    node=next(x for x in cell.body if isinstance(x,ast.FunctionDef) and x.name=='code_state')
    ns={'__name__':'audit_test','types':types,'inspect':inspect,'hashlib':hashlib,'json':json}
    exec(compile(ast.Module(body=[node],type_ignores=[]),'<audit>','exec'),ns)
    exec('def probe(x):\n    return x * 2 + 1',ns)
    before=ns['code_state']()
    for i in range(10000):ns['probe'](i)
    assert before==ns['code_state']()
    exec('def probe(x):\n    return x * 3 + 1',ns)
    assert before['probe']!=ns['code_state']()['probe']


def test_png_files_decode_completely():
    from PIL import Image
    images=list((ROOT/'tcc/figuras').glob('*.png'))+list((ROOT/'outputs/temporal_complement/figures').glob('*.png'))
    assert len(images)==11
    for path in images:
        with Image.open(path) as image:
            image.load()
            assert image.width>900 and image.height>300
