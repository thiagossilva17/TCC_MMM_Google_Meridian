"""Exporta SVGs técnicos sem recalcular análises e registra proveniência."""
from pathlib import Path
import hashlib, csv, json
import cairosvg
ROOT=Path(__file__).resolve().parents[1]
FIGURES=[('populacao_kpi','geo/population_kpi.svg','fig01_populacao_kpi.png'),('decomposicao_bruta','geo/variance_decomposition.svg','fig02_decomposicao_bruta.png'),('geo_time','geo/geo_time_r2.svg','fig03_geo_time.png'),('channel2_calendario','media_geo/Channel2_impression_pc_geo_time.svg','fig04_channel2_calendario.png'),('channel3_calendario','media_geo/Channel3_impression_pc_geo_time.svg','fig05_channel3_calendario.png'),('correlacao_residual','relationships/correlation_two_way.svg','fig06_correlacao_residual.png'),('stl','temporal/kpi_stl_52.svg','fig07_stl.png')]
TABLES=[('integridade_painel',['data_audit.csv'],3),('variancia',['within_between_variance.csv','geo_time_r2.csv','geo_time_r2_per_capita.csv'],4),('atividade',['activity_intensity_summary.csv','channel_summary.csv'],4),('correlacoes_escalas',['substantive_pair_comparison.csv','predictor_kpi_comparison.csv'],4),('sintese_metodologica',[],4)]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=[]
 for i,(key,source,name) in enumerate(FIGURES,1):
  src=ROOT/'outputs/figures'/source;dest=ROOT/'tcc/figuras'/name
  cairosvg.svg2png(url=str(src),write_to=str(dest),scale=2)
  rows.append(dict(element_id='fig:'+key,tipo='figura',numero_atual=i,titulo=key,capitulo=4,origem_tecnica=str(src.relative_to(ROOT)),caminho_editorial=str(dest.relative_to(ROOT)),status='convertida; conferencia_visual_registrada_na_auditoria',hash_origem=digest(src),hash_destino=digest(dest),metodo_de_obtencao='CairoSVG 2.8.2; escala 2; sem recalculo',observacoes='Original SVG preservado; sem mudança de título, eixo ou valores'))
 for i,(key,names,chapter) in enumerate(TABLES,1):
  srcs=[ROOT/'outputs/tables'/n for n in names];dest=ROOT/('tcc/03_material_e_metodos.md' if chapter==3 else 'tcc/04_resultados_eda.md')
  rows.append(dict(element_id='tab:'+key,tipo='tabela',numero_atual=i,titulo=key,capitulo=chapter,origem_tecnica=';'.join(str(s.relative_to(ROOT)) for s in srcs) if srcs else str(dest.relative_to(ROOT)),caminho_editorial=str(dest.relative_to(ROOT)),status='evidencias_identificadas' if srcs else 'sintese_autoral',hash_origem=json.dumps({str(s.relative_to(ROOT)):digest(s) for s in srcs}) if srcs else digest(dest),hash_destino=digest(dest),metodo_de_obtencao='tabela editorial preservada' if srcs else 'sintese academica; nao e output numerico direto',observacoes='Conferência numérica no teste editorial; Tabela 5 é síntese interpretativa'))
 with (ROOT/'tcc/controle_de_elementos.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
 print('Sete figuras convertidas e doze elementos registrados.')
if __name__=='__main__':main()
