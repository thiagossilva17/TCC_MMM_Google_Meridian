# Auditoria do planejamento integrado — 03/11/2026

## Escopo e checkpoints

Repositório exclusivo: `thiagossilva17/TCC_MMM_Google_Meridian`, branch `main`. Commit inicial: `cff48026c51c3c4542abcd863f18e2a343eacde6`; checkout inicialmente limpo. A conversa anexada foi lida por OCR de suas 68 páginas e inspeção visual quando necessário. A última revisão descrita no PDF não constava da branch publicada: não foi tratada como decisão já incorporada. Não se alteraram repositórios históricos nem se executaram instruções antigas do PDF como tarefa atual.

A tarefa 1 acrescentou conteúdo exclusivamente às Seções 3.3 e 4.6, no commit `8fbf68f`. Preservou toda a redação anterior dessas seções e todos os demais trechos. A tarefa 2 executou sequencialmente as intervenções 1 → 2 → 3 → 5; depois atualizou uma única vez 3.5, 3.6 e 3.7. A seção 3.3 e todo o Capítulo 4 foram congelados após a tarefa 1.

A identificação do commit final consta do histórico Git que contém esta auditoria: evita-se um hash autorreferente impossível de registrar dentro do próprio commit. A confirmação de publicação será fornecida na entrega após verificação remota.

## Fontes e matriz de evidências

Lidos: os cinco arquivos de `tcc/`, o notebook consolidado (fontes e saídas relevantes, especialmente 08/A–E), `EDA_DIDACTIC_GUIDE.md`, `DIAGNOSTICO_TEMPORAL_COMPLEMENTAR.md`, `MAPEAMENTO_EDA_PARA_TCC.md`, `desenho_cientifico.md`, `decisoes_metodologicas.md`, `reproducibilidade.md`, dicionário, dependências, testes históricos e CSVs pertinentes. O prompt atual foi lido integralmente e os valores não foram tomados apenas de resumos. Nenhum protocolo parcialmente publicado foi encontrado na árvore inicial.

| Evidência | Fonte em outputs/temporal_complement/tables/ | Leitura / limite | Decisão |
|---|---|---|---|
| Nacional ADF(c) p≈6,287e−23; KPSS(c) p≈0,0471 | tc_stationarity_national.csv | Hipóteses diferentes; evidência mista com constante | Não diferenciar automaticamente |
| ADF(ct) p≈3,676e−20; KPSS(ct) limite ≥0,10 | tc_stationarity_national.csv | Compatível com tendência estacionária sob especificação; não prova | Examinar flexibilidade temporal |
| ADF em nível rejeita nos 40 GEOs; KPSS BY nenhuma rejeição | tc_stationarity_summary.csv | BY conservador; limites dos p-valores; dependência GEO | Evitar votação de testes como identificação |
| 23 altas, 15 quedas, 2 estáveis a ±1% | tc_geo_trend_profile.csv; tc_geo_trend_summary.csv | Critério descritivo; sensibilidade 0/5% | Diagnósticos de tendências residuais locais |
| Compensação 57,4% entre mudanças de janelas | tc_geo_trend_profile.csv | Soma de magnitudes, não efeito causal | Comparar agregado e GEO |
| Channel2/3: ACF(1) nacional 0,236/0,310; medianas GEO 0,046/0,090 | tc_media_temporal_persistence.csv; tc_media_persistence_summary.csv | Calendário não identifica adstock | Sensibilidade de forma e max_lag |
| Maior inatividade local 27/2 semanas | tc_geo_media_persistence.csv | Suporte desigual, não experimento natural | Atenção específica aos dois canais |
| Blocos detrendizados −0,120; 0,222; 0,036 | tc_seasonality_diagnostic.csv | Só três blocos; não anos civis | Não impor controles sazonais artificiais |
| Mudança nacional 3,8616% da média global; razão SD 0,9172 | tc_instability_windows.csv | Não é crescimento relativo ao início nem teste de quebra | Avaliação por janelas e influência |

A mediana GEO de sazonalidade foi conferida no arquivo detalhado excluindo `Nacional`: o resumo `tc_seasonality_summary.csv` agrupa também a linha nacional, portanto não foi usado como se resumisse apenas 40 GEOs. Essa particularidade histórica foi registrada, sem alterar seu CSV.

## Etapas e passagens

1. **Temporal:** oito candidatos e posições explícitas; defaults distinguidos das referências de pesquisa; K=T incompatível com B; AKS opcional bloqueado para seleção que utiliza reservas. API verificada no commit fixado.
2. **Comparação:** conservação dos totais, ponderação explícita dos índices, receita omitida; A=1.248 células, B=31 semanas, desenvolvimento=15. Cobertura e posto temporal conferidos. Base nacional condicional à semântica dos índices, com fonte e hash no YAML.
3. **Diagnósticos:** critérios computacionais, residuais, preditivos e estruturais definidos; nenhuma posterior inexistente diagnosticada.
4. **Sensibilidade:** 29 cenários, nove essenciais; máscaras, referências, parâmetros, prioridades e dependências explícitos; todos não executados ou condicionais.
5. **Acadêmico:** somente 3.5–3.7 na segunda tarefa, com chamadas bibliográficas correspondentes a entradas já existentes nesses trechos revisados.

## Compatibilidade e vazamento

A inspeção estática confirma `knots`, `enable_aks`, `holdout`, legado `holdout_id`, `adstock_decay_spec`, `hill_before_adstock`, tipos de prior e campos de `PriorDistribution`. O JSON `planejamento/meridian_api_audit.json` guarda campos e hashes dos arquivos examinados. A biblioteca não foi atualizada nem instalada para estimar modelos.

A política de coeficientes é uma escolha de pesquisa, não o default de ROI. Identificou-se uso do KPI completo em `KpiTransformer`, em AKS e em parametrizações dependentes do total do resultado. A mitigação por isolamento das reservas foi implementada como helper e testada em software; a invariância dentro do Meridian continua sendo uma condição obrigatória antes de ajustar. A verificação de posto cobre somente a base temporal e, no caso A, também a estrutura aditiva temporal/geográfica, não toda a identificação não linear.

`Analyzer.expected_outcome` exige `use_kpi=True` nesta pesquisa. O código upstream oferece expectativas por draw e métricas preditivas, mas isso não substitui uma simulação do ruído para PPC. `posterior_sampler.py` exporta `sample_stats` a partir dos campos disponíveis; energia e tree depth não serão presumidos presentes.

## Integridade e testes

O manifesto novo `planejamento/preservation_manifest.json` congela por SHA-256 318 arquivos da árvore inicial. Nos dois capítulos editáveis, congela seções fora do escopo e verifica adicionalmente que o texto da tarefa 1 não mudou na tarefa 2. Capítulos 1/2, bibliografia, notebook completo, raw, painel GEO, código temporal, outputs, figuras, tabelas e manifestos históricos continuam protegidos.

Três testes históricos usavam o hash integral dos capítulos de antes da revisão (migração, preservação acadêmica e caminhos editoriais das tabelas). Foram atualizados apenas esses invariantes obsoletos: continuam conferindo os demais arquivos históricos; agora verificam preservação por seção para os capítulos autorizados e identidade integral dos blocos de tabelas. Os hashes e manifestos originais não foram substituídos para fazer testes passarem.

O ambiente de teste da preparação é isolado em relação às dependências históricas. A primeira tentativa encontrou ausência de pytest; foi preparado ambiente virtual com `requirements-planning.txt`, sem mudar `requirements.txt` ou `constraints-tested.txt`. A EDA não foi reexecutada.

Resultado final da suíte: **25 testes aprovados em 7,12 segundos**, sem falhas. `git diff --check` também não encontrou erros de whitespace. A primeira execução completa teve 24 aprovações e uma falha no hash integral de capítulo usado como destino editorial de tabela. A verificação foi refinada para comparar os blocos das tabelas byte a byte, sem alterar tabelas ou manifestos.

## Arquivos e reprodução

Modificados na tarefa 1: `tcc/03_material_e_metodos.md`, `tcc/04_resultados_eda.md`.

Modificados na tarefa 2: `tcc/03_material_e_metodos.md`, `docs/desenho_cientifico.md`, `docs/decisoes_metodologicas.md`, `tests/test_integrity.py`.

Criados:

- `docs/PROTOCOLO_CIENTIFICO_INTEGRADO.md`, `docs/MATRIZ_EXPERIMENTAL.md`, esta auditoria.
- `configs/temporal_specifications.yaml`, `configs/agregacao_nacional.yaml`, `configs/validacao_holdout.yaml`, `configs/diagnosticos_posteriores.yaml`, `configs/sensibilidades.yaml`.
- `configs/holdouts/holdout_geo_distribuido.csv`, `configs/holdouts/holdout_semanas_comuns.csv`, `configs/holdouts/holdout_manifest.json`.
- `data/processed/national_weekly.csv` (sob hipótese explícita; não substitui painel GEO).
- `src/planning.py`, `scripts/prepare_planning.py`, `scripts/render_experiment_matrix.py`, `tests/test_planning.py`, `requirements-planning.txt`.
- `docs/planejamento/meridian_api_audit.json`, `docs/planejamento/preservation_manifest.json` e registro dos testes.

Reproduzir os comandos indicados no protocolo. O diff completo entre o commit inicial e a entrega identifica exatamente cada acréscimo. Não foram adicionados anexos de conversa ao repositório, nem cópias integrais do upstream, ambientes, caches ou dados de modelos fictícios.

## Limitações e pendências

**Concluído:** incorporação temporal, desenho integrado, configuração, máscaras, agregação operacional, código auxiliar, testes e verificação de preservação.

**Condicional:** semântica da ponderação dos controles/Promo, justificativa causal dos controles, priors preditivas, integração das máscaras e invariância de transformações/priors à resposta reservada. A seleção AKS permanece opcional e não elegível para o desenho principal atual.

**Não validado empiricamente:** configuração ótima, adequação de priors, contribuições, convergência dos MMMs, estabilidade e superioridade GEO. Nenhum experimento de modelagem foi executado.

**Documentação preservada fora do escopo:** 3.1/3.4 mantêm citações antigas Google [s. d.]; 3.8 e o mapeamento histórico descrevem o estado anterior. A auditoria de migração registra reexecução isolada, mas não altera retroativamente a redação protegida. A bibliografia não contém referências específicas de ADF/KPSS, BY, Theil–Sen ou Ljung–Box; sua inclusão acadêmica deve ser tratada em revisão bibliográfica autorizada, sem inventar atribuição a Gelman ou Google. A revisão geral de referências, o guia didático consolidado e LaTeX não foram ampliados para além do pedido atual.

**Futuro:** validar preparação na biblioteca, executar prior predictive checks, ajustar modelos, diagnosticar, avaliar sensibilidades, consolidar resultados e revisar a monografia final. A validação na interface real do Colab continua pendente.
