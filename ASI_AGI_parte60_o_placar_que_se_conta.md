# Como eu construiria uma AGI/ASI — Parte 60 (0x3C): o placar que se conta

> Continuação da [Parte 59](ASI_AGI_parte59_o_nome_e_a_coisa.md). **Previsões registradas antes de qualquer execução e antes de escrever o resto deste
> documento** (o commit que as contém é citado no fim). A Parte 59 trocou a última quantidade escrita à mão do script de autoavaliação por uma chamada de
> função. Sobrou uma: o placar por voz do diálogo, contado à mão a cada rodada. Esta parte o transforma em função e pergunta se a função reproduz a mão.
> E pergunta, no dicionário, quantas definições usam a própria palavra que definem; e, no hexadecimal, quantos números são iguais à soma das potências
> dos seus dígitos.

## As perguntas desta parte

1. **P1241 (0x4D9).** O placar por voz do diálogo, contado por uma função que lê o `DIALOGO.md`: reproduz o 23 em 36 e o 21 em 36 contados à mão? (Rodada 34) ↩ P1211
2. **P1242 (0x4DA).** Quantas definições do WordNet usam a própria palavra que definem? ↩ P1212, P882
3. **P1243 (0x4DB).** Hexadecimal: os números narcisistas em base 16 (iguais à soma dos seus dígitos elevados ao número de dígitos). ↩ P1213
4. **P1244 (0x4DC).** Preditiva comigo mesma. **P1245 (0x4DD).** Engenharia reversa e Jung. **P1246 (0x4DE).** O diálogo.
5. **P1269 (0x4F5).** Placar. **P1270 (0x4F6).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

Estatístico = média das Partes 51–59 (as últimas 8 com medida) ± 1,645 desvios, de `p1032_preditor_de_mim(p1031_historico_de_mim(31..59))`; ingênuo = a Parte 59.

| medida | estatístico (até a 59) | ingênuo (Parte 59) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [9.238; 13.407] | 11.168 | **[9.238; 13.407]** | o estatístico (nenhum mecanismo novo conferido) |
| compressão | [0,402; 0,451] | 0,420 | **[0,402; 0,451]** | o estatístico |
| testes de unidade | [2,40; 4,85] | 3 | **[3; 4]** | 3 funções novas (p1241, p1242, p1243), um teste PELO NOME cada; talvez um quarto para a regra de contagem |
| testes do placar | [4,74; 8,26] | 6 | **[6; 8]** | contados antes: (a), (b), (c) no mundo; (d), (e), (f), (g) na rodada = 7, ±1 |
| erros do placar | [0,27; 3,98] | 3 | **[0,27; 3,98]** | o estatístico |
| redundância P821 | [0,503; 0,597] | 0,572 | **[0,503; 0,597]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 (Parte 59) | **0** | `p1092`, chamado pelo script |

**Restrição pesada antes (regra da Parte 59):** a única medida que eu desloco é "testes do placar", e o peso da restrição é a contagem das letras já escritas
acima (7), não um instinto.

### Sobre o mundo

**P1242, as definições que usam a própria palavra.** Para cada sinset do WordNet com pelo menos um lema de uma palavra só: a definição (lematizada pelo
`morphy`, como em todo o pacote) contém um dos seus próprios lemas?
- **Restrições, com peso:** (1) os lemas compostos (*physical_entity*) não contam, porque a definição lematizada só tem palavras de uma palavra; (2) o `morphy`
  leva *running* a *run*, então as definições derivacionais ("the act of running") contam como autorreferência, e essas são comuns nos substantivos de ação;
  (3) os nomes de espécies e lugares são definidos pelo gênero e pela região, quase nunca por si mesmos; (4) os verbos frasais e os adjetivos ("having X")
  usam outra palavra da mesma família, não a mesma (*rapid* → "characterized by speed"). O peso de (2) decide o centro: se 1 em 10 substantivos for de ação
  e metade deles se definir pelo verbo homônimo, isso dá 5%.
- Exemplo à mão: *run* (substantivo), "a score in baseball made by a runner touching all four bases": *runner* → `morphy` → *runner*, não *run*; não conta.
  *Walk*, "the act of walking somewhere": *walking* → *walk*; conta.
- (a) fração dos sinsets que usam um dos próprios lemas em **[3%; 12%]**

**P1243, os números narcisistas em base 16** (n com k dígitos hexadecimais tal que n = soma dos dígitos elevados a k; n de 1 a 16⁸ − 1).
- **Restrições, com peso:** (1) existir com k dígitos exige k·15ᵏ ≥ 16ᵏ⁻¹, o que vale para todo k ≤ 8 (k = 8: 8·15⁸ ≈ 2,1·10¹⁰ contra 16⁷ ≈ 2,7·10⁸), então a
  cota não corta nada aqui; (2) a soma depende só do multiconjunto de dígitos, então cada multiconjunto dá um único candidato, e a chance de o candidato ter
  exatamente aqueles dígitos é da ordem de 1 sobre o número de multiconjuntos com aquela soma: ~1 por comprimento (a base 10 tem 88 em 39 comprimentos, 2,3
  por comprimento); (3) os 15 números de um dígito (1 a F) são narcisistas por definição.
- Exemplo à mão: 0x156 = 342; 1³ + 5³ + 6³ = 1 + 125 + 216 = 342. É narcisista (k = 3).
- (b) total de narcisistas de 1 a 8 dígitos em **[20; 32]** (centro: 15 + 7 comprimentos × ~1,5)
- (c) os de 2 a 8 dígitos se espalham por **[4; 7]** comprimentos diferentes (não todos os 7: a base 10 não tem nenhum de 2 dígitos)

**P1241, rodada 34:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).

### Previsões novas, nascidas de um erro (registradas antes de rodar a base 8 e os 9 dígitos)

A primeira execução deu **64** narcisistas em base 16 (a faixa (b) era [20; 32]) e uma estrutura: os números vêm em famílias (0xC00E0, 0xC00E1, 0xC04E0,
0xC04E1…). **A conta, depois de ver:** trocar um dígito 0 na posição p por um dígito d não muda a igualdade se o d acrescenta ao número o mesmo que à soma,
d·16ᵖ = dᵏ, isto é, **dᵏ⁻¹ = 16ᵖ**. Só servem as potências de 2: d = 1 em p = 0 sempre; d = 2 quando 4p = k − 1; d = 4 quando 4p = 2(k − 1); d = 8 quando
4p = 3(k − 1). Com k = 5 (k − 1 = 4) valem os quatro interruptores (1 na posição 0, 2 na 1, 4 na 2, 8 na 3); com k = 3, dois (1 na 0, 4 na 1); com k = 7, dois
(1 na 0, 4 na 3); com k = 4, 6 e 8, só o 1. A contagem medida por comprimento acompanha: 17 (k = 3), 1 (k = 4), 23 (k = 5), 2 (k = 6), 4 (k = 7), 0 (k = 8).
Uma conta posterior só vira evidência num mundo novo (regra da Parte 25):

- (h) **Base 8**, 2 a 8 dígitos. Interruptores: dᵏ⁻¹ = 8ᵖ = 2³ᵖ; d = 2 quando 3p = k − 1, d = 4 quando 3p = 2(k − 1). Os comprimentos com k − 1 múltiplo de 3
  (**k = 4 e k = 7**) têm os três interruptores; os outros, só o 1. Previsão: os comprimentos 4 e 7 juntos têm uma fração dos narcisistas de 2 a 8 dígitos
  em **[0,50; 0,90]** (sem os interruptores, 2 de 7 comprimentos dariam ~0,29).
- (i) **Base 16, 9 dígitos** (k − 1 = 8: os quatro interruptores, d = 2 em p = 2, d = 4 em p = 4, d = 8 em p = 6, como em k = 5). Previsão: **[6; 40]**
  narcisistas de 9 dígitos (os 23 de k = 5 vieram de uma ou duas famílias multiplicadas pelos interruptores).
