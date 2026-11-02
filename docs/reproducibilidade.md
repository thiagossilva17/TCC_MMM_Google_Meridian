# Reprodução independente

## Origem e ambiente

Este projeto usa apenas seus próprios dados, notebook e artefatos. A base oficial é sintética, com 40 GEOs, 156 semanas e 6.240 linhas. O raw conserva o SHA-256 `d9ee016f7cd21f5c90b50da10a794af91a372b69f881d3caa266edd41fdafbf6`. A única transformação do painel é remover o índice exportado após verificar sua sequência, converter `time` em data, ordenar por GEO/tempo e exportar sem índice.

O Meridian está fixado no commit `02111531f8661373aa7b6ba31c316c67d72d1dd2` (versão 2.1.0). `requirements.txt` inclui as restrições testadas em `constraints-tested.txt`; `requirements-temporal.txt` permite executar somente o complemento sem carregar TensorFlow/Meridian. Python testado: 3.12. Os metadados históricos em `data/metadata/` permanecem intactos; o ambiente desta validação está em [ambiente_validacao.json](proveniencia/ambiente_validacao.json).

## Ambiente local

```bash
git clone https://github.com/thiagossilva17/TCC_MMM_Google_Meridian.git
cd TCC_MMM_Google_Meridian
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Para somente a seção 08, instalar `requirements-temporal.txt` é suficiente. Nunca é necessário clonar os projetos históricos.

## Execução e preservação

```bash
# Executa apenas 08, preserva as primeiras 122 células e seus outputs:
python scripts/execute_notebook.py --mode temporal --engine inprocess

# Executa todas as seções em uma cópia isolada em validation_runs/:
python scripts/execute_notebook.py --mode full --engine inprocess

# Alternativa por kernel Jupyter, em ambientes que permitem sockets:
python scripts/execute_notebook.py --mode full --engine jupyter
```

O executor `inprocess` usa um novo processo Python com IPython, capturando stdout, tabelas e imagens. Não equivale à validação do frontend Jupyter ou Colab. O modo `full` copia o projeto para um diretório de validação, redefine `TCC_MMM_ROOT` e grava ali resultados, metadados e notebook executado. Assim, a reexecução não sobrescreve as evidências históricas versionadas. O caminho da cópia é impresso no final.

Para comparar uma execução integral com as tabelas preservadas:

```bash
python scripts/compare_runs.py validation_runs/IDENTIFICADOR_DA_EXECUCAO
```

Esse comando atualiza o relatório local de comparação. Tolera diferenças numéricas de ponto flutuante (`rtol=atol=1e-7`), mas confere ordem, rótulos, dimensões e valores. As tolerâncias não autorizam alterar valores da monografia.

A identificação da raiz usa `.tcc-mmm-root` ou a variável explícita `TCC_MMM_ROOT`. Não pressupõe que qualquer diretório atual seja a raiz, nem cria uma pasta de projeto antigo.

**Atenção operacional:** executar manualmente todas as células dentro do checkout principal reproduz os gravadores históricos, que escrevem em `outputs/` e `data/metadata/`. Para preservar a versão auditada, use o modo `full` isolado ou uma cópia descartável do checkout. O notebook publicado mantém os outputs históricos; os outputs novos da seção 08 são da execução atual.

## Google Colab

Abra uma sessão nova e execute a preparação:

```python
import os, subprocess, sys
from pathlib import Path
checkout = Path('/content/TCC_MMM_Google_Meridian')
if not checkout.exists():
    subprocess.run(['git','clone','https://github.com/thiagossilva17/TCC_MMM_Google_Meridian.git',str(checkout)],check=True)
os.chdir(checkout)
subprocess.run([sys.executable,'-m','pip','install','-r','requirements.txt'],check=True)
```

Se o runtime já importou versões incompatíveis, reinicie-o após a instalação. Em seguida:

```python
import os, subprocess, sys
os.chdir('/content/TCC_MMM_Google_Meridian')
subprocess.run([sys.executable,'scripts/execute_notebook.py','--mode','full','--engine','inprocess'],check=True)
```

O notebook pode ser aberto em [Colab](https://colab.research.google.com/github/thiagossilva17/TCC_MMM_Google_Meridian/blob/main/notebooks/01_EDA_COMPLETA.ipynb). Abrir um notebook por URL não clona seus dados: a preparação anterior é necessária. Para execução manual do notebook, defina `TCC_MMM_ROOT` para um checkout de trabalho e execute na ordem original.

Ao concluir, confira `outputs/logs/notebook_run_manifest.json` na cópia executada e `outputs/temporal_complement/logs/tc_execution_manifest.json`. Baixe `EDA_RESULTS.zip` e `TEMPORAL_COMPLEMENT_RESULTS.zip` da cópia. O primeiro ZIP é produzido antes da seção 08; o segundo identifica separadamente o complemento. A execução na interface real do Colab permanece pendente; estes comandos são instruções, não prova de execução nesse serviço.

## Verificação e navegação

- Texto acadêmico: `tcc/`; sete imagens em `tcc/figuras/` e origens em `tcc/controle_de_elementos.csv`.
- Histórico: `outputs/figures/`, `outputs/tables/`, `outputs/reports/`, `outputs/logs/` e `data/metadata/`.
- Complemento: `outputs/temporal_complement/`, com 15 CSVs, quatro figuras, relatório e manifesto.
- Snapshot original: `docs/proveniencia/notebook_original.json.gz`; permite recuperar todos os bytes do anexo. Não é notebook concorrente de pesquisa.
- Diferenças de infraestrutura: `docs/proveniencia/alteracoes_portabilidade.json`.

```bash
sha256sum data/raw/geo_all_channels.csv
python -m pytest -q
```

Os testes conferem hashes, preservação de capítulos/células, funções científicas por AST, navegação, dados, números editoriais e completude temporal. As datas de aquisição original, consolidação e migração não devem ser confundidas. Os registros antigos com nomes de projetos e caminhos de execução são proveniência, não dependências.
