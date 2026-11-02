# Auditoria da migração

Data: 01/11/2026. Destino exclusivo: `thiagossilva17/TCC_MMM_Google_Meridian`, branch `main`. Estado inicial: commit `d9f4dca12574901608af4907a91ac796f0b22f6b`, contendo apenas README com o título do repositório. O título foi incorporado ao README ampliado; não havia outros arquivos para reconciliar.

## Fontes e inventário anterior às alterações

Foram inspecionados os oito anexos, inclusive as oito páginas rasterizadas do planejamento em PDF, e o repositório histórico em `ef39d0a7629e849d31582cea6cefccb581f7a445`. Esse commit coincide com a origem indicada pelo notebook. Não foi necessário consultar Project2. O arquivo Texto colado é o próprio prompt master; não veio um segundo prompt temporal independente, e as seções 12–19 do master forneceram o escopo.

O [inventário inicial](proveniencia/inventario_inicial.json) foi produzido antes da migração. O [manifesto de migração](proveniencia/manifesto_migracao.json) contém 260 transferências/segmentações com origem, destino, hashes e transformação. Os oito anexos permanecem intocados. O notebook original está adicionalmente preservado como snapshot integral comprimido.

Os 220 arquivos citados no manifesto histórico foram encontrados e conferiram por SHA-256. A base raw foi transferida sem alteração e seu hash também foi confirmado por download independente da URL oficial fixada; o painel processado foi comparado à transformação original. Metadados históricos e licença da base foram preservados. [Metadados da migração](../data/metadata/migration.json).

## Curadoria

Migrados: dados raw/processed, metadados e licença, SVGs, CSVs, relatórios, logs e documentação de apoio usada na navegação e interpretação. Não migrados: notebooks particionados, módulos científicos redundantes, caches, ambientes virtuais, testes históricos duplicados, ZIPs, diretório de auditorias experimentais e modelos futuros. O planejamento em PDF foi consultado, mas não publicado: é contexto de arquitetura, não evidência científica.

Introdução, referencial e bibliografia foram copiados byte a byte. O arquivo 04 foi segmentado nas marcas reais de capítulos e referências auxiliares. Concatenar os dois capítulos e a seção auxiliar reconstrói exatamente os bytes originais. A seção auxiliar fica em `docs/proveniencia/`, fora da monografia principal; nenhuma referência foi removida ou acrescentada à bibliografia.

## Independência e navegação

O notebook usa somente arquivos do projeto ou a origem oficial fixada do Google. Nenhum script clona projetos históricos, nenhum import carrega seus módulos, e não há submódulos nem remotes adicionais. Links de navegação apontam para os arquivos locais e para o notebook consolidado; nomes antigos em logs, snapshot e documentação são referências históricas de proveniência.

A validação integral utilizou uma cópia apenas do novo projeto, com raiz explícita. Os repositórios antigos não foram utilizados em tempo de execução. As funções científicas estão no notebook; os scripts entregues tratam de execução, comparação e exportação editorial, sem replicar a lógica de análise.

## Testes e evidências

- [Preservação do notebook e da ciência](VALIDACAO_PRESERVACAO_EDA.md).
- [Comparação de 129 tabelas](proveniencia/comparacao_reexecucao.json).
- [Manifesto da reexecução 00–07](proveniencia/reexecucao_integral_manifesto.json).
- [Manifesto temporal da execução isolada](proveniencia/reexecucao_temporal_isolada_manifesto.json).
- Testes automatizados em `tests/test_integrity.py`; resultado final em `proveniencia/testes.txt`.
- Sete figuras verificadas visualmente; quatro tabelas numéricas conferidas; quinta tabela identificada como síntese.

## Divergências e limitações registradas

1. API de metadados GitHub informou tamanho zero; inspeção Git revelou commit inicial com README. O commit foi preservado.
2. A primeira tentativa por kernel Jupyter falhou por bloqueio de sockets; execução por IPython foi utilizada e explicitamente identificada.
3. O fingerprint histórico `marshal` acusou alterações inexistentes no checkpoint final. A correção ficou restrita à infraestrutura, com diff e teste de regressão; a segunda execução integral passou.
4. Dependências desta execução diferem de algumas versões históricas. O commit Meridian foi mantido, as versões testadas foram fixadas e 129 tabelas concordaram numericamente. Isso não é identidade binária de todos os gráficos ou HTMLs regenerados.
5. Os capítulos 3/4 citam Google [s. d.]a/b etc.; a bibliografia principal usa Google 2026a–g. Divergência preservada e pendente de revisão acadêmica autorizada.
6. O relatório original `CONSOLIDACAO_VALIDACAO.md` não foi recuperado. A página local distingue o relato de 21/10 das verificações realizadas agora, sem inventar evidências antigas.
7. Colab real, decisões finais de modelagem, estimação GEO/nacional, comparação causal, revisão acadêmica e LaTeX permanecem futuros.

8. Uma conferência de hashes detectou um PNG complementar truncado após a execução. Os bytes foram restaurados do ZIP produzido pela mesma execução, com recuperação do hash esperado; os 11 PNGs editoriais/complementares foram abertos integralmente para validação. Não houve recálculo nem alteração da evidência.

## Publicação

Somente o novo repositório será atualizado, por avanço normal da branch `main`, sem force push. O commit publicado é verificável no histórico GitHub e será informado na entrega. A documentação não presume publicação antes de confirmação remota.


## Validação final em ambiente virtual novo

Instalação dos requisitos em venv sem system-site-packages concluída; execução sequencial 00–08 em cópia isolada concluída. As 129 tabelas históricas e os 15 CSVs complementares concordaram com os artefatos preservados/publicados. O ambiente foi registrado em [ambiente_limpo.json](proveniencia/ambiente_limpo.json). Os nove testes finais passaram; resultado em [testes.txt](proveniencia/testes.txt). Essa verificação não substitui a interface real do Colab.
