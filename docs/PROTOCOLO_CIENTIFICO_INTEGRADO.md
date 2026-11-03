# Protocolo científico integrado — GEO × nacional

Versão de planejamento: 03/11/2026. Estado: especificações propostas e preparação verificadas; **nenhum MMM estimado**. Fonte executável de decisões: cinco YAMLs em `configs/`. A [matriz experimental](MATRIZ_EXPERIMENTAL.md) é derivada desses arquivos. A [auditoria](AUDITORIA_PLANEJAMENTO_INTEGRADO.md) registra evidências, preservação e condições ainda não validadas.

A questão é como a agregação geográfica modifica estimativas, incerteza e avaliação. Não se assume superioridade GEO, nem que 6.240 células dependentes equivalham a experiências independentes. A pesquisa compara modelos observacionais de dados sintéticos; não dispõe de parâmetros geradores verdadeiros ou de lift tests para calibração causal.

## I — Especificação temporal

### I.1 Representação e identificação

Adota-se $\boldsymbol\mu=\mathbf W\mathbf b$, com $\mathbf W\in\mathbb R^{T\times K}$, $\mathbf b\in\mathbb R^K$ e $T=156$. Os pesos interpolam linearmente os valores dos knots; fora dos extremos, prevalece o knot mais próximo. A implementação fixada armazena os pesos na orientação transposta, $K\times T$. Não confundir essa orientação de armazenamento com a fórmula expositiva.

Knots controlam a dimensão da componente temporal compartilhada: muitos pontos permitem trajetórias mais flexíveis, mas podem competir com mídia e controles; poucos pontos podem deixar variação relevante sem representação. Interceptos GEO representam diferenças persistentes de nível. Controles GEO × tempo podem explicar movimentos locais quando causalmente justificáveis. Nenhum desses componentes isolados equivale ao baseline completo: este é o resultado esperado sob um cenário de referência explicitado para as mídias e tratamentos, incluindo interceptos, controles e transformação inversa para conversões.

As evidências de 15 trajetórias locais opostas à nacional motivam diagnósticos posteriores; não autorizam acrescentar 40 tendências independentes. A STL de três ciclos não justifica Fourier ou dummies anuais automáticas. Os testes ADF/KPSS não determinam diferenciação do KPI ou uma quantidade ótima de knots. Não há garantia de identificação causal por posto completo da base temporal, bom ajuste ou convergência.

### I.2 Referências e candidatos

`temporal_specifications.yaml` contém posições explícitas e parâmetros. O padrão da versão fixada é `knots=None, enable_aks=False`: equivale a K=T no GEO e K=1 no nacional. Não se deve impor K=T ao nacional: um parâmetro temporal por observação permite saturar a dimensão temporal e competir integralmente com os demais componentes.

| Nível | Candidatos | Papel |
|---|---|---|
| GEO | 156, 52, 26, 13 | K=156 referência de implementação para A; demais candidatos para B |
| Nacional | 1, 4, 8, 13 | K=1 referência de implementação; alternativas de flexibilidade |
| Par principal B | GEO-K13 e NAT-K13 | Posições idênticas para reduzir uma fonte de diferença; escolha de desenho, não ótimo empírico |

As posições seguem `numpy.linspace(0,155,K,dtype=int)`, que trunca para inteiros, sem escolher datas com base no KPI. K=13 oferece uma dimensão temporal moderada e comum às duas grades; não representa sazonalidade de 13 semanas. A referência pareada não elimina diferenças de hierarquia, pooling, escala, transformação não linear e distribuição de exposição. Referências padrão e par com flexibilidade harmonizada respondem a perguntas distintas.

Para cada máscara verifica-se posto e massa de treinamento das colunas de W. No holdout A há 32 mercados observados em cada semana, preservando suporte direto de K=T. No B, K=156 perde posto; fica inelegível. K=52,26,13 no GEO e K=1,4,8,13 no nacional mantêm posto completo também ao retirar as 15 semanas de desenvolvimento. Isso é condição necessária, não teste completo de identificação do MMM não linear. Após carregar os dados serão necessários diagnósticos de desenho conjunto, priors e posterior.

### I.3 AKS e versão

Fonte técnica: Meridian 2.1.0 no commit `02111531f8661373aa7b6ba31c316c67d72d1dd2`, mantido em `requirements.txt`. O código `knots.py` implementa splines adaptativas com penalização, escala a penalização por $1/\sqrt G$ e seleciona pelo AIC entre candidatos admissíveis. Utiliza `InputData.scaled_centered_kpi`; o caminho em `ModelContext.knot_info` não transmite máscara de holdout. Portanto, AKS não é seleção causalmente ótima nem automaticamente restrita ao treino.

`enable_aks=True` exige `knots=None`; a combinação com knots explícitos é inválida. AKS é apenas exploração opcional, excluída da comparação principal. Usar KPI preenchido artificialmente nas reservas também não constitui seleção em treino: uma implementação futura deve realmente restringir o objetivo às observações de treinamento, manter o calendário e passar testes de invariância. AKS não foi executado.

### I.4 Mídia, priors e histórico

A referência usa adstock geométrico, Hill após adstock, `max_lag=8`, efeitos de mídia `log_normal`, slope de Hill fixado em 1 e EC com prior truncada. `adstock_decay_spec='binomial'` e `hill_before_adstock` existem no código fixado. Os valores completos de todas as priors utilizadas estão no YAML, sem copiar hiperparâmetros neste documento.

A parametrização proposta para mídias paga e orgânica é por coeficiente, com prior Normal na média hierárquica em espaço logarítmico e HalfNormal na dispersão. A Normal permite média logarítmica negativa, mas o efeito local lognormal permanece positivo. A escolha evita depender de receita por conversão e de calibragens automáticas baseadas no total do KPI. Não é a prior padrão de ROI nem uma prior calibrada externamente. `Promo` conserva tratamento contínuo, prior por coeficiente e referência zero; os dois controles ficam presentes na referência, sob hipótese de confundidores pré-tratamento a ser defendida. Orgânico permanece componente próprio, não controle reclassificado.

Priors numericamente iguais nas escalas internas não implicam informação equivalente entre GEO e nacional. Antes da estimação, exigir verificações preditivas da prior nas unidades de conversões e sob exposições observadas. Se forem implausíveis, registrar uma emenda datada ao protocolo sem consultar o teste final. Nenhuma distribuição é declarada ótima. Coeficientes e dispersões padrão restantes são identificados no YAML e na auditoria de API.

O painel fornece 156 tempos de mídia e 156 tempos de KPI, sem pré-histórico anterior à primeira semana. Alterar max_lag não autoriza cortar silenciosamente o KPI. A implementação permite preenchimento anterior com zeros: isso é hipótese de inicialização, não exposição observada. Preservar 156 semanas nas alternativas L=4,8,10; inspecionar separadamente influência das primeiras dez semanas. A autocorrelação da exposição não estima memória causal, especialmente diante das lacunas de Channel2 e da continuidade de Channel3.

## II — Comparação GEO × nacional

### II.1 Agregação e unidades

`agregacao_nacional.yaml` é a fonte dos operadores. A preparação determinística gera `data/processed/national_weekly.csv`, sem modificar o painel original.

| Variável | Operação | Interpretação e ressalva |
|---|---|---|
| Conversões | Soma por semana | Conservação do KPI; conversões sintéticas contínuas |
| Impressões pagas e orgânicas | Soma por semana | Contagens aditivas de exibições; não alcance único |
| Gastos | Soma por semana e canal | Moeda não documentada; não interpretar ROI comercial |
| População | Soma de uma população por GEO | Total repetido por semana apenas como metadado; nunca somar sobre 156 semanas |
| Dois controles | Média ponderada pela população | Hipótese operacional para índices sintéticos; unidade/população-alvo não comprovadas |
| Promo | Média ponderada pela população | Índice contínuo de intensidade; não binarizar nem chamar de contagem |
| Receita por conversão | Omitida da entrada de modelagem | Evita conversões reservadas no peso; estimando primário não monetário |

A semântica populacional dos índices não foi confirmada em fonte geradora. Por isso, a série nacional é um **artefato sob hipótese explícita**, com status `conditional`, e não uma agregação substantiva universalmente validada. Uma alternativa por médias simples dos índices foi pré-especificada. A regra de ponderação reutiliza a EDA descritiva, mas não transforma sua convenção em verdade causal. A não linearidade implica que somar respostas transformadas GEO não equivale a transformar uma exposição somada nacional.

A soma populacional é preservada no CSV para auditoria. O carregador nacional do Meridian substitui a população por 1; não aplicar divisão manual extra antes dele. Para eventual reconciliação descritiva de receita, $RPC_t=\sum_g y_{gt}RPC_{gt}/\sum_g y_{gt}$, indefinido se o denominador for zero. Essa expressão não deve alimentar ajuste ou seleção: usa o próprio KPI, inclusive nas reservas.

### II.2 Experimentos e máscaras

**A — reprodução GEO interna:** máscara booleana 40×156, 1.248 células reservadas (20%), oito por semana e 31 ou 32 por mercado. O algoritmo permuta coordenadas e distribui oito posições cíclicas por semana. Não usa valores do KPI. É avaliação de células omitidas em mercados já observados; não mede generalização para mercados inteiramente novos. O nacional não é avaliado usando os totais parcialmente observados de A.

**B — comparação principal:** 31 semanas inteiras reservadas (19,87%), em estratos cronológicos de cinco semanas, sem reservas nas extremidades e sem blocos consecutivos extensos. Os mesmos KPIs são excluídos em todos os mercados e no nacional. O manifesto registra listas explícitas, seed, dimensões, hashes, versões e resultados de posto. CSV materializado, e não apenas a seed, define a máscara congelada.

O subconjunto `DEV-B` separa outras 15 semanas do desenvolvimento, sem sobreposição com o teste B. Durante escolha de especificações, excluir desenvolvimento e teste do ajuste: restam 110 semanas de treinamento. Comparar alternativas apenas nas 15 semanas de desenvolvimento, com incerteza e critérios estruturais; sua pequena dimensão limita seleção. A especificação escolhida poderá ser reajustada nas 125 semanas não pertencentes ao teste, antes de uma única avaliação final nas 31 semanas. A utiliza a referência pré-especificada; exploração posterior dos erros de A não poderá ser rotulada como validação intocada.

A nomenclatura A/B aqui segue o prompt atual (células versus semanas), não os rótulos alternativos empregados em um trecho da conversa histórica.

`True` significa KPI excluído da verossimilhança; mídia continua disponível para adstock. A API preferida usa `HoldoutSpec`, `GeoHoldoutSpec` e `DateRange`. O tensor `holdout_id` ainda é aceito, porém depreciado; nunca fornecer ambos. Exigir correspondência exata entre CSV e máscara compilada antes da amostragem. As máscaras foram validadas em NumPy; a conversão em objetos Meridian ainda requer teste de integração.

### II.3 Vazamento: condição explícita de execução

O código fixado constrói `KpiTransformer(self.kpi,self.population)` sem máscara, usando média e desvio do KPI completo. Priors por contribuição e alguns caminhos de calibração também dependem de totais do KPI. Portanto, holdout na verossimilhança não garante isolamento do teste.

A mitigação proposta mantém as verdades reservadas fora do objeto de entrada e preenche suas posições, apenas nesse objeto, com médias por GEO calculadas exclusivamente no treino. O helper `masked_kpi` é determinístico e sua invariância a perturbações do KPI reservado é testada. Mantêm-se máscaras verdadeiras e priors por coeficiente; não habilitar AKS ou calibração baseada no KPI. Esse preenchimento não é uma imputação da base de pesquisa e não entra na verossimilhança. Seus efeitos sobre a parametrização interna precisam de validação de integração, não bastando testar o helper.

**Porta obrigatória antes de MCMC:** variar arbitrariamente as verdades reservadas e verificar que entrada de ajuste, transformadores, hiperparâmetros, máscara compilada e log-probabilidade de treinamento permanecem iguais; garantir que métricas usem as verdades originais. Se não passar, bloquear a avaliação principal e corrigir a preparação sem editar o upstream ou o notebook protegido. Não há alegação de avaliação sem vazamento enquanto essa porta estiver pendente.

Exposições e controles de todo o calendário são conhecidos: a tarefa é reconstrução/interpolação condicional, não previsão operacional com covariáveis futuras desconhecidas. Além disso, a EDA já examinou todas as semanas; o teste será reservado ao ajuste e à seleção futura, mas não é amostra cega a toda a pesquisa. Reconhecer essa limitação em qualquer resultado futuro.

### II.4 Estimandos e métricas

A comparação preditiva B usa $Y_t^{NAT}=\sum_gY_{gt}$ e, para cada realização conjunta $s$, $\widehat Y_t^{GEO,s}=\sum_g\widehat Y_{gt}^{s}$. Somar dentro da mesma cadeia/draw antes de obter quantis conserva a dependência posterior entre mercados. Nunca somar limites de intervalos. A expectativa posterior e a predição de uma nova observação têm distribuições diferentes: a segunda inclui ruído da verossimilhança.

Sobre as mesmas semanas e escala original: $MAE=n^{-1}\sum|y-\hat y|$, $RMSE=\sqrt{n^{-1}\sum(y-\hat y)^2}$, $wMAPE=100\sum|y-\hat y|/\sum|y|$ e $R^2=1-\sum(y-\hat y)^2/\sum(y-\bar y)^2$. Denominadores nulos produzem resultado indefinido, não zero. R² pode ser negativo. Cobertura e largura utilizam intervalos preditivos centrais de 90%, quando disponíveis; não usar intervalos da média como se fossem preditivos.

O estimando substantivo é a contribuição incremental em conversões sintéticas por canal, agregada sobre população e horizonte comuns, comparando exposição observada e exposição zero do canal sob covariáveis fixas e cenário contrafactual documentado. Preservar a regra de mídia anterior ao horizonte e o tratamento de carryover em ambas as especificações. É uma quantidade condicional ao modelo; sem mecanismo gerador conhecido não se mede recuperação causal verdadeira. Ranking, ROI, mROI ou otimização de orçamento não serão resultados desta entrega.

| Dimensão | Tratamento da comparabilidade |
|---|---|
| Fonte, datas, KPI, canais, versão | Idênticos |
| Controles e Promo | Mesmos nomes e hipótese causal; agregação explícita |
| Knots | Par principal com posições iguais; padrões diferentes em experimentos separados |
| Adstock, Hill, max_lag | Iguais na referência; uma alteração por cenário |
| Priors | Famílias declaradas; equivalência substantiva examinada em prior predictive checks |
| Escala | Transformações internas distintas; avaliação em conversões originais |
| Hierarquia e pooling | Estruturalmente diferentes e inseparáveis da agregação |
| Holdout, métricas e horizonte | Mesmos em B; A é tarefa distinta |
| Incerteza | Draws conjuntos por modelo; nenhum pareamento arbitrário entre modelos |

## III — Diagnósticos posteriores

`diagnosticos_posteriores.yaml` separa qualidade computacional, temporal, probabilística e estrutural. Todos os resultados têm estado `not_executed`. Não calcular R-hat de EDA, nem tratar priors já simuladas como posterior.

### III.1 Qualidade computacional

Planejar quatro cadeias e sementes registradas. Referências: R-hat rank-normalizado e split ≤1,01, bulk/tail ESS ≥400 para quantidades essenciais, zero divergências após adaptação; acompanhar MCSE, trace e rank plots. Esses limites são heurísticas científicas, não os limites internos da biblioteca nem provas universais. Número de draws/adaptação será dimensionado para ESS e MCSE, nunca para produzir contribuição desejada; registrar tentativas e custos. Energia e profundidade da árvore só serão reportadas quando disponibilizadas pelo backend, sem inventar campos.

Cobrir efeitos pagos e orgânicos, controles, Promo, parâmetros hierárquicos, knots, interceptos geográficos, adstock, Hill e dispersão. Parâmetros determinísticos, como slope fixado, recebem `NAO_APLICAVEL`, não R-hat artificial. Falhas persistentes impedem interpretação substantiva e permanecem na matriz de resultados.

### III.2 Resíduos, calendário e geografia

Definir $e_{gt}=y_{gt}-\widehat{E}(Y_{gt}\mid D_{treino},X)$ em conversões. Distinguir resíduos de treino, erros reservados, resíduos padronizados e replicações preditivas. Nunca concatenar mercados ou comprimir semanas ausentes. ACF descritiva em calendários incompletos usa pares separados pela distância real e registra quantos pares existem; sua normalização por pares não é a ACF histórica da EDA. PACF e Ljung–Box exigem sequências regulares contíguas e amostra suficiente.

Inspecionar lags 1,4,8,13,26; lag 52 somente quando houver ao menos 100 pares, reconhecendo aproximadamente três ciclos. Para Ljung–Box, usar lag no máximo min(26,n/5), sem subtrair indiscriminadamente o número de parâmetros Bayesianos. A calibração assintótica após ajuste é aproximada: priorizar magnitude, gráfico e PPC; corrigir famílias geográficas por BY e não rejeitar modelos por um p-valor isolado. Em teste B descontínuo, Ljung–Box/PACF convencionais podem ser não aplicáveis.

Investigar tendências locais remanescentes, sequências de sinais, heterocedasticidade por população, correlações residuais entre mercados com datas alinhadas e padrões nas janelas de 13/26 semanas. Comparar treino e reservas separadamente; gráficos do calendário completo podem misturar ambos somente com marcação explícita. Baixa correlação histórica do KPI não garante independência residual.

### III.3 Verificações preditivas e baseline

Comparar observações com novas observações replicadas quanto a média, mediana, dispersão, quantis, extremos, ACF, tendências, sequências e mudanças entre janelas; por GEO, examinar within/between e trajetórias; no agregado, totais semanais, dispersão e periodicidade. `Analyzer.expected_outcome` é expectativa por draw, não simulação completa de observações. Para esta pesquisa, exigir `use_kpi=True`, `inverse_transform_outcome=True`, `aggregate_times=False` e, ao somar explicitamente mercados, `aggregate_geos=False`; o padrão de receita não é adequado sem receita por KPI. Uma implementação posterior de PPC deve adicionar o ruído conforme a verossimilhança confirmada, respeitar sigma e transformar de volta à escala original. Testar dimensões e unidades antes de interpretar cobertura.

O baseline completo será calculado no cenário de referência explicitado, com incerteza. Avaliar oscilações, extremidades, movimentos locais não capturados e competição com mídia. Aparência plausível ou grande R² não demonstram causalidade correta.

### III.4 Decisões

Classificar cada dimensão como satisfatória, requer investigação, problemática, inconclusiva, não aplicável ou não executada. Examinar primeiro MCMC, depois adequação preditiva, dependência temporal, heterogeneidade, baseline e síntese. Não produzir nota única que esconda falha. Mudanças de especificação motivadas por diagnósticos devem ser registradas como pré-especificadas ou exploratórias; nunca apagar resultados desfavoráveis.

## IV — Sensibilidade e robustez

`sensibilidades.yaml` registra 29 cenários, nove essenciais; linhas pareadas correspondem a dois ajustes, e os custos não são estimativas de tempo de execução. A matriz gerada contém hipótese, referência, alternativa, fatores fixos, máscaras, estimando, métricas, dependências, prioridade, custo e status. A execução é futura.

Prioridade 1: referências A/B, knots, priors e omissão individual de controles. Prioridade 2: decaimento, max_lag, Hill e hipótese de agregação. Prioridade 3: pooling, família, influência e interações selecionadas. Não executar produto cartesiano. Experimentos JOINT dependem de seus componentes individuais e de evidência diagnóstica; não são todos obrigatórios.

PRIOR-1 e PRIOR-2 mudam apenas a dispersão da média logarítmica do coeficiente pago, mantendo sua localização. Isso mantém a mediana nessa escala transformada, mas pode alterar média e cauda do efeito na escala original; não alegar média original fixa. PRIOR-3 é alternativa de família Student-t condicionada à revisão preditiva, não substituição automática. A alteração de EC truncada pode modificar sua média por truncamento; a mudança de slope fixo para lognormal muda flexibilidade, mesmo com mediana 1. A família normal de efeitos locais permite sinais negativos e não é apenas outra dispersão da lognormal.

Omissões de controles são testes de estresse: retirar um confundidor pode introduzir viés. Não tratar todo subconjunto como igualmente defensável. Promo e orgânico mantêm papéis próprios. Influência de mercados maiores, trajetórias opostas, extremidades e casos extremos usa critérios explícitos anteriores ao ajuste; mudanças de população ou período alteram o estimando e exigem comparação em suporte comum. Não remover dados automaticamente nem aplicar winsorization.

Por canal reportar média, mediana, intervalo de credibilidade de 90%, largura, diferença absoluta $\Delta=C_{ALT}-C_{REF}$ e diferença relativa $100\Delta/|C_{REF}|$ apenas acima de um piso substantivo previamente definido. Não há piso inventado: enquanto ele não for justificado, suprimir percentuais. Incluir probabilidades de ordenação, mudança de baseline, incerteza e erro de desenvolvimento, com atenção específica a Channel2 e Channel3.

Draws de modelos distintos não são amostras conjuntas por terem o mesmo índice. Uma comparação probabilística sob produto independente de posteriores pode ser calculada com amostragem independente e deve receber essa interpretação, sem fingir posterior conjunta identificada para a diferença causal. Não resumir robustez somente por ranking pontual.

Classificar a síntese como estável, moderadamente sensível, altamente sensível, inconclusiva ou não comparável segundo persistência das conclusões substantivas e incerteza, sem cortes percentuais arbitrários. Relatar todas as alternativas elegíveis e as falhas. Nunca reutilizar B para selecionar a versão que produz o melhor resultado.

## Integração, dependências e reprodução

A sequência executada foi: incorporação acadêmica 3.3/4.6; auditoria; especificação temporal; agregação e máscaras; diagnósticos; sensibilidade; síntese 3.5–3.7. Cada etapa consome a anterior. O Capítulo 4 foi congelado novamente depois da primeira tarefa.

Os YAMLs não são argumentos diretos de `ModelSpec`: contêm governança, referências e alternativas. Somente campos sob `model_spec` e patches validados devem ser convertidos por um futuro construtor. As posições e a ordem das coordenadas precisam coincidir com `InputData`.

Reprodução apenas da preparação, sem executar a EDA ou MCMC:

```bash
python -m pip install -r requirements-planning.txt
python scripts/prepare_planning.py
python scripts/render_experiment_matrix.py
python -m pytest -q
```

O script só escreve a base nacional e os três arquivos novos de holdout; a matriz é gerada separadamente. Não executa o notebook. A auditoria de fonte é estática, com hashes e campos da API em `docs/planejamento/meridian_api_audit.json`. Antes da modelagem: validar integração no ambiente fixado, isolamento do KPI, equivalência das máscaras, priors preditivas e plausibilidade dos controles/agregação. Essas são condições explícitas de passagem, não resultados empíricos omitidos.

Fontes técnicas consultadas: [especificação](https://developers.google.com/meridian/docs/advanced-modeling/model-spec), [knots](https://developers.google.com/meridian/docs/advanced-modeling/setting-knots), [holdout](https://developers.google.com/meridian/docs/advanced-modeling/holdout-observations), [configuração](https://developers.google.com/meridian/docs/user-guide/configure-model), [mídia](https://developers.google.com/meridian/docs/advanced-modeling/media-saturation-lagging), [priors](https://developers.google.com/meridian/docs/advanced-modeling/default-prior-distributions), [controles](https://developers.google.com/meridian/docs/advanced-modeling/control-variables), [diagnósticos](https://developers.google.com/meridian/docs/user-guide/model-diagnostics), [health checks](https://developers.google.com/meridian/docs/post-modeling/health-checks) e [fonte fixada](https://github.com/google/meridian/tree/02111531f8661373aa7b6ba31c316c67d72d1dd2). Páginas atuais podem mudar: compatibilidade de parâmetros foi conferida no commit, sem atualizar dependências históricas. Estes links técnicos não alteram a bibliografia da monografia.
