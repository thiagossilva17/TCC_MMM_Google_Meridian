# Validação da preservação da EDA

## Entrada e comparação

O anexo `01_EDA_COMPLETA(4).ipynb` possui SHA-256 `c184cd07d2313fd0f84c2f5a5b805e9a881e006dfe1804da04bb95dea198387d`, 122 células (75 Markdown, 47 código). Sua representação integral, inclusive outputs, metadados, identificadores e formatação JSON, está comprimida em `proveniencia/notebook_original.json.gz`.

| Grupo | Quantidade | Evidência |
|---|---:|---|
| Células originais integralmente idênticas como objetos JSON | 102 | Comparação automatizada com snapshot |
| Células Markdown adaptadas para navegação/descrição da raiz | 18 | Diff exato por célula |
| Células de código com adaptação de infraestrutura | 2 | Índices zero-based 4 e 9 |
| Células complementares anexadas ao final | 14 | Sete Markdown e sete código |
| Total final | 136 | Validação nbformat |

A ordem das 122 células, todos os seus outputs, metadados e anexos foram preservados. Não se declara identidade byte a byte do notebook final, cujo JSON foi serializado novamente. As células sem alteração são idênticas estruturalmente. Nenhum output histórico foi substituído pelo da reexecução.

## Exceções de infraestrutura

**Célula 4:** raiz por marcador/variável de ambiente; leitura dos requisitos versionados, sem sobrescrevê-los durante instalação. **Célula 9:** fingerprint estrutural determinístico substitui a serialização `marshal` do objeto inteiro. A execução inicial das etapas 00–06 terminou, mas o checkpoint 07 detectou falsamente alterações em oito funções não redefinidas (`show`, `dictionary`, `save`, `heatmap`, `bars`, `lines`, `table`, `enrich`). A correção conserva a verificação de integridade e distingue alteração efetiva de código. Teste específico executa a mesma função 10.000 vezes e verifica estabilidade; uma redefinição é detectada.

Os 53 identificadores de funções de nível superior foram comparados. Somente `code_state`, função de infraestrutura, mudou; as outras 52 definições, incluindo todas as funções científicas, mantêm AST idêntica. Não houve mudança de filtros, fórmulas, agregações, limiares, figuras ou resultados históricos.

[Diff completo, hashes e justificativas](proveniencia/alteracoes_portabilidade.json).

## Execução real

A reexecução integral das seções 00–08 ocorreu em cópia isolada, por Python/IPython, incluindo a EDA oficial Meridian 2.1.0 no commit fixado. Nenhuma posterior, MCMC, ROI ou alocação foi estimada. As 129 tabelas históricas recalculadas concordam em forma, rótulos e valores com tolerâncias `rtol=atol=1e-7`. [Comparação por arquivo](proveniencia/comparacao_reexecucao.json) e [manifesto das etapas](proveniencia/reexecucao_integral_manifesto.json).

O kernel Jupyter via ZMQ não iniciou neste host por bloqueio de sockets (`Operation not permitted`). A validação realizada é de execução de código e captura de outputs, não da interface Colab. Os outputs e relatórios históricos permanecem intactos, inclusive seus registros de limitações anteriores.

## Figuras e tabelas

Os sete SVGs técnicos foram convertidos por CairoSVG 2.8.2, escala 2, sem recálculo. Comparação visual lado a lado com os PNGs embutidos no notebook confirmou conteúdo, escalas, eixos, cores, legendas e títulos. Diferenças de rasterização/resolução não foram tratadas como identidade de bytes. [Correspondência por célula/output](proveniencia/figuras_correspondencia_notebook.json).

Tabelas acadêmicas 1–4: conferência do painel, decomposições, participações/atividade e correlações com tolerâncias de arredondamento. Tabela 5: síntese interpretativa preservada, sem apresentá-la como output numérico direto. O manifesto editorial registra 12 elementos.

## Ampliação

A seção 08 exporta 15 CSVs, quatro figuras e relatórios próprios. As interpretações são geradas dos valores efetivamente calculados. A escala GEO continua observacional; os testes não identificam causalidade. O mapeamento acadêmico propõe revisão posterior, sem incorporar os resultados diretamente aos capítulos 3 e 4.


## Validação final em ambiente virtual novo

Instalação dos requisitos em venv sem system-site-packages concluída; execução sequencial 00–08 em cópia isolada concluída. As 129 tabelas históricas e os 15 CSVs complementares concordaram com os artefatos preservados/publicados. O ambiente foi registrado em [ambiente_limpo.json](proveniencia/ambiente_limpo.json). Os nove testes finais passaram; resultado em [testes.txt](proveniencia/testes.txt). Essa verificação não substitui a interface real do Colab.
