# Como eu construiria uma AGI/ASI — Parte 82 (0x52): o pacote revisado

> Continuação da [Parte 81](ASI_AGI_parte81_o_que_nao_serve.md). **Próxima:** [Parte 83 — a probabilidade da probabilidade](ASI_AGI_parte83_a_probabilidade_da_probabilidade.md). Pedido do usuário, com o arquivo `SYNTHAI_consolidado.py` anexado: **"Adicione, no que couber, ao nosso código. E me envie o
> código final consolidado."** Uma parte de integração, não de experimento: nenhuma previsão foi registrada antes de rodar os testes que vieram no pacote, e isso fica dito aqui.

## O que o arquivo é (lido sem executar)

Um zip em base85 dentro de uma string, com um SHA-256 de conferência (conferido: igual). Aberto pela árvore sintática e por código meu, sem rodar o extrator dele. Dentro: **288 arquivos**. Deles, **228**
são idênticos aos nossos (o pacote é o nosso projeto até a Parte 68), **37** diferem e **23** são novos. Dos 37 que diferem, quase todos são versões nossas mais antigas (as rodadas corrigidas nas
Partes 73 a 77, o `calculos.py` que cresceu). O que ele **mudou** em código nosso: 7 módulos do pacote (`agente`, `composta`, `autorregulacao`, `metacognicao`, `mundos`, `rsi`, `__main__`) e 8
funções do `calculos.py` (`p287`, `p313`, `p314`, `p316`, `p317`, `p318b`, `p322`, `p324`).

## Os defeitos que a revisão do pacote achou no nosso código (reproduzidos com entradas controladas)

1. **`agente.decidir`** devolvia a primeira opção quando nenhuma passava no veto: escolhia uma opção rejeitada. Corrigido: devolve `None` (abstenção), e os mundos encerram a tentativa sem ação.
2. **`metacognicao.comparacao_pareada`** devolvia t = +∞ com desvio zero: um caso degenerado parecia aprovação. Corrigido: t = NaN, com validação de comprimento e de valores finitos.
3. **O selo do `rsi.AvaliadorSelado`** cobria só o texto de uma função: trocar uma dependência na memória mudou a nota sem invalidar o selo. Corrigido: o selo cobre o catálogo de dependências e é
   conferido antes e depois do cálculo.
4. **Os mundos** compartilhavam um gerador aleatório: duas políticas com consumos diferentes não viam os mesmos eventos (a comparação deixava de ser pareada). Corrigido: `aleatoriedade.FontesAleatorias`,
   uma fonte por canal e coordenada, derivada por SHA-256.

## O que entrou, e onde

- **`synthai/revisado/`**: o pacote corrigido inteiro, como subpacote (as correções só valem juntas: a âncora e a exploradora herdam do agente corrigido). **As versões originais ficam intactas**
  (as regras do projeto: os módulos medidos não se editam; versões novas entram em arquivos novos), e por isso todos os números históricos continuam se reproduzindo. Para usar as corrigidas:
  `from synthai.revisado import Synthai`, e a demonstração `python3 -m synthai.revisado`.
- **Os testes de revisão do pacote** (4 arquivos), com os caminhos ajustados para o subpacote: **59 de 59** passam. Um teste foi retirado, com o motivo escrito no arquivo: ele exercita as versões
  reescritas das funções `pNN` do `calculos.py`, que não entraram.
- **`laboratorio/`** (evidência sequencial por supermartingal de teste; feedback persistente em SQLite com "no máximo uma atualização por decisão"): **27 de 27** testes passam.
- **`documentacao/`**: a revisão técnica e os três contratos (abstenção, aleatoriedade, avaliador), e em `documentacao/pacote_recebido/` o README, o log e o relatório de validação do pacote.

## O que não coube, e por quê

- **As 8 funções `pNN` reescritas:** são experimentos históricos, cujos números estão citados nos documentos; reescrevê-las mudaria resultados publicados.
- **`synthai_cli.py`, `verificar.py` e `gerar_distribuicao.py` do pacote:** foram feitos para o layout dele (`fontes/`). O nosso `SYNTHAI_completo.py` (gerado por `gerar_arquivo_unico.py`) faz o mesmo
  papel e agora inclui o subpacote, o laboratório e a documentação.
- **O `testes.py` deles:** é a nossa suíte medida pela P286, com uma linha a mais (as chaves novas do resumo), que vale para os mundos revisados e não para os originais.

## O arquivo único

`SYNTHAI_completo.py` (Partes 1 a 82), testado numa pasta vazia: **353** testes do pacote e **27** do laboratório, todos passando (`python3 SYNTHAI_completo.py --testes`).
