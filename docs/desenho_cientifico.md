# Desenho científico — mapa das próximas entregas

Status em 01/11/2026: planejamento; nenhum modelo estimado nesta migração. O problema central é comparar GEO × nacional sob estimandos, horizontes e tarefas de avaliação compatíveis. Os capítulos acadêmicos registram propostas; esta página não congela parâmetros ainda não avaliados.

| Entrega futura | Perguntas e decisões | Evidência necessária para encerramento |
|---|---|---|
| 1 — Desenho e configuração científica | Formalizar hipóteses sobre heterogeneidade, ganho/perda de informação, confundimento e identificabilidade; escolher especificações comparáveis, priors, controles, adstock, saturação, knots, max_lag, holdouts, métricas e sensibilidades | Protocolo datado, configurações justificadas, regras de agregação e critérios de avaliação definidos antes de interpretar contribuições |
| 2 — Modelo GEO de referência | Estimar o modelo com compartilhamento hierárquico, avaliar baseline, ajuste e incerteza | Cadeias, R-hat, ESS, divergências, verificações preditivas e avaliação fora da amostra |
| 3 — Investigação estatística | Estudar sensibilidade a priors, controles, flexibilidade temporal, dependência residual, influência e estabilidade das contribuições | Experimentos registrados; resultados favoráveis e desfavoráveis preservados |
| 4 — Nacional e comparação | Agregar conforme semântica de cada variável; harmonizar tarefas, horizonte, estimandos e avaliação; explicitar diferenças de flexibilidade | Avaliação em escala nacional comum, incerteza posterior e limites da comparação |
| 5 — Consolidação acadêmica | Discutir achados, limites da base sintética, conclusões e diagramação | Resultados efetivamente obtidos incorporados à monografia, citações harmonizadas e posterior projeto LaTeX |

A seção 08 informa essas decisões, mas não escolhe automaticamente transformações nem comprova causalidade. Não iniciar estimação só porque a migração está pronta.

## Estado atualizado em 03/11/2026

A entrega de desenho agora está especificada no [protocolo científico integrado](PROTOCOLO_CIENTIFICO_INTEGRADO.md), com [matriz experimental gerada](MATRIZ_EXPERIMENTAL.md), cinco configurações YAML, preparação nacional sob hipótese explícita e máscaras congeladas. As Seções 3.3/4.6 incorporam evidências da seção 08; 3.5–3.7 sintetizam o planejamento.

O próximo passo é validar os objetos de entrada na versão fixada, a equivalência das máscaras, a invariância ao KPI reservado e as distribuições preditivas da prior. Somente depois dessas portas será admissível estimar os modelos. As hipóteses substantivas de agregação dos índices e de posição causal dos controles continuam condicionais. Nenhum modelo, diagnóstico posterior ou resultado de robustez foi executado nesta entrega.

Ordem de leitura para esta etapa: protocolo → matriz → auditoria. Os documentos da EDA e seus manifestos históricos foram preservados; não há uma segunda EDA nem quatro protocolos concorrentes.
