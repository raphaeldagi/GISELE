# Como eu construiria uma AGI/ASI — Parte 55 (0x37): o ulp que chega

> Continuação da [Parte 54](ASI_AGI_parte54_a_sorte_das_rodadas.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o resto
> deste documento.** A Parte 54 achou que as diferenças da libm somem quando caem fora do caminho da saída (uma escolha as absorve) e se propagam numa
> iteração. Esta parte **injeta** um ulp em cada exp e log das rodadas antigas e mede quanto ele chega à saída; mede a fragilidade do mapa da definição a
> uma palavra; conta os dígitos hexadecimais que um ulp muda; e audita as funções novas sem teste.

## As perguntas desta parte

1. **P1091 (0x443).** Um ulp em cada exp e log: quanto chega à saída de cada rodada? (Rodada 29) ↩ P1061
2. **P1092 (0x444).** Quantas funções pNN novas (desde a P821) não têm teste? (a checagem pedida pela Parte 54)
3. **P1093 (0x445).** Tirando o funil *act* do mapa da definição, quantas palavras mudam de destino? ↩ P882
4. **P1094 (0x446).** Hexadecimal: quantos dígitos hexadecimais um ulp muda, em média?
5. **P1095 (0x447).** Preditiva comigo mesma. **P1096 (0x448).** Engenharia reversa e Jung. **P1097 (0x449).** O diálogo.
6. **P1119 (0x45F).** Placar. **P1120 (0x460).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

Estatístico (últimas 8 partes, até a 54) e os dois mecanismos conferidos (a seção sobre mim aumenta o tamanho; a tabela de autoavaliação baixa a compressão):

| medida | estatístico | ingênuo (Parte 54) | **eu** |
|---|---|---|---|
| caracteres | [7.483; 13.066] | 11.211 | **[9.500; 13.500]** |
| compressão | [0,412; 0,470] | 0,424 | **[0,405; 0,445]** |
| testes de unidade | [2,52; 4,23] | 3 | **[2,52; 4,23]** |
| testes do placar | [4,90; 12,85] | 8 | **[4,90; 12,85]** |
| erros do placar | [0,06; 4,69] | 2 | **[0,06; 4,69]** |
| redundância P821 | [0,511; 0,603] | 0,586 | **[0,511; 0,603]** |
| previsões unilaterais | — | 0 | **0** |

**P1092, a auditoria do meu código.** Das **35** funções pNN escritas desde a P821, quantas não aparecem em nenhum arquivo `synthai/testes_parte*.py`?
- Exemplo à mão: a `p821_inversao` não tem teste (lembrança, a conferir pela função).
- (a) **8 a 18** sem teste

### Sobre o mundo

**P1093, a fragilidade do mapa.** No mapa da P882, as palavras cujo primeiro substantivo da definição é *act* passam a ir para o **segundo** substantivo da
definição (ou viram sumidouro). Quantas palavras mudam de destino final (o ciclo ou o sumidouro onde a órbita termina)?
- (b) fração em **[10%; 60%]** (70% caíam na bacia do ciclo de *act*; muitas chegam lá sem passar por *act* diretamente)

**P1094, o ulp em hexadecimal.** Para doubles sorteados em [1, 2) (semente 1094), quantos dos 13 dígitos hexadecimais da mantissa mudam ao somar um ulp?
- A conta: o último dígito muda sempre; o vai-um passa ao dígito anterior se o último era F (chance 1/16), e assim por diante: E = Σ_{k≥0} 16⁻ᵏ = 16/15 = **1,0667**.
- (c) média medida em 100.000 sorteios em **[1,05; 1,09]**
