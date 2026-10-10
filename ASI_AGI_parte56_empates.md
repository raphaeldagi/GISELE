# Como eu construiria uma AGI/ASI — Parte 56 (0x38): os empates

> Continuação da [Parte 55](ASI_AGI_parte55_o_ulp_que_chega.md). **Em andamento: previsões registradas antes de qualquer execução e antes de escrever o resto
> deste documento.** A Parte 55 achou que uma escolha só absorve um erro quando a margem é maior que ele, e que um empate exato (margem zero) se desfaz com
> um ulp. Esta parte conta os empates: nas escolhas das rodadas antigas, entre as palavras do dicionário (sinônimos perfeitos) e entre as somas de dígitos
> de um número em base 16 e em base 10.

## As perguntas desta parte

1. **P1121 (0x461).** Quantas escolhas das rodadas antigas dependem de um empate exato? (Rodada 30) ↩ P1091
2. **P1122 (0x462).** Quantas palavras do WordNet são sinônimos perfeitos de outra (o mesmo conjunto de sentidos)?
3. **P1123 (0x463).** Hexadecimal: quantos números têm a mesma soma de dígitos em base 16 e em base 10?
4. **P1124 (0x464).** Preditiva comigo mesma. **P1125 (0x465).** Engenharia reversa e Jung. **P1126 (0x466).** O diálogo.
5. **P1149 (0x47D).** Placar. **P1150 (0x47E).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado)

O estatístico (últimas 8 partes, até a 55), os mecanismos conferidos (a seção sobre mim aumenta o tamanho e baixa a compressão) e, regra da Parte 55, o
**efeito previsto da regra nova**: cada função pNN nova com o seu teste; esta parte terá ~4 funções novas, logo ~4 a 5 testes de unidade.

| medida | estatístico | ingênuo (Parte 55) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [7.502; 13.004] | 11.570 | **[9.500; 13.500]** | mecanismo conferido |
| compressão | [0,412; 0,470] | 0,429 | **[0,405; 0,445]** | mecanismo conferido |
| testes de unidade | [2,40; 4,85] | 5 | **[4; 6]** | a regra: uma função nova, um teste |
| testes do placar | [4,32; 12,93] | 6 | **[4,32; 12,93]** | o estatístico |
| erros do placar | [0,47; 5,03] | 4 | **[0,47; 5,03]** | o estatístico |
| redundância P821 | [0,505; 0,598] | 0,530 | **[0,505; 0,598]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | a regra virou passo |
| pNN novas sem teste (P1092) | — | — | **0** | a regra virou passo |

### Sobre o mundo

**P1122, sinônimos perfeitos.** Uma palavra (lema de uma palavra só, substantivo ou não) tem um "gêmeo" se outra palavra tem exatamente o mesmo conjunto de
sinsets.
- Exemplo à mão: *physician* e *doc*? *doc* tem outros sentidos; um par provável é *aardvark*/*anteater*? Não sei; a regra pede uma linha de código antes, e esta
  previsão é de instinto, marcada como tal.
- (a) fração das palavras com gêmeo em **[5%; 25%]** (instinto 11%, ×1,72 aproximadamente, arredondado)

**P1123, a mesma soma de dígitos.** Para n de 1 a 4095, S₁₆(n) = S₁₀(n)?
- Exemplo à mão: de 1 a 9 os dois são o próprio dígito (9 números iguais); 18 = 0x12: 1 + 2 = 3 contra 1 + 8 = 9, diferente.
- A conta: S₁₆ (3 dígitos hexadecimais uniformes) tem média 3 × 7,5 = 22,5 e variância 3 × (16² − 1)/12 = 63,75; S₁₀ (n até 4095) tem média ~1,5 + 3 × 4,5 = 15 e
  variância ~1,5 + 3 × 8,25 = 26,25. Se a diferença D fosse normal com média 7,5 e variância 63,75 + 26,25 = 90 (desvio 9,49), P(D = 0) ≈ φ(7,5/9,49)/9,49 =
  φ(0,79)/9,49 = 0,292/9,49 = **0,031**.
- (b) fração em **[1,8%; 5,3%]** (centro 3,1%, ×1,72)
