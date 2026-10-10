# Como eu construiria uma AGI/ASI — Parte 62 (0x3E): o último dígito

> Continuação da [Parte 61](ASI_AGI_parte61_o_dobro.md). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de escrever
> o resto deste documento.** A Parte 61 achou que o excesso dos narcisistas sobre a conta mora numa base, a 8. Esta parte pergunta se o teste do último dígito
> explica isso, quantas palavras portuguesas da OpenWordNet-PT se escrevem igual à inglesa do mesmo sinset, e quantos números em base 16 não são n + (soma dos
> dígitos de n) para nenhum n (os autonúmeros de Kaprekar).

## As perguntas desta parte

1. **P1301 (0x515).** O teste do último dígito explica, base por base, o excesso dos narcisistas sobre a conta? (Rodada 36) ↩ P1274
2. **P1302 (0x516).** Quantos sinsets têm uma palavra portuguesa escrita exatamente como a inglesa? ↩ P1211
3. **P1303 (0x517).** Hexadecimal: a densidade dos autonúmeros em base 16. ↩ P1273
4. **P1304 (0x518).** Preditiva comigo mesma, condicional às surpresas. **P1305 (0x519).** Engenharia reversa e Jung. **P1306 (0x51A).** O diálogo.
5. **P1329 (0x531).** Placar. **P1330 (0x532).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (regra da Parte 61)

**Surpresa** = uma previsão do mundo que erra por mais do que a largura da própria faixa (um erro que pede mecanismo novo). Planejadas: 7 previsões do mundo
((a) a (g)) e 3 funções (p1301, p1302, p1303), um teste de unidade cada.

| medida | estatístico (até a 61) | ingênuo (Parte 61) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [6.836; 20.270] | 16.934 | **[6.836; 20.270]** | o estatístico |
| compressão | [0,408; 0,434] | 0,424 | **[0,408; 0,434]** | o estatístico |
| testes de unidade | [0,98; 7,77] | 5 | **[2 + S; 5 + S]** | 3 planejados, ~1 a mais por surpresa |
| testes do placar | [4,02; 10,23] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,67; 4,58] | 3 | **[0,67; 4,58]** | o estatístico |
| redundância P821 | [0,505; 0,621] | 0,595 | **[0,505; 0,621]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1302, as palavras iguais nas duas línguas.** Dos sinsets com lema em português na OpenWordNet-PT, quantos têm um lema português (de uma palavra só,
em minúsculas) idêntico a um lema inglês do mesmo sinset?
- **Restrições, com peso:** (1) muito do vocabulário erudito do inglês é latino, mas a grafia quase sempre muda (*nation*/*nação*, *activity*/*atividade*);
  igualdade exata exige palavras curtas e sem sufixo (*animal*, *hotel*, *radar*); (2) os nomes próprios (*Paris*, *Darwin*) se escrevem igual e são uma
  fração visível dos sinsets de instância; (3) os termos técnicos e os nomes de gêneros biológicos (*Canis*, *Rosa*) são latim nas duas línguas.
- Exemplo à mão: *animal* (n) = *animal*: conta. *dog*/*cão*: não.
- (a) fração dos sinsets com lema português que têm uma palavra igual em **[6%; 18%]**
- (b) por classe: a fração nos substantivos é maior que nos verbos por um fator em **[3; 15]** (os verbos portugueses terminam em -ar, -er, -ir; quase nunca
  coincidem)

**P1303, os autonúmeros em base 16** (m que não é n + s₁₆(n) para nenhum n; m de 1 a 16⁵).
- **Restrições, com peso:** (1) numa base ímpar, s(n) ≡ n (mod 2), então n + s(n) é sempre par e todo ímpar é autonúmero: densidade ½ (confirmado na fonte);
  numa base par, não há essa restrição, e a densidade é bem menor; (2) dentro de uma dezena (sem vai-um), n + s(n) anda de 2 em 2, e os buracos são cobertos
  pelas imagens de outras dezenas: a densidade vem dos vai-uns; (3) calibração (outro mundo, medida por código antes deste registro): base 10, até 10⁶,
  densidade **0,0978**.
- Exemplo à mão: em base 16, os ímpares abaixo de 16 (1, 3, …, 15) são autonúmeros (n + s(n) = 2n para n < 16); 0x10 = 16 = 8 + 8: não é.
- (c) densidade dos autonúmeros de 1 a 16⁵ em **[0,06; 0,13]** (centro na base 10; a base maior tem vai-uns mais raros, o que pode mover para qualquer lado)

**P1301, rodada 36:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).
