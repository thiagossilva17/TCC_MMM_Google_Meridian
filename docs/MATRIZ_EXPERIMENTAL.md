# Matriz experimental integrada

Gerada de `configs/sensibilidades.yaml`; não editar valores manualmente. Todos os ajustes são futuros. Nove cenários essenciais; uma linha pareada envolve dois modelos. Os demais cenários são ampliados/condicionais, não uma busca fatorial obrigatória.

| ID | Família | Modelo | Referência | Prioridade | Custo | Essencial | Estado |
|---|---|---|---|---|---|---|---|
| BASE-A | BASE | GEO-A | None | 1 | medium | True | not_executed |
| BASE-B | BASE | paired | None | 1 | medium | True | not_executed |
| TIME-N1 | TIME | NAT | BASE-B | 1 | medium | True | not_executed |
| TIME-GEO26 | TIME | GEO | BASE-B | 1 | medium | True | not_executed |
| TIME-GEO52 | TIME | GEO | BASE-B | 1 | medium | False | not_executed |
| TIME-NAT4 | TIME | NAT | BASE-B | 1 | medium | True | not_executed |
| TIME-NAT8 | TIME | NAT | BASE-B | 1 | medium | False | not_executed |
| TIME-AKS | TIME | paired | BASE-B | 3 | high | False | conditional |
| PRIOR-1 | PRIOR | paired | BASE-B | 1 | medium | True | not_executed |
| PRIOR-2 | PRIOR | paired | BASE-B | 1 | medium | True | not_executed |
| PRIOR-3 | PRIOR | paired | BASE-B | 3 | medium | False | conditional |
| CTRL-COMP | CTRL | paired | BASE-B | 1 | medium | True | not_executed |
| CTRL-SENT | CTRL | paired | BASE-B | 1 | medium | True | not_executed |
| CTRL-AGG | CTRL | NAT | BASE-B | 2 | medium | False | not_executed |
| ADSTOCK-BIN | ADSTOCK | paired | BASE-B | 2 | medium | False | not_executed |
| LAG-4 | LAG | paired | BASE-B | 2 | medium | False | not_executed |
| LAG-10 | LAG | paired | BASE-B | 2 | medium | False | not_executed |
| HILL-EC | HILL | paired | BASE-B | 2 | medium | False | not_executed |
| HILL-SLOPE | HILL | paired | BASE-B | 2 | medium | False | not_executed |
| HILL-ORDER | HILL | paired | BASE-B | 2 | medium | False | not_executed |
| GEO-POOL | GEO | GEO | BASE-B | 3 | medium | False | not_executed |
| GEO-FAMILY | GEO | GEO | BASE-B | 3 | medium | False | conditional |
| INFLUENCE-GEO | INFLUENCE | paired | BASE-B | 3 | medium | False | not_executed |
| INFLUENCE-TREND | INFLUENCE | paired | BASE-B | 3 | medium | False | conditional |
| INFLUENCE-EDGE | INFLUENCE | paired | BASE-B | 3 | medium | False | not_executed |
| INFLUENCE-EXTREME | INFLUENCE | paired | BASE-B | 3 | medium | False | conditional |
| JOINT-TIME-CTRL | JOINT | paired | BASE-B | 3 | high | False | not_executed |
| JOINT-LAG-DECAY | JOINT | paired | BASE-B | 3 | high | False | not_executed |
| JOINT-PRIOR-POOL | JOINT | GEO | BASE-B | 3 | high | False | not_executed |

## BASE-A

- **hypothesis**: Internal reconstruction with per-week temporal effects
- **alternative**: {"prior": "PRIOR-0", "temporal": "GEO-K156"}
- **factor**: BASE
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-A
- **development_ref**: None
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## BASE-B

- **hypothesis**: Compare geographic hierarchy and aggregation with matched knot positions
- **alternative**: {"GEO": "GEO-K13", "NAT": "NAT-K13", "prior": "PRIOR-0"}
- **factor**: BASE
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## TIME-N1

- **hypothesis**: National default as rigid temporal benchmark
- **alternative**: {"NAT": "NAT-K1"}
- **factor**: TIME
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## TIME-GEO26

- **hypothesis**: Does temporal flexibility change prediction or contribution?
- **alternative**: {"temporal": "GEO-K26"}
- **factor**: TIME
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## TIME-GEO52

- **hypothesis**: Does temporal flexibility change prediction or contribution?
- **alternative**: {"temporal": "GEO-K52"}
- **factor**: TIME
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## TIME-NAT4

- **hypothesis**: Does temporal flexibility change prediction or contribution?
- **alternative**: {"temporal": "NAT-K4"}
- **factor**: TIME
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## TIME-NAT8

- **hypothesis**: Does temporal flexibility change prediction or contribution?
- **alternative**: {"temporal": "NAT-K8"}
- **factor**: TIME
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## TIME-AKS

- **hypothesis**: Data-driven knots under verified training-only selection
- **alternative**: {"temporal": "AKS-OPTIONAL"}
- **factor**: TIME
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## PRIOR-1

- **hypothesis**: More concentrated hierarchical log-media coefficient prior
- **alternative**: {"prior_patch": {"beta_m": {"family": "Normal", "loc": 0.0, "scale": 0.5}}}
- **factor**: PRIOR
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## PRIOR-2

- **hypothesis**: More dispersed hierarchical log-media coefficient prior
- **alternative**: {"prior_patch": {"beta_m": {"family": "Normal", "loc": 0.0, "scale": 2.0}}}
- **factor**: PRIOR
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## PRIOR-3

- **hypothesis**: Alternative coefficient prior family with matched log-space variance
- **alternative**: {"prior_patch": {"beta_m": {"df": 5.0, "family": "StudentT", "loc": 0.0, "scale": 0.7745966692414834}}}
- **factor**: PRIOR
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## CTRL-COMP

- **hypothesis**: Stress test omission; not automatically a valid causal model
- **alternative**: {"remove_control": "competitor_sales_control"}
- **factor**: CTRL
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## CTRL-SENT

- **hypothesis**: Stress test omission; not automatically a valid causal model
- **alternative**: {"remove_control": "sentiment_score_control"}
- **factor**: CTRL
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## CTRL-AGG

- **hypothesis**: Dependence on index aggregation assumption
- **alternative**: {"aggregate_indices": "unweighted_mean"}
- **factor**: aggregation assumption
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## ADSTOCK-BIN

- **hypothesis**: Alternative lag weight shape
- **alternative**: {"model_spec_patch": {"adstock_decay_spec": "binomial"}}
- **factor**: ADSTOCK
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## LAG-4

- **hypothesis**: Dependence on finite memory horizon
- **alternative**: {"model_spec_patch": {"max_lag": 4}}
- **factor**: LAG
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## LAG-10

- **hypothesis**: Dependence on finite memory horizon
- **alternative**: {"model_spec_patch": {"max_lag": 10}}
- **factor**: LAG
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## HILL-EC

- **hypothesis**: Half-saturation prior sensitivity
- **alternative**: {"prior_patch": {"ec_m": {"family": "TruncatedNormal", "high": 10.0, "loc": 0.8, "low": 0.1, "scale": 0.4}}}
- **factor**: HILL
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## HILL-SLOPE

- **hypothesis**: Allow non-unit slope with median one
- **alternative**: {"prior_patch": {"slope_m": {"family": "LogNormal", "loc": 0.0, "scale": 0.3}}}
- **factor**: HILL
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## HILL-ORDER

- **hypothesis**: Transformation order sensitivity
- **alternative**: {"model_spec_patch": {"hill_before_adstock": true}}
- **factor**: HILL
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## GEO-POOL

- **hypothesis**: Stronger partial pooling
- **alternative**: {"prior_patch": {"eta_m": {"family": "HalfNormal", "scale": 0.5}}}
- **factor**: GEO
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## GEO-FAMILY

- **hypothesis**: Normal effects allow negative local coefficients and change support
- **alternative**: {"model_spec_patch": {"media_effects_dist": "normal"}, "prior_patch": {"beta_m": {"family": "HalfNormal", "scale": 1.0}}}
- **factor**: joint family/support change, not dispersion-only
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## INFLUENCE-GEO

- **hypothesis**: Influence of largest population; fixed rule, not best/worst model outcome
- **alternative**: {"estimand_changed": true, "reaggregate": true, "remove_geos": "one largest population; lexical tie break"}
- **factor**: INFLUENCE
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## INFLUENCE-TREND

- **hypothesis**: Influence of opposite descriptive trajectories
- **alternative**: {"estimand_changed": true, "subset_rule": "opposite to national in frozen tc_geo_trend_profile.csv"}
- **factor**: INFLUENCE
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## INFLUENCE-EDGE

- **hypothesis**: Missing prehistory and edge effects
- **alternative**: {"estimand_changed": true, "exclude_evaluation_weeks": "first 10 and last 10, report separately", "training_unchanged": true}
- **factor**: INFLUENCE
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## INFLUENCE-EXTREME

- **hypothesis**: Influence of already flagged extremes
- **alternative**: {"action": "case-by-case leave-one-out after predeclared case list; no winsorization", "cases_ref": "outputs/tables/outlier_case_review.csv", "estimand_changed": true}
- **factor**: INFLUENCE
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: []
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## JOINT-TIME-CTRL

- **hypothesis**: Temporal flexibility and omitted control interaction
- **alternative**: {"combine": ["TIME-GEO26", "CTRL-COMP"]}
- **factor**: JOINT
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: ["TIME-GEO26", "CTRL-COMP"]
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## JOINT-LAG-DECAY

- **hypothesis**: Lag horizon and decay shape interaction
- **alternative**: {"combine": ["LAG-10", "ADSTOCK-BIN"]}
- **factor**: JOINT
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: ["LAG-10", "ADSTOCK-BIN"]
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review

## JOINT-PRIOR-POOL

- **hypothesis**: Mean-prior and pooling interaction
- **alternative**: {"combine": ["PRIOR-1", "GEO-POOL"]}
- **factor**: JOINT
- **fixed**: all except declared factor; data, masks and versions fixed unless influence explicitly changes estimand
- **data_ref**: AGG-V1
- **mask_ref**: HOLDOUT-B
- **development_ref**: DEV-B
- **estimand**: incremental synthetic conversions under declared counterfactual
- **metrics_ref**: STABILITY-V1
- **diagnostics_ref**: DIAG-V1
- **depends_on**: ["PRIOR-1", "GEO-POOL"]
- **eligibility**: MCMC-GATE, temporal rank, leakage invariance, matched scale and counterfactual; prior predictive review
