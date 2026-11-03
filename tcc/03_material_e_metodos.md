# 3 MATERIAL E MÉTODOS

## 3.1 Delineamento da pesquisa e questão científica

Esta pesquisa possui abordagem quantitativa, caráter aplicado e delineamento metodológico-computacional. Seu objeto é a aplicação do *Marketing Mix Modeling* (MMM) Bayesiano hierárquico por meio da biblioteca de código aberto Google Meridian, com ênfase nas implicações da granularidade geográfica para a mensuração de resultados associados à publicidade. O estudo utiliza dados sintéticos de demonstração disponibilizados pelo projeto Meridian, e não informações de campanhas efetivas de uma organização. Desse modo, trata-se de uma investigação observacional em ambiente simulado, na qual a interpretação dos efeitos estimados estará condicionada aos pressupostos do modelo, sem equivaler à validação experimental de causalidade (Sun et al., 2017; Google, [s. d.]a).

A pesquisa busca responder à seguinte questão: **em que medida a preservação da estrutura geotemporal dos dados altera as estimativas, a incerteza e a avaliação de um MMM Bayesiano hierárquico, em comparação com uma especificação construída a partir da agregação nacional?** A presença de mais observações no painel geográfico não será tratada como prova antecipada de maior precisão ou de melhor identificação causal. A comparação deverá examinar tanto benefícios potenciais quanto custos de complexidade, dependência da especificação e limitações de identificação.

O percurso empírico compreende duas fases. A primeira, já executada, consiste na análise exploratória dos dados (EDA), voltada à integridade do painel, às diferenças entre mercados, à dinâmica das exposições e à associação entre os preditores. Seus resultados são apresentados no Capítulo 4. A segunda consiste no desenho, na estimação e na avaliação dos modelos GEO e nacional, cujos procedimentos são aqui especificados e serão executados e documentados posteriormente. Esta distinção impede que parâmetros posteriores, retorno sobre investimento ou resultados da comparação de modelos sejam apresentados como descobertas já obtidas.

## 3.2 Dados, unidade observacional e variáveis

A base consiste em um painel balanceado com 40 mercados sintéticos (`Geo0` a `Geo39`) e 156 observações semanais por mercado, entre 25 de janeiro de 2021 e 15 de janeiro de 2024. Cada linha corresponde à combinação de um mercado com uma semana, perfazendo 6.240 registros. Os rótulos geográficos não representam municípios identificáveis, não havendo suporte para atribuir aos resultados características econômicas ou institucionais de regiões reais.

A variável-resposta é `conversions`, interpretada como quantidade sintética de conversões. A base inclui cinco canais pagos (`Channel0` a `Channel4`), cada qual descrito por impressões e gasto (`spend`); um canal orgânico (`Organic_channel0_impression`); população (`population`); dois índices candidatos a controles (`competitor_sales_control` e `sentiment_score_control`); e uma variável contínua de tratamento não midiático (`Promo`). Existe ainda um campo de receita por conversão, cuja eventual aplicação monetária dependerá da compatibilidade de unidades. As impressões representam exibições, e não alcance único; por isso, a modalidade do Meridian baseada em alcance e frequência não será ativada na especificação de referência. Os gastos não possuem unidade monetária comercial validada na documentação examinada.

**Tabela 1 – Caracterização e integridade do painel utilizado no estudo**

| Indicador | Resultado verificado |
|:--|--:|
| Mercados sintéticos | 40 |
| Semanas por mercado | 156 |
| Observações esperadas | 6.240 |
| Observações existentes | 6.240 |
| Pares mercado–semana distintos | 6.240 |
| Duplicidades de chave | 0 |
| Células ausentes | 0 |
| Completude do painel | 100,0% |

Fonte: elaboração própria.

Nota: indicadores da auditoria estrutural armazenada no notebook da EDA. As verificações se referem ao conjunto de regras programadas; completude não significa ausência de confundimento ou plena plausibilidade econômica.

## 3.3 Procedimentos da análise exploratória

A EDA foi desenvolvida em notebook Python consolidado, organizado em módulos de auditoria estrutural, síntese nacional, investigação temporal, decomposição geográfica da variância, distribuição dos investimentos, correlações, multicolinearidade e diagnósticos oficiais do Meridian. Os procedimentos foram planejados para distinguir evidências descritivas de condições necessárias, mas não suficientes, à inferência sobre efeitos publicitários.

Na primeira etapa, verificaram-se a cardinalidade das chaves de mercado e tempo, a presença de períodos ausentes, a unicidade dos registros, os valores faltantes, a validade dos domínios numéricos, o comportamento da população e a consistência entre impressões e gastos dos canais pagos. Para a descrição temporal, foram construídas séries nacionais por agregação semanal, medidas de tendência suavizada, decomposição STL com período aproximado de 52 semanas e funções de autocorrelação. Essas ferramentas caracterizam regularidades observacionais, sem confirmar mecanismos de sazonalidade ou o momento de ocorrência de efeitos causais.

A investigação geográfica distinguiu variabilidade entre mercados (*between*) e variabilidade dentro dos mercados (*within*). No painel balanceado, com $G=40$ mercados e $T=156$ semanas, a decomposição da variância populacional de uma variável $z_{g,t}$ foi representada por:

$$
\frac{1}{GT}\sum_{g=1}^{G}\sum_{t=1}^{T}(z_{g,t}-\bar z)^2
=\frac{1}{G}\sum_{g=1}^{G}(\bar z_{g\cdot}-\bar z)^2
+\frac{1}{GT}\sum_{g=1}^{G}\sum_{t=1}^{T}(z_{g,t}-\bar z_{g\cdot})^2.
$$

O primeiro termo do lado direito corresponde à variação das médias geográficas; o segundo, às oscilações das observações em torno da média do próprio mercado. Para examinar a variação que não é descrita por efeitos aditivos de mercado e semana, foi utilizada a transformação:

$$
\widetilde z_{g,t}
=z_{g,t}-\bar z_{g\cdot}-\bar z_{\cdot t}+\bar z.
$$

As parcelas associadas à identidade do mercado ($R^2_{\mathrm{GEO}}$), à semana ($R^2_{\mathrm{TIME}}$) e ao resíduo após a remoção dos dois fatores têm natureza **descritiva** e não constituem medidas de acurácia preditiva ou contribuição causal. As decomposições foram realizadas tanto nos valores originais quanto em intensidades por mil habitantes. A comparação das escalas procura evitar que diferenças de tamanho populacional sejam interpretadas automaticamente como diferenças estruturais de atuação publicitária.

Os canais pagos foram examinados quanto à participação acumulada no investimento, à composição interna de cada mercado (*media mix*), à distribuição territorial por canal e, principalmente, à atividade semanal. Esta última incluiu proporção de zeros, sequências de inatividade, variabilidade nas semanas positivas e contribuição da alternância entre presença e ausência para a variância *within*. Também foram calculadas correlações de Pearson sob quatro representações: série nacional semanal, painel bruto, desvios internos aos mercados e resíduos após remoção de mercado e semana. Os fatores de inflação da variância (VIF) foram obtidos de regressões auxiliares com intercepto e preditores padronizados, sem duplicar simultaneamente gastos e impressões de um mesmo canal.

Valores incomuns foram triados com critérios robustos de dispersão e inspecionados em escalas diferentes; nenhum registro foi removido apenas por se distinguir dos demais. Por fim, executaram-se as verificações exploratórias disponibilizadas pela versão 2.1.0 do Meridian, com reconciliação entre suas transformações internas e as estatísticas descritivas do projeto. Essas verificações não constituem estimação da posterior dos efeitos de mídia.

Complementarmente, a Seção executável 08 do notebook investigou estacionariedade, tendências locais, persistência, estabilidade sazonal e mudanças entre janelas. Aplicaram-se os testes ADF, cuja hipótese nula é a presença de raiz unitária, e KPSS, cuja hipótese nula é a estacionariedade em torno dos termos determinísticos especificados. Ambos foram examinados com constante e com constante acrescida de tendência linear, no agregado nacional e por mercado, em níveis, por mil habitantes e em primeiras diferenças. No ADF, as defasagens foram selecionadas por AIC, com máximo de Schwert limitado pelos graus de liberdade; no KPSS, utilizou-se seleção automática da largura de banda. Adotou-se nível de significância de 5%, preservando os avisos e os limites tabulados dos p-valores do KPSS. Para cada família de 40 testes geográficos, definida pelo teste, especificação determinística e escala, empregou-se o ajuste de Benjamini–Yekutieli, com tratamento conservador dos p-valores limitados. Não rejeitar uma hipótese não foi interpretado como comprová-la, e as primeiras diferenças constituíram apenas uma ferramenta diagnóstica, sem alteração da resposta prevista para o MMM.

As tendências foram descritas pela inclinação robusta de Theil–Sen, normalizada pela média de cada série e multiplicada pelos 155 intervalos semanais. Utilizou-se uma faixa descritiva de estabilidade de ±1%, acompanhada de sensibilidade a 0% e 5%. Compararam-se também as médias das primeiras e últimas 26 semanas, distinguindo o saldo nacional da compensação de movimentos locais positivos e negativos. Esses procedimentos não constituem testes de tendência causal, nem permitem equiparar interceptos geográficos a tendências específicas de cada mercado.

A persistência foi examinada por ACF nas defasagens de 1, 4, 8, 13, 26 e 52 semanas e por PACF do KPI até a defasagem 13, estimada pelo método de Yule–Walker com denominador de máxima verossimilhança. Nas séries de mídia, conservaram-se as semanas com exposição nula e distinguiram-se impressões, gastos e atividade. Para avaliar a estabilidade do padrão sazonal, compararam-se três blocos consecutivos de 52 semanas, em nível e após remoção de tendência linear, no país e por mercado; esses blocos não equivalem a anos civis. A instabilidade foi descrita por médias e desvios das janelas iniciais e finais de 13 e 26 semanas, por blocos de 52 semanas e por estatísticas móveis de 13 semanas completas. Não se realizaram testes formais de quebra estrutural nem se atribuíram eventos comerciais reais às oscilações. A autocorrelação observacional, a persistência das exposições, o adstock causal e a dependência residual de um futuro modelo foram tratados como conceitos distintos.

## 3.4 Especificação proposta para o MMM geográfico

A modelagem subsequente utilizará a estrutura hierárquica geo-level do Meridian, com interceptos associados aos mercados e ao tempo, covariáveis de controle, mídia orgânica, tratamentos não midiáticos e transformações de mídia paga para representar persistência e saturação. Para fins de exposição conceitual, o resultado transformado pode ser descrito por:

$$
Y^{*}_{g,t}=\mu_t+\tau_g+\boldsymbol\gamma^{\mathsf T}\mathbf Z^{*}_{g,t}
+\delta P^{*}_{g,t}
+\sum_{m=0}^{4}\beta_{g,m}\,f_m\!\left(\mathbf X^{*}_{g,1:t};\boldsymbol\theta_m\right)
+\beta_{g,O}f_O\!\left(\mathbf O^{*}_{g,1:t}\right)+\varepsilon_{g,t}.
$$

Nessa representação, $\mu_t$ denota a componente temporal de base, $\tau_g$ representa diferenças persistentes entre mercados, $\mathbf Z_{g,t}$ agrupa controles, $P_{g,t}$ representa `Promo`, e as funções $f_m$ descrevem a transformação não linear das exposições ao longo do tempo. Os termos $\beta_{g,m}$ evidenciam a possibilidade de heterogeneidade geográfica e compartilhamento hierárquico de informação. **A expressão é uma simplificação expositiva**, não uma substituição das equações, transformações de escala e parametrizações da versão oficial do Meridian (Google, [s. d.]a).

A variável `population` será preservada no carregamento geo-level de acordo com as regras da biblioteca. Não será aplicado indiscriminadamente um segundo escalonamento por mil habitantes aos dados que o Meridian transforma internamente: a normalização por população realizada na EDA teve finalidade descritiva. Impressões constituirão a medida principal de exposição nos cinco canais pagos; gastos serão mantidos para interpretação das decisões de investimento, quando suas unidades forem compatíveis com o estimando.

A hipótese de heterogeneidade dos efeitos de mídia será avaliada por meio das distribuições posteriores de efeitos entre mercados, e não inferida diretamente das diferenças de nível de conversão. A seleção dos controles exigirá justificativa de seu possível papel como confundidores pré-tratamento e exame de relações entre demanda esperada, investimento, exposição e resultado. `competitor_sales_control` e `sentiment_score_control` serão tratados como candidatos cuja interpretação causal precisa ser defendida, e `Promo` conservará seu caráter contínuo. Não se assumirá que um nome de coluna basta para determinar sua posição causal. Especificações alternativas poderão avaliar a sensibilidade dos resultados à inclusão desses fatores (Chen et al., 2018).

## 3.5 Dinâmica publicitária, efeitos temporais e distribuições a priori

O modelo de referência considerará *adstock* geométrico para representar persistência das exposições e função de Hill para modelar saturação, respeitando a ordem de transformações documentada na configuração efetivamente instalada. O *adstock* permite que exposição em semanas anteriores contribua para o estoque efetivo de mídia, com pesos de decaimento; a função de Hill representa resposta não linear cuja magnitude e inclinação dependem de parâmetros estimados. As correlações exploratórias com defasagens de zero a oito semanas não serão interpretadas como estimativas da duração real do efeito publicitário (Google, [s. d.]a; Google, [s. d.]b).

Os interceptos temporais do Meridian são construídos com parâmetros associados a *knots*. O número e a localização desses pontos afetam a flexibilidade da tendência de base e podem interferir na separação estatística entre variação de demanda e contribuição de mídia. O notebook registrou uma especificação **provisória de EDA** com 156 *knots* e defasagem máxima de oito semanas; essa configuração não foi validada como modelo final. O protocolo de estimação deverá congelar e documentar a escolha de *knots*, `max_lag`, ordem Hill/*adstock*, distribuição de efeitos e demais parâmetros antes da leitura dos resultados de contribuição.

As distribuições a priori serão identificadas por família, escala, hiperparâmetros e estimando correspondente. Como a base é sintética e não incorpora conhecimento empresarial verificável, priors padrão não serão tratados como crenças empiricamente calibradas sobre um canal real. Serão consideradas verificações preditivas da prior e testes de sensibilidade que contrastem especificações justificadas. Alterações serão motivadas por hipóteses ou problemas diagnósticos, e não pela intenção de maximizar ROI ou produzir rankings desejados. O estimando primário será a contribuição incremental em conversões sintéticas, expressa com incerteza posterior; a interpretação econômica de ROI e mROI ficará condicionada à verificação das unidades de receita por conversão e de gasto (Gelman et al., 2013; Google, [s. d.]b).

## 3.6 Comparação entre níveis geográfico e nacional

O confronto central da pesquisa será realizado entre um modelo com 40 mercados e um modelo nacional com uma série de 156 semanas. No segundo caso, conversões, gastos e impressões serão agregados por soma semanal, sem somar novamente a população repetida a cada semana. A agregação de controles expressos em índices será decidida conforme sua natureza, com documentação do critério adotado, tal como média ponderada pela população quando substantivamente justificável. `Promo` e receita por conversão exigirão tratamento análogo, compatível com as unidades e com o papel previsto no modelo. Não será aplicada a mesma operação de agregação a colunas semanticamente diferentes.

As duas especificações utilizarão o mesmo horizonte temporal, canais comparáveis e hipóteses de controles explicitadas. A comparação quantitativa de predições ocorrerá em unidades nacionais semanais quando apropriado: previsões do modelo GEO serão agregadas entre mercados, enquanto as previsões do modelo nacional já estarão nessa escala. Não se confrontará diretamente uma métrica computada sobre 6.240 células geográficas com outra computada sobre 156 totais nacionais sem adequação do objeto de avaliação.

A documentação oficial admite diferenças importantes entre modelos multi-GEO e de um único mercado, sobretudo na flexibilidade dos interceptos temporais. Serão registrados os *knots* efetivamente usados e examinadas alternativas compatíveis de flexibilidade; uma diferença de desempenho não poderá ser atribuída exclusivamente à geografia se também decorrer de uma estrutura temporal diferente (Google, [s. d.]c).

## 3.7 Estratégia de avaliação e diagnósticos futuros

A validação será organizada em duas perguntas complementares. Para examinar a capacidade interna de reprodução de observações geográficas, será proposta uma máscara de *holdout* distribuída entre mercados e semanas, com fração semelhante de observações reservadas para cada mercado e período. Para permitir confronto nacional em unidades comparáveis, será desenvolvido adicionalmente um desenho de avaliação temporal comum aos dois modelos, com semanas de teste distribuídas no período, evitando grandes blocos contíguos no final da série. A viabilidade desse segundo desenho dependerá da disponibilidade de observações de treinamento suficientes para os interceptos temporais e de uma parametrização coerente de *knots*; ambas as máscaras serão explicitadas e congeladas antes da estimação. Não se confundirão os resultados das duas tarefas de validação, que respondem a perguntas diferentes (Google, [s. d.]d).

As medidas de avaliação poderão compreender erro absoluto médio (MAE), raiz do erro quadrático médio (RMSE) e erro percentual absoluto ponderado (wMAPE), acompanhado de análise de denominadores, além de cobertura e amplitude de intervalos preditivos quando disponíveis. A acurácia em dados reservados será examinada separadamente da capacidade de identificar efeitos incrementais; previsão adequada não demonstra, por si, correção causal dos parâmetros de mídia.

A estimação Bayesiana por MCMC deverá ser acompanhada de análise de convergência e qualidade numérica, incluindo $\widehat R$, tamanho efetivo da amostra, divergências, traçados das cadeias e verificações preditivas da posterior. A investigação estatística deverá explorar sensibilidade a priors, *knots*, transformações de mídia e controles, dando atenção especial à atividade intermitente de `Channel2` e à exposição quase contínua de `Channel3`. Os diagnósticos serão avaliados antes de qualquer recomendação de contribuição por canal, retorno ou alocação de investimento. Resultados instáveis ou inconclusivos serão apresentados como tais, sem seleção por conveniência de uma configuração.

## 3.8 Rastreabilidade, limitações e escopo

A pesquisa manterá os dados originais separados dos painéis processados, além de registrar versões do código, biblioteca, configurações, máscaras de avaliação, sementes, artefatos de amostragem e saídas gráficas e numéricas. A EDA foi documentada no notebook consolidado `01_EDA_COMPLETA.ipynb`. Esta redação foi produzida com base nas saídas de tabelas e figuras **já armazenadas nesse notebook**; não constitui reexecução integral do código sobre os arquivos originais, os quais devem permanecer disponíveis para auditoria independente. A validação em sessão real do Google Colab figurava como pendência na documentação examinada.

As limitações centrais incluem a origem sintética da base, as denominações genéricas dos canais, as unidades monetárias não demonstradas, a ausência de alcance único e frequência, o curto horizonte para avaliar recorrência anual e a falta de observação direta do mecanismo que gerou decisões de publicidade. As conclusões da EDA são descritivas, e as futuras estimativas do MMM serão condicionais às hipóteses e à especificação. Nenhuma conclusão será generalizada automaticamente para mercados reais.

