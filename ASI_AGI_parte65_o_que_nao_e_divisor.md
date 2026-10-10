# Como eu construiria uma AGI/ASI — Parte 65 (0x41): o que não é divisor

> Continuação da [Parte 64](ASI_AGI_parte64_o_fator_do_final.md). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 64 achou as seis bases de 17 a 22 abaixo da conta dos primos palíndromos. Esta parte pergunta se os primos pequenos que
> não dividem 2b explicam o viés, se a definição de um substantivo fica mais longa quanto mais fundo ele está na taxonomia, e quanto vale o período de 1/p em hexadecimal.

## As perguntas desta parte

1. **P1391 (0x56F).** Os primos pequenos q ∤ 2b dividem os palíndromos com a frequência 1/q? A correção explica o viés das bases grandes? (Rodada 39) ↩ P1361
2. **P1392 (0x570).** A definição de um substantivo é mais longa quanto mais fundo ele está na taxonomia? ↩ P1362
3. **P1393 (0x571).** Hexadecimal: o período de 1/p em base 16, relativo ao maior possível (p − 1). ↩ P1363
4. **P1394 (0x572).** Preditiva comigo mesma. **P1395 (0x573).** Engenharia reversa e Jung. **P1396 (0x574).** O diálogo.
5. **P1419 (0x58B).** Placar. **P1420 (0x58C).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1391, p1392, p1393).

| medida | estatístico (até a 64) | ingênuo (Parte 64) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [8.500; 21.356] | 14.704 | **[8.500; 21.356]** | o estatístico |
| compressão | [0,404; 0,429] | 0,417 | **[0,404; 0,429]** | o estatístico |
| testes de unidade | [1,61; 7,89] | 4 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [4,72; 10,53] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,33; 4,17] | 2 | **[0,33; 4,17]** | o estatístico |
| redundância P821 | [0,537; 0,638] | 0,643 | **[0,537; 0,638]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1392, a profundidade e o tamanho da definição.** Nos substantivos com profundidade na taxonomia (P793), o Spearman entre a profundidade e o número de palavras da
definição (sem os exemplos).
- **Restrições, com peso:** (1) um conceito mais específico precisa de mais diferenças para ser separado dos irmãos (gênero + mais diferenças): puxa para cima; (2) os
  sinsets fundos são sobretudo espécies e gêneros, definidos por uma fórmula curta ("a genus of…", "any of various…"): puxa para baixo. **Peso medido num caso
  escolhido por regra escrita antes (a outra classe com hierarquia, os verbos), por código antes deste registro:** Spearman **0,020** (13.708 verbos).
- Exemplo à mão: *entity* (profundidade 0), 18 palavras; *dog* (profundidade ~13), "a member of the genus Canis…", ~20 palavras: quase igual.
- (a) Spearman nos substantivos em **[−0,10; 0,15]**

**P1393, o período de 1/p em base 16.** Para os primos p de 10⁴ a 10⁵, a média de ord_p(16)/(p − 1) (ord_p(16) é o período de 1/p em hexadecimal).
- **Restrições, com peso:** (1) 16 = 2⁴ é um quadrado, então nunca é raiz primitiva: ord_p(16) = ord_p(2)/mdc(ord_p(2), 4) ≤ (p − 1)/2; (2) a média de ord_p(2)/(p − 1)
  é uma constante conhecida (~0,58, da conjectura de Artin e dos trabalhos de Stephens). **Peso medido num caso escolhido por regra escrita antes (todos os primos
  abaixo de 10⁴), por código antes deste registro:** média de ord_p(16)/(p − 1) = **0,279**; de ord_p(2)/(p − 1) = 0,585; razão 0,477 = E[1/mdc(ord₂, 4)].
- Exemplo à mão: p = 17: ord₁₇(2) = 8, ord₁₇(16) = 8/4 = 2; 1/17 = 0x0,0F0F…, período 2.
- (b) média de ord_p(16)/(p − 1) nos primos de 10⁴ a 10⁵ em **[0,26; 0,30]**

**P1391, rodada 39:** no `dialogo/DIALOGO.md` (previsões (c) a (g)).
