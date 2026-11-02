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
