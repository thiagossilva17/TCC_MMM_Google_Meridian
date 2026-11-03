# Decisões metodológicas e operacionais

Data destas decisões: 01/11/2026. Os registros históricos permanecem em [decisions.md](decisions.md); sua data não foi substituída pela migração.

| Decisão | Evidência e justificativa | Alternativa considerada | Limitação/impacto | Status |
|---|---|---|---|---|
| Notebook anexo como fonte canônica | 122 células, 79 imagens em outputs; hash no inventário | Reconstruir notebooks particionados | Evita perder a consolidação; snapshot integral comprimido permite reconstrução | Executada |
| Manter capítulos e bibliografia sem revisão científica | Escopo explícito de preservação | Harmonizar citações agora | Citações Google [s. d.] nos capítulos 3/4 permanecem pendentes | Executada |
| Raiz por marcador ou variável explícita | Célula inicial apontava para nome de projeto antigo | Criar alias com nome antigo | Fail-fast fora do checkout; independência efetiva | Executada |
| Fingerprint estrutural de funções | Primeira execução integral gerou falsos positivos no hash marshal após etapas 00–06 | Desativar a validação | Validação mantida; código modificado continua detectável; funções científicas intactas | Correção de infraestrutura executada |
| ADF AIC e KPSS automático em c/ct | Distinguir nível estável e tendência; 156 semanas | Fixar um lag arbitrário | Seleção depende da amostra; KPSS registra limites dos p-valores | Executada |
| BY por família de 40 GEOs | Dependência entre mercados e múltiplas comparações | Tratar testes como independentes | Conservador; KPSS usa limite superior para ajuste, podendo perder poder | Executada |
| Escalas nível, por mil habitantes e diferenças apenas diagnósticas | População constante por GEO e questão de persistência | Diferenciar automaticamente a resposta | Sem transformação definitiva do MMM | Executada |
| Theil–Sen normalizado, faixa ±1%, sensibilidade 0/5% | Escalas geográficas distintas | Comparar inclinações absolutas | Classificação descritiva; não é teste de efeito causal | Executada |
| ACF cronológica com zeros; gasto e atividade separados | Intermitência Channel2 e continuidade Channel3 | Excluir semanas sem mídia | Excluir destruiria o calendário; série constante tem ACF indefinida | Executada |
| Comparar três blocos de 52 semanas e tendência linear auxiliar | STL e ACF anual já existiam | Nova busca espectral extensa | Apenas três ciclos; bloco não equivale ao ano civil | Executada |
| Janelas 13/26 e blocos 52 para instabilidade | Questão exploratória, sem data de ruptura pré-especificada | Testes formais de quebras múltiplas | Sem comprovação de ruptura; sem remoção de extremos | Executada |
| Manter MMM, knots finais, priors e holdout para próxima entrega | Esta tarefa é EDA e migração | Antecipar parâmetros finais | A evidência atual orienta hipóteses, não encerra identificação | Futura |

A hipótese de que granularidade geográfica melhora a inferência permanece aberta. As decisões acima não foram justificadas retroativamente por uma busca de resultados favoráveis.

## Atualização de 03/11/2026 — planejamento integrado

Os registros de 01/11 são históricos. A decisão então futura de formalizar o desenho é desenvolvida no [protocolo integrado](PROTOCOLO_CIENTIFICO_INTEGRADO.md); não significa que os modelos tenham sido estimados. A incorporação temporal em 3.3/4.6 ocorreu primeiro, no commit `8fbf68f`, e permanece congelada na segunda tarefa.

| Decisão atual | Evidência/justificativa | Alternativa | Limite | Estado |
|---|---|---|---|---|
| Grades temporais pequenas e posições determinísticas | Tendências locais heterogêneas; flexibilidade padrão GEO/nacional diferente | Otimizar knots pela EDA | Não há ótimo conhecido; posto temporal não garante identificação total | proposed |
| GEO-K13 × NAT-K13 como par inicial B | Reduz diferença de flexibilidade; suporte temporal verificado | Comparar só os padrões | Hierarquia e agregação continuam distintas | reference de desenho |
| K=T apenas em A | Em B há semanas sem nenhuma observação de treino | Usar prior para preencher efeitos livres sem suporte | Não interpretar efeitos sem suporte como validação identificada | approved para restrição |
| AKS fora da comparação principal | Fonte fixada consulta KPI sem máscara | Seleção automática no calendário completo | Seleção em treino requer implementação e validação próprias | conditional |
| Priors por coeficiente e KPI não monetário | Semântica monetária não confirmada; evitar calibragem pelo KPI reservado | ROI ou contribution | Priors precisam de verificação preditiva e equivalência de escala | proposed |
| Controles/Promo ponderados por população | Convenção da EDA; índices contínuos | Média simples prevista | Semântica populacional não comprovada; hipótese explícita | conditional |
| Máscaras materializadas A/B e desenvolvimento separado | Congelar observações e impedir seleção pelo teste | Escolher reservas após ajustar | EDA já observou todo o calendário | materialized |
| Isolar KPI reservado no objeto de ajuste | Transformador do upstream usa todo o KPI | Declarar holdout suficiente | Teste de invariância do helper passa; integração Meridian pendente | requires_validation |
| Quatro dimensões de diagnóstico | Convergência não substitui adequação temporal ou estrutural | Nota única de qualidade | Diagnósticos reais só após ajuste | not_executed |
| Nove cenários essenciais e conjunto ampliado condicionado | Priorização de knots, priors e controles | Fatorial completo | Linhas pareadas exigem dois modelos; custo futuro | proposed |
| Preservação por arquivo e por seção | Autorização limitada a 3.3, 4.6 e depois 3.5–3.7 | Trocar hashes históricos | Manifestos históricos intactos; novos testes verificam limites específicos | implemented |

Parâmetros, máscaras e cenários possuem fontes únicas nos YAMLs. Esta tabela registra razões e estado, sem manter outra grade numérica independente.
