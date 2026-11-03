from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.planning import load_configs


def render():
 c=load_configs(ROOT);rows=c['sensibilidades']['experiments']
 lines=['# Matriz experimental integrada','', 'Gerada de `configs/sensibilidades.yaml`; não editar valores manualmente. Todos os ajustes são futuros. Nove cenários essenciais; uma linha pareada envolve dois modelos. Os demais cenários são ampliados/condicionais, não uma busca fatorial obrigatória.','', '| ID | Família | Modelo | Referência | Prioridade | Custo | Essencial | Estado |','|---|---|---|---|---|---|---|---|']
 for e in rows:lines.append('| '+' | '.join(str(e[k]) for k in ['id','family','model','reference','priority','cost','essential','status'])+' |')
 for e in rows:
  lines+=['',f"## {e['id']}",'']
  for k in ['hypothesis','alternative','factor','fixed','data_ref','mask_ref','development_ref','estimand','metrics_ref','diagnostics_ref','depends_on','eligibility']:
   val=json.dumps(e[k],ensure_ascii=False,sort_keys=True) if isinstance(e[k],(dict,list)) else str(e[k]);lines.append(f'- **{k}**: {val}')
 return '\n'.join(lines)+'\n'


if __name__=='__main__':(ROOT/'docs/MATRIZ_EXPERIMENTAL.md').write_text(render())
