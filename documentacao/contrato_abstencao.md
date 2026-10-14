# Contrato de decisão e abstenção

## Interface sequencial

`decidir(situacao)` devolve uma `Opcao` ou `None`. Uma opção devolvida segue para execução e, depois, `observar(resultado)`. `None` encerra o episódio ou a rodada: não autoriza substituir a decisão pela primeira opção rejeitada e não produz resultado fictício para aprendizagem. Lista de opções vazia também devolve `None`.

Os agentes continuam sequenciais. Esta alteração não oferece associação de resultados concorrentes nem confirmação de execução externa. `None` tampouco codifica a causa exata da abstenção; veto, risco e falta de orçamento conservam tratamentos existentes.

## Custos e estado

Consultas e leituras realizadas antes da abstenção são descontadas. Ganhos e perdas anteriores permanecem no retorno. Vetos já recebidos permanecem disponíveis para registro. A abstenção limpa a decisão pendente; na autorregulação, o prefixo do episódio abandonado não entra na estimação de retorno futuro de episódios completos. Dados efetivamente observados nas ações anteriores continuam válidos para a regressão.

Na composição, `observar` é repassado uma vez depois de uma escolha aceita; após abstenção é ignorado. O último delegado permanece disponível para leitura de vetos e relação.

## Métricas

| Campo | Definição |
|---|---|
| retorno | Ganhos/perdas, menos consultas e leituras, por episódio ou rodada solicitado. |
| abstencoes | Fração dos episódios ou rodadas encerrados por `None`. |
| acoes | Número médio de ações executadas por episódio ou rodada solicitado. |
| cobertura | Ações executadas divididas por todas as ações originalmente previstas. |
| concluidos | Fração de episódios sequenciais terminados sem catástrofe nem abstenção; no bandido, fração das rodadas com todas as puxadas executadas. |

Cobertura não implica sucesso: uma tarefa de um passo com ação catastrófica tem cobertura 1 e conclusão 0. No bandido, catástrofes continuam sem encerrar a rodada, portanto podem coexistir com conclusão 1. O campo `catastrofes` permanece separado.

O diagnóstico do bandido mantém seu teto no horizonte original, mesmo com abstenção. Sem braços seguros, teto e referência diagnóstica da rodada valem zero. Essas convenções não garantem que o retorno ou sua normalização constituam uma medida geral de inteligência.

## Compatibilidade

O resumo acrescenta quatro chaves. Consumidores que exigem um conjunto exato precisam incluí-las. Os quatro wrappers históricos que desreferenciavam a escolha foram adaptados. Comparações entre opção descartada e substituta são calculadas apenas quando existe escolha aceita; sem observações, as respectivas estimativas ficam `NaN`. Isso muda o condicionamento da amostra e não autoriza reutilizar conclusões numéricas antigas.

## Validação

67 testes selecionados passaram, incluindo 16 testes novos. Após acrescentar o caso sequencial catastrófico de um passo ao teste existente, os 16 testes de regressão passaram novamente. A demonstração `python -m synthai` concluiu as três tarefas e exibiu as novas métricas. Na semente padrão, não houve abstenções nessa demonstração; os testes controlados cobrem os caminhos de rejeição.

Os avisos preexistentes de arquivos não fechados nos testes continuam presentes. A suíte completa e todos os experimentos históricos não foram executados.

## Arquivos

- Implementação: fontes/synthai/{agente,mundos,autorregulacao,composta,__main__}.py e fontes/calculos.py.
- Testes: fontes/synthai/testes_abstencao_revisao.py e ajuste de interface em fontes/synthai/testes.py.
- Logs: validacao_abstencao.log, regressoes_abstencao.log e demonstracao_abstencao.txt.
- Patch: abstencao.patch, contra a cópia antes desta etapa. A correção estatística da etapa anterior já pertence a essa base.
- Manifesto: manifesto_abstencao.json, com hashes dos arquivos alterados.

O avaliador com selo incompleto continua pendente de correção.

Atualização da etapa seguinte: o selo passou a detectar alterações no catálogo de dependências, conforme contrato_avaliador.md. A indicação anterior de pendência registra o estado ao concluir a etapa de abstenção.
