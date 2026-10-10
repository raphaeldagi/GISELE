# Como eu construiria uma AGI/ASI — Parte 59 (0x3B): o nome e a coisa

> Continuação da [Parte 58](ASI_AGI_parte58_a_primeira_diferenca.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o resto deste
> documento.** A Parte 58 achou o bloco de palavras com maiúscula no começo da ordem dos códigos e um erro meu: uma quantidade escrita à mão no script de
> autoavaliação (a regra nova está no `CLAUDE.md`). Esta parte pergunta quantos nomes próprios do português também são palavras comuns, quantas palavras do
> inglês nunca servem para definir outra, e quanto dura a persistência multiplicativa em base 16.

## As perguntas desta parte

1. **P1211 (0x4BB).** Quantos lemas portugueses com maiúscula têm uma irmã minúscula com a mesma grafia? (Rodada 33) ↩ P1181
2. **P1212 (0x4BC).** Quantas palavras do WordNet nunca aparecem na definição de outra? ↩ P882
3. **P1213 (0x4BD).** Hexadecimal: a persistência multiplicativa em base 16 (multiplicar os dígitos até sobrar um).
4. **P1214 (0x4BE).** Preditiva comigo mesma. **P1215 (0x4BF).** Engenharia reversa e Jung. **P1216 (0x4C0).** O diálogo.
5. **P1239 (0x4D7).** Placar. **P1240 (0x4D8).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

| medida | estatístico (até a 58) | ingênuo (Parte 58) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.168; 13.707] | 11.541 | **[9.500; 13.707]** | mecanismo conferido |
| compressão | [0,402; 0,460] | 0,416 | **[0,402; 0,445]** | mecanismo conferido |
| testes de unidade | [2,59; 4,91] | 4 | **[3; 4]** | 3 a 4 funções novas (p1211, p1212, p1213, talvez um auxiliar), um teste PELO NOME cada |
| testes do placar | [4,88; 8,37] | 7 | **[4,88; 8,37]** | o estatístico |
| erros do placar | [0,24; 3,76] | 1 | **[0,24; 3,76]** | o estatístico |
| redundância P821 | [0,503; 0,597] | 0,549 | **[0,503; 0,597]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 1 (Parte 58) | **0** | `p1092`, chamado pelo script (regra nova) |

### Sobre o mundo

**P1212, as palavras que não definem.** No grafo de definições do WordNet (palavra → palavras das suas definições), quantas das 77.503 palavras nunca aparecem
na definição de outra (grau de entrada zero)?
- **Restrições:** as definições usam um vocabulário de base (as palavras gerais: *act*, *person*, *state*); os nomes de espécies, gêneros e lugares quase nunca
  definem nada; e as palavras curtas e comuns definem muito.
- Exemplo à mão: *aardvark* não deve aparecer em definição nenhuma; *animal* aparece em milhares.
- (a) fração das palavras que nunca definem em **[55%; 85%]**

**P1213, a persistência multiplicativa em base 16** (n de 16 a 16⁵ − 1: o número de passos "multiplicar os dígitos hexadecimais" até sobrar um dígito).
- **Restrições:** um dígito 0 zera o produto; e um produto com 4 ou mais fatores 2 termina em 0 em hexadecimal (16 = 2⁴), então o passo seguinte dá 0. Com
  dígitos ao acaso, quase todo produto de vários dígitos tem 4 fatores 2: a persistência fica curta.
- Exemplo à mão: 0x3F → 3 × 15 = 45 = 0x2D → 2 × 13 = 26 = 0x1A → 1 × 10 = 10 = 0xA: 3 passos.
- (b) a maior persistência em **[3; 6]**
- (c) a média em **[1,1; 2,0]** (a maioria cai em 0 em um ou dois passos)

**P1211, rodada 33:** no `dialogo/DIALOGO.md`.
