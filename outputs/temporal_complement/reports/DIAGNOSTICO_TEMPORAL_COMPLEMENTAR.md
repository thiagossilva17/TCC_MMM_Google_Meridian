# Diagnóstico temporal complementar

Execução iniciada em 2026-11-01T20:27:30.173898+00:00.

Objetivo: investigar propriedades temporais nacionais, geográficas e de mídia para orientar a futura comparação GEO × nacional.

Métodos: ADF com AIC e máximo de Schwert limitado por graus de liberdade; KPSS com bandwidth automático (Hobijn), ambos em c/ct; níveis, por mil habitantes e diferenças. BY por família de 40 GEOs, com p-valores limitados tratados conservadoramente. ACF não ajustada sem FFT; PACF ywm até 13; Theil–Sen com faixa ±1% e sensibilidade 0/5%; janelas 13/26 e três blocos de 52 semanas. Parâmetros e warnings completos nos CSVs e manifesto.

## Estacionariedade nacional e geográfica

**Pergunta:** há sinais de persistência incompatíveis com um nível ou uma tendência estável? **Método:** ADF/KPSS pareados, conforme especificações acima. **Resultado nacional em nível:** c: ADF p=6.287e-23; KPSS p=0.0471 (interpolated); resultado misto ou inconclusivo; ct: ADF p=3.676e-20; KPSS p=0.1 (p_ge_0.10); compatível com estacionariedade sob esta especificação.

**Resultado geográfico:**

| scale      | test   | regression   |   n_geos |   reject_unadjusted |   reject_BY |
|:-----------|:-------|:-------------|---------:|--------------------:|------------:|
| difference | ADF    | c            |       40 |                  40 |          40 |
| difference | ADF    | ct           |       40 |                  40 |          40 |
| difference | KPSS   | c            |       40 |                   6 |           0 |
| difference | KPSS   | ct           |       40 |                  22 |           0 |
| level      | ADF    | c            |       40 |                  40 |          40 |
| level      | ADF    | ct           |       40 |                  40 |          40 |
| level      | KPSS   | c            |       40 |                   3 |           0 |
| level      | KPSS   | ct           |       40 |                   0 |           0 |
| per_1000   | ADF    | c            |       40 |                  40 |          40 |
| per_1000   | ADF    | ct           |       40 |                  40 |          40 |
| per_1000   | KPSS   | c            |       40 |                   3 |           0 |
| per_1000   | KPSS   | ct           |       40 |                   0 |           0 |

**Interpretação e limites:** as contagens são diagnósticos correlacionados, não 40 experimentos. Ajuste BY é conservador; limites KPSS não são p-valores exatos. Dividir por população constante em um GEO muda a escala, não a dinâmica temporal. Não rejeição não comprova a hipótese.

**Implicação para MMM:** investigar baseline, controles e resíduos futuros. Nenhum teste exige automaticamente diferenciar a resposta, nem constitui condição geral de uso do Meridian. Tabelas: `tc_stationarity_national.csv`, `tc_stationarity_geo.csv`, `tc_stationarity_summary.csv`.

## Tendências específicas e compensação

**Pergunta:** a tendência nacional representa os mercados? **Método:** Theil–Sen normalizado e janelas de 26 semanas. **Resultado:** direção nacional alta, mudança robusta de 3.69% da média ao longo da amostra; 23/40 mercados na mesma categoria e 15/40 em direção oposta (faixa ±1%). A soma das diferenças de médias finais–iniciais é 16,320,348.70 conversões semanais; componentes positivos 27,322,297.60 e negativos -11,001,948.90. A compensação descritiva é 57.4%, definida como 1−|saldo|/soma de magnitudes. Cinco mercados concentram 34.0% dessas magnitudes (Geo28, Geo32, Geo31, Geo35, Geo39).

**Interpretação:** saldo nacional e trajetórias locais respondem a perguntas diferentes. A comparação por mil habitantes está no perfil; população fixa por GEO mantém a direção normalizada. **Limites:** limiar descritivo, sem teste de tendência causal; janelas e suavização afetam o resumo. Sensibilidade de limiares em `tc_geo_trend_summary.csv`.

**Implicação:** distinguir interceptos GEO, baseline compartilhado e possíveis tendências locais no desenho futuro; não foram implementadas tendências no MMM. Evidências: `tc_geo_trend_profile.csv`, `tc_geo_trends.png`.

## Persistência do KPI, mídia e controles

**Pergunta:** quanto a observação atual se parece com seu próprio passado? **Método:** ACF/PACF e calendário completo. **Resultado:** KPI nacional ACF(1) histórica 0.008, ACF(52) 0.032; ACF(1) das diferenças -0.528. Channel2: ACF(1) nacional 0.236, mediana GEO 0.046; maior sequência local zero 27 semanas; Channel3: ACF(1) nacional 0.310, mediana GEO 0.090; maior sequência local zero 2 semanas.

**Interpretação:** a comparação em diferenças muda o objeto; autocorrelação negativa pode ser induzida pela própria diferenciação. A agenda de mídia tem persistência distinta da resposta. A quase continuidade do Channel3 e as lacunas do Channel2 afetam o suporte, mas não demonstram duração do efeito nem experimento natural. Os gastos podem espelhar impressões por construção; não são evidência independente.

**Limites:** 104 pares no lag 52; bandas e p-valores independentes não foram usados. **Implicação:** avaliar identificabilidade e sensibilidade do adstock no modelo futuro; autocorrelação residual só poderá ser diagnosticada após estimação. Artefatos: `tc_temporal_acf_summary.csv`, `tc_kpi_pacf.csv`, `tc_media_temporal_persistence.csv`, `tc_geo_media_persistence.csv`, `tc_media_persistence_summary.csv`, `tc_media_persistence.png`.

## Sazonalidade e estabilidade entre ciclos

**Pergunta:** o padrão anual é repetível? **Método:** comparação de três blocos de 52 semanas em nível e após tendência linear. **Resultado:** correlações nacionais após detrendização: 1–2: -0.120, 2–3: 0.222, 1–3: 0.036; mediana GEO das três comparações 0.027. A força sazonal da STL histórica é 0.503, um resumo descritivo.

**Leitura conjunta:** a STL fornece uma componente periódica condicionada ao período escolhido, evidência descritiva favorável à exploração de sazonalidade. Correlações pequenas ou negativas entre blocos enfraquecem a hipótese de um formato anual estável, mesmo quando a força STL é alta. Três ciclos tornam inconclusiva uma afirmação geral de presença ou ausência sazonal.

**Limites:** ano civil não equivale a 52 semanas; a STL é exploratória e sofre efeitos de borda. Nem ACF anual baixa prova ausência, nem componente STL prova causa. Não atribuímos datas comerciais reais aos dados sintéticos. **Implicação:** comparar flexibilidades do baseline e validar fora da amostra no futuro. Artefatos: `tc_seasonality_diagnostic.csv`, `tc_seasonality_summary.csv`, `tc_seasonality_stability.png`.

## Instabilidade temporal

**Pergunta:** houve alteração sustentada do comportamento? **Método:** janelas de 13/26 semanas, blocos de 52 e estatísticas móveis; os diagnósticos históricos de mudanças semanais permanecem em `outputs/tables/kpi_level_changes.csv`. **Resultado:** primeiras versus últimas 26 semanas no país: mudança da média 3.86% da média global, razão de desvios 0.917. Entre GEOs, mudança relativa da média varia de -27.77% a 31.45%.

**Interpretação:** a agregação pode amortecer alterações locais. Médias e dispersões resumem dimensões distintas. **Limites:** comparações descritivas, dependentes das janelas; não localizam nem confirmam uma quebra estrutural e não identificam eventos reais. **Implicação:** avaliar estabilidade por janela e resíduos após estimar o MMM, preservando agora todos os extremos. Evidências: `tc_instability_windows.csv`, `tc_rolling_statistics.csv`, `tc_instability_rolling.png`.

## Integração, limites e próximos passos

A EDA histórica já demonstrou heterogeneidade de níveis e exposições. Os diagnósticos novos acrescentam a dimensão temporal sem atribuir efeitos à mídia. Interceptos GEO representam diferenças de nível; efeitos temporais compartilhados representam movimentos comuns; tendências locais exigem hipótese própria. Não se presume que um termo substitua o outro.

No desenho científico futuro: documentar candidatos a controles e sua posição causal; comparar flexibilidades dos knots; avaliar identificabilidade de adstock diante da persistência das exposições; harmonizar tarefas GEO × nacional; planejar holdout temporal, diagnóstico residual e sensibilidade das contribuições. Nenhum desses parâmetros foi escolhido definitivamente nesta seção, e nenhum modelo MMM foi estimado.

Limitações transversais: dados sintéticos, 156 semanas, 40 mercados dependentes, testes com poder limitado, múltiplas comparações, três ciclos anuais e ausência de experimento causal. Resultados exploratórios não são validação de recuperação dos efeitos geradores. A validação na interface real do Colab permanece pendente.

## Artefatos desta execução

- `outputs/temporal_complement/tables/tc_stationarity_national.csv`
- `outputs/temporal_complement/tables/tc_stationarity_geo.csv`
- `outputs/temporal_complement/tables/tc_stationarity_summary.csv`
- `outputs/temporal_complement/tables/tc_geo_trend_profile.csv`
- `outputs/temporal_complement/tables/tc_geo_trend_summary.csv`
- `outputs/temporal_complement/figures/tc_geo_trends.png`
- `outputs/temporal_complement/tables/tc_temporal_acf_summary.csv`
- `outputs/temporal_complement/tables/tc_kpi_pacf.csv`
- `outputs/temporal_complement/tables/tc_media_temporal_persistence.csv`
- `outputs/temporal_complement/tables/tc_geo_media_persistence.csv`
- `outputs/temporal_complement/tables/tc_media_persistence_summary.csv`
- `outputs/temporal_complement/figures/tc_media_persistence.png`
- `outputs/temporal_complement/tables/tc_seasonality_diagnostic.csv`
- `outputs/temporal_complement/tables/tc_seasonality_summary.csv`
- `outputs/temporal_complement/figures/tc_seasonality_stability.png`
- `outputs/temporal_complement/tables/tc_instability_windows.csv`
- `outputs/temporal_complement/tables/tc_rolling_statistics.csv`
- `outputs/temporal_complement/figures/tc_instability_rolling.png`