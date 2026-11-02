# TCC_MMM_Google_Meridian

## O que o total nacional não conta

**Marketing Mix Modeling Bayesiano com Google Meridian: comparação entre a informação geográfica e a agregação nacional.**

Este TCC investiga em que medida preservar a estrutura GEO × tempo altera estimativas, incerteza e avaliação de um MMM, comparado à série nacional. A justificativa é simples: o mesmo total pode combinar trajetórias locais diferentes. Mais linhas, porém, não garantem melhor identificação causal. A comparação dos modelos ainda será executada.

A pesquisa utiliza a **base sintética oficial do Google Meridian**: 40 mercados, 156 semanas, 6.240 observações; cinco canais pagos com impressões e gastos, conversões, população, mídia orgânica, controles, promoção e receita por conversão. Os GEOs não representam cidades identificáveis, e os dados não são campanhas comerciais reais. O Meridian oferece a estrutura Bayesiana hierárquica; esta entrega preserva a EDA e amplia seus diagnósticos temporais, sem estimação MMM.

## Três percursos

| Quero… | Começar por… |
|---|---|
| Ler a monografia | [Introdução](tcc/01_introducao.md), [referencial](tcc/02_referencial_teorico.md), [métodos](tcc/03_material_e_metodos.md), [resultados da EDA](tcc/04_resultados_eda.md) e [referências](tcc/referencias.md) |
| Reproduzir os cálculos | [Notebook único](notebooks/01_EDA_COMPLETA.ipynb) e [guia de reprodução](docs/reproducibilidade.md) |
| Entender o raciocínio | [Guia didático](docs/EDA_DIDACTIC_GUIDE.md), [diagnóstico temporal](docs/DIAGNOSTICO_TEMPORAL_COMPLEMENTAR.md) e [decisões](docs/decisoes_metodologicas.md) |

## Situação real

| Frente | Estado |
|---|---|
| EDA original | Concluída historicamente; outputs preservados |
| Migração | Arquivos centralizados e independência operacional verificada |
| Complementação temporal | Seção 08 executada: 15 CSVs, quatro figuras e relatórios |
| Execução integral local | Seções 00–08 executadas em cópia isolada via Python/IPython; 129 tabelas históricas concordantes |
| Interface Google Colab | Validação real pendente |
| Metodologia/desenho científico | Parcialmente documentados; decisões finais futuras |
| Modelo GEO | Futuro |
| Investigação estatística do modelo | Futura |
| Modelo nacional e comparação | Futuros |
| Revisão acadêmica e LaTeX | Futuros; citações Google dos capítulos 3/4 ainda exigem harmonização |

## O que a seção 08 acrescentou

- **Estacionariedade:** ADF/KPSS nacionais e por GEO, com constante e tendência, limites dos p-valores e tratamento conservador das comparações múltiplas. No país, o diagnóstico com constante é misto; com tendência, é compatível com estacionariedade em torno de tendência, sem comprovação.
- **Trajetórias:** 15/40 GEOs apresentam direção descritiva oposta à nacional; o saldo de janelas iniciais/finais oculta compensação de movimentos locais. A classificação tem sensibilidade de limiar documentada.
- **Persistência:** ACF(1) nacional das impressões de Channel2 = 0,236 e Channel3 = 0,310; as medianas locais são 0,046 e 0,090. Persistência da exposição não é duração causal do efeito.
- **Sazonalidade:** correlações entre três blocos anuais após detrendização de −0,120, 0,222 e 0,036; pouca evidência de formato anual estável, com somente três ciclos.
- **Instabilidade:** comparação de janelas e estatísticas móveis; sem afirmar rupturas, remover extremos ou inferir eventos reais.

As evidências completas e limitações estão no [relatório temporal](docs/DIAGNOSTICO_TEMPORAL_COMPLEMENTAR.md). O [mapeamento para o TCC](docs/MAPEAMENTO_EDA_PARA_TCC.md) indica possíveis inserções futuras; os capítulos acadêmicos não foram reescritos.

## Estrutura existente

```text
TCC_MMM_Google_Meridian/
├── README.md
├── requirements.txt
├── requirements-temporal.txt
├── constraints-tested.txt
├── tcc/
│   ├── 01_introducao.md
│   ├── 02_referencial_teorico.md
│   ├── 03_material_e_metodos.md
│   ├── 04_resultados_eda.md
│   ├── referencias.md
│   ├── figuras/
│   └── controle_de_elementos.csv
├── notebooks/01_EDA_COMPLETA.ipynb
├── data/{raw,processed,metadata}/
├── docs/
│   ├── EDA_DIDACTIC_GUIDE.md
│   ├── DIAGNOSTICO_TEMPORAL_COMPLEMENTAR.md
│   ├── MAPEAMENTO_EDA_PARA_TCC.md
│   ├── desenho_cientifico.md
│   ├── decisoes_metodologicas.md
│   ├── reproducibilidade.md
│   ├── auditoria_migracao.md
│   ├── VALIDACAO_PRESERVACAO_EDA.md
│   └── proveniencia/
├── outputs/
│   ├── figures/{data_audit,general,temporal,geo,media_geo,relationships}/
│   ├── tables/
│   ├── reports/
│   ├── logs/
│   └── temporal_complement/{figures,tables,reports,logs}/
├── scripts/
└── tests/
```

A árvore resume diretórios existentes; não inclui notebooks nem capítulos futuros vazios. `outputs/` guarda evidências; `tcc/` guarda o texto e apenas as sete figuras editoriais selecionadas. [Manifesto dos 12 elementos acadêmicos](tcc/controle_de_elementos.csv).

## Executar

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python scripts/execute_notebook.py --mode full --engine inprocess
```

O modo integral cria uma cópia em `validation_runs/`, para preservar os arquivos históricos versionados. Para somente o complemento:

```bash
python -m pip install -r requirements-temporal.txt
python scripts/execute_notebook.py --mode temporal --engine inprocess
```

[Instruções completas para ambiente local e Colab](docs/reproducibilidade.md). [Abrir notebook no Colab](https://colab.research.google.com/github/thiagossilva17/TCC_MMM_Google_Meridian/blob/main/notebooks/01_EDA_COMPLETA.ipynb): é necessário preparar o checkout e instalar os requisitos antes da execução; abrir a URL não disponibiliza automaticamente os dados.

## Proveniência, preservação e limites

O notebook tem 136 células: 122 de origem e 14 novas. Dessas originais, 102 permanecem integralmente idênticas, 18 receberam ajustes de navegação/descrição e duas receberam correções de infraestrutura. Todos os outputs históricos permanecem intactos. As funções científicas mantêm AST idêntica; a correção do fingerprint é operacional. A base raw tem checksum verificado, e o Meridian é fixado no commit oficial documentado.

A [auditoria da migração](docs/auditoria_migracao.md) e a [validação de preservação](docs/VALIDACAO_PRESERVACAO_EDA.md) apresentam hashes, diferenças, testes e limitações. Os projetos anteriores são apenas fontes de proveniência; nenhum é necessário para executar este projeto. A licença original dos dados está em [MERIDIAN_LICENSE](data/metadata/MERIDIAN_LICENSE).

Dados sintéticos, apenas três ciclos anuais e dependência entre observações limitam as conclusões. Não há efeitos causais verdadeiros validados, posterior estimada, ROI, otimização de orçamento ou resultado de comparação GEO × nacional nesta entrega. A próxima etapa é o [desenho e configuração científica](docs/desenho_cientifico.md), sem início automático da modelagem.
