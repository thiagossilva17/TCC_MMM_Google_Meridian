# Validação da EDA no Google Colab

**Validação concluída quanto ao conteúdo.** As 129 tabelas históricas e os 15 CSVs temporais foram reproduzidos. A diferença detectada em `outlier_coincidence.csv` se restringiu à ordem de linhas empatadas. O [registro anterior do Colab](COLAB_VALIDATION.md) documenta a situação anterior a esta execução.

## Ambiente e execução

| Item | Registro |
|---|---|
| Data | 18 de novembro de 2026, início às 23:23:34 UTC e término da seção 08 às 23:26:12 UTC |
| Repositório de referência | `007f487d9f541c34a43395412c9637254bd65c04` |
| Ambiente | Google Colab, Linux x86-64 com glibc 2.35, Python 3.12.13, CPU e backend JAX |
| Meridian | `2.1.0` no commit `02111531f8661373aa7b6ba31c316c67d72d1dd2` |
| Bibliotecas científicas | JAX e jaxlib `0.12.0.1`, dm-tree `0.1.10`, TensorFlow `2.21.0`, TFP Nightly `0.26.0.dev20260130`, NumPy `2.3.5`, pandas `2.2.3`, SciPy `1.17.0`, statsmodels `0.14.6`, Matplotlib `3.10.8` |
| Notebook e testes | nbformat `5.10.4`, nbclient `0.10.4`, pytest `8.4.2` |
| Executor | `scripts/execute_notebook.py --mode full --engine inprocess`, cópia isolada `validation_runs/8epfbe25` |

O executor concluiu as seções 00–08 com código de saída `0`. A cópia de referência ficou limpa. O manifesto do Meridian registra apenas o grupo `prior`, gerado automaticamente no diagnóstico exploratório, e `posterior_sampled: false`. Esta validação cobre a execução no serviço Colab pelo modo `inprocess`. O ajuste GEO pertence à etapa seguinte. [Executor](../scripts/execute_notebook.py)

O pacote de evidências é `VALIDACAO_EDA_COLAB.zip`, com SHA-256 `98eae2535c5289b548624542fd55239aaf5bcf6d1505699e62bece040d942d23`. Ele contém `relatorios/ambiente.json`, `relatorios/versoes_instaladas.txt`, `relatorios/execucao.json`, os logs de integridade e execução, `relatorios/comparacao.json`, os manifestos das etapas, o notebook executado e os ZIPs de resultados.

## Resultados e ressalvas

| Verificação | Resultado |
|---|---|
| Integridade da base bruta e do painel | SHA-256 conferidos. O painel preserva 6.240 linhas, 40 GEOs e 156 semanas. |
| Testes de integridade no Colab | 7 passaram, 2 falhas conhecidas, 0 falhas inesperadas. |
| Tabelas históricas | 129/129 equivalentes em conteúdo. O comparador posicional da execução original registrou 128/129. |
| CSVs temporais | 15/15 equivalentes. |

As duas falhas de `test_migrated_hashes` e `test_academic_preservation` apontam para a mesma divergência em `tcc/01_introducao.md`. Os manifestos esperavam `04bc9a7320cfa8f90c6053119198cf3483047d501c4eaf13cc9db3890166634e`, relativo à versão anterior do capítulo. O commit executado tem `93a3faa368dc34e0a7d4af24f764efc095a1c4bb2fd71d5aa7e61d79030198cb`. A execução manteve os dois registros como ressalvas de proveniência.

## Equivalência de `outlier_coincidence.csv`

A comparação usou o [CSV histórico](../outputs/tables/outlier_coincidence.csv) no commit auditado e o CSV homônimo em `execucao/EDA_RESULTS.zip`, no caminho interno `outputs/tables/outlier_coincidence.csv`.

- Os cabeçalhos são idênticos. Ambas as versões têm 2.918 linhas, com `geo`, `time` e `variables` em texto e `count` lido como `int64`. As datas são válidas e os campos estão preenchidos.
- Cada linha completa foi contada como uma tupla das quatro colunas. A comparação verificou cada multiplicidade, identificou 2.918 tuplas distintas em cada arquivo e encontrou zero ocorrências ausentes ou adicionais. Uma segunda checagem, após ordenar pelas quatro colunas, confirmou igualdade exata.
- Há 2.866 posições com linhas diferentes, sempre entre registros com o mesmo `count`. Por exemplo, `Geo36` em `2023-09-11`, com `count=11`, aparece na 3ª posição histórica e na 7ª no Colab.
- O `outliers.csv` de entrada é idêntico byte a byte. O gerador agrupa por GEO e semana e ordena apenas por `count` decrescente. O `quicksort` padrão do pandas permite permutar empates. A aplicação desse trecho em memória sobre a entrada já exportada reproduziu a ordem do Colab nas 2.918 posições. A igualdade de todos os registros sustenta a conclusão de que a diferença de ordenação não tem impacto científico. [Código gerador](../notebooks/01_EDA_COMPLETA.ipynb) · [Ordenação no pandas 2.2.3](https://pandas.pydata.org/pandas-docs/version/2.2.3/reference/api/pandas.DataFrame.sort_values.html)

| Arquivo | SHA-256 |
|---|---|
| CSV histórico no Git | `5e8d91fab192677ffb133051c5c8b1bcf3069e759081352a7ddb2f6a410f1bb9` |
| CSV do Colab, confirmado pelo manifesto da etapa 01 | `53fe4afff9c9ece098a58c7a59f8d89af2dc59dcaaeaa602e9b0fbf598b87334` |

O [comparador atualizado](../scripts/compare_runs.py) confere os cabeçalhos e conta as ocorrências dos registros completos exclusivamente nesse CSV. A igualdade é exata nos campos decodificados, inclusive no campo numérico. Os outros CSVs mantêm comparação posicional com `rtol=atol=1e-7`. Os [testes](../tests/test_compare_runs.py) cobrem linhas reordenadas, duplicatas, alterações de valores e diferenças de estrutura. O ZIP original conserva o resultado reportado na data da execução.

## Verificação da consolidação

- Os 10 testes do comparador passaram. A conferência com o ZIP real retornou 129/129 tabelas históricas equivalentes. Apenas `outlier_coincidence.csv` mudou de classificação e continua com `byte_equal: false`.
- A suíte completa em uma cópia temporária com finais LF teve 32 aprovações e 3 falhas. As duas falhas de integridade registradas no Colab e a falha em `test_protected_files` apontam para os mesmos hashes da introdução. A suíte completa inclui esse terceiro teste de preservação.
- O manifesto de preservação conserva o hash histórico do comparador. O teste de preservação reconhece a alteração autorizada apenas nesse script, cujo comportamento passou a ser verificado pelos testes específicos.
