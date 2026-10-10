# Como eu construiria uma AGI/ASI — Parte 71 (0x47): os autovalores da atenção

> Continuação da [Parte 70](ASI_AGI_parte70_algebra_e_geometria.md). O loop segue sozinho (pedido do usuário: "não pare mais"), com álgebra e geometria e a forma de GPT crescendo.

## Previsões sobre as minhas previsões desta parte (registradas ANTES de planejar as calibrações, pela regra da Parte 70)

Neste momento eu ainda não pensei faixa nenhuma desta parte; sei só os temas (os autovalores da atenção do GPT, a rodada 45; uma pergunta do dicionário; uma do hexadecimal). O histórico
pela régua `p1481` (Partes 53 a 70): **127** previsões, **74,8%** de acerto; por tipo, as que cruzam o zero acertam 55,6%, as frações 76,7%, as contagens 66,7%, as outras 77,1%, as
categóricas 81,2%; as medianas de w por tipo vão de 0,29 a 0,47.
- **(m1)** o número de previsões do mundo em **[6; 10]**.
- **(m2)** o número de faixas que cruzam o zero em **[0; 2]**.
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,10; 0,50]**.
- **(m4)** a fração de acertos do mundo em **[0,55; 1,00]**.
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 2]**.
- **(m6)** o número de surpresas em **[0; 2]**.

## As perguntas desta parte

1. **P1571–P1572 (0x623–0x624).** Quantas direções a atenção do GPT usa? Os valores singulares de W_Q W_Kᵀ por Jacobi, e a razão de participação (Rodada 45). ↩ P1543
2. **P1573 (0x625).** A geometria do crescimento: quantos sinsets de substantivo há em cada profundidade? A taxonomia cresce como um espaço hiperbólico? ↩ P1544
3. **P1574 (0x626).** Hexadecimal como polinômios sobre GF(2): os irredutíveis de grau 15 e os "gêmeos" (f, f ⊕ x ⊕ x²). ↩ P1545
4. **P1575 (0x627).** Preditiva comigo mesma. **P1576 (0x628).** Engenharia reversa e Jung. **P1577 (0x629).** O diálogo.
5. **P1599 (0x63F).** Placar (três). **P1600 (0x640).** Unificação.

## Previsões pré-registradas (escritas depois do registro das (m))

### Sobre mim (placar separado), condicionais ao número S de surpresas

Planejadas: as 6 previsões do mundo abaixo, (a) a (f), e 5 funções novas (p1571 a p1574 e a rodada 45, p1578).

| medida | estatístico (até a 70) | ingênuo (Parte 70) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [13.588; 20.030] | 19.769 | **[13.588; 20.030]** | o estatístico |
| compressão | [0,398; 0,421] | 0,408 | **[0,398; 0,421]** | o estatístico |
| testes de unidade | [2,72; 8,53] | 7 | **[4 + S; 7 + S]** | 5 funções, uma por teste, ~1 por surpresa |
| testes do placar | [5,67; 10,33] | 10 | **6 + 2·S ± 1** | as 6 letras abaixo |
| erros do placar | [0; 3,17] | 2 | **[0; 3,17]** | o estatístico |
| redundância P821 | [0,565; 0,651] | 0,644 | **[0,565; 0,651]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1573, o crescimento da taxonomia dos substantivos.** O número de sinsets em cada profundidade r e o fator por nível e^λ da reta de ln N(r) contra r, nas profundidades 1 a 8.
- **Restrições, com peso:** (1) num espaço hiperbólico (uma árvore), N(r) cresce como a ramificação elevada a r (a P1492 dava ~4,8 filhos por pai interno); (2) mas a taxonomia não é cheia:
  ela fica mais fina perto das folhas e acaba em profundidade ~18; (3) **peso medido num caso escolhido por regra escrita antes (os verbos):** os verbos têm o máximo na profundidade 2 e
  encolhem depois (fator 0,54 por nível nas profundidades 1 a 8): a hierarquia dos verbos é rasa. Os substantivos são uma hierarquia funda (profundidade média ~8, P793).
- Exemplo à mão: *entity* (0) → *physical entity*, *abstraction*, *thing* (1) → … → *dog* (13).
- (a) o fator por nível nos substantivos em **[1,2; 3,0]**
- (b) a profundidade com mais sinsets em **[7; 11]**

**P1574, os gêmeos irredutíveis sobre GF(2).** Os polinômios de grau 15 (os números de 0x8000 a 0xFFFF) irredutíveis, e os pares (f, f ⊕ x ⊕ x²) com os dois irredutíveis.
- **A conta antes da medida:** Gauss: N(15) = (2¹⁵ − 2⁵ − 2³ + 2)/15 = **2.182** (teorema: fora do placar). Os gêmeos por um bit só (f, f ⊕ x) **não existem** (um irredutível de grau > 1 tem
  número ímpar de termos, e trocar um bit troca a paridade): descoberto na calibração, que deu 0 contra a conta de 48. Com dois bits (f ⊕ x ⊕ x²), a conta ingênua é N²/2¹⁴/2 = **145,3**.
  **Peso medido em casos escolhidos por regra (os graus ímpares logo abaixo, 11 e 13):** 28 contra 16,9 (razão 1,66) e 76 contra 48,4 (razão 1,57).
- (c) os gêmeos de grau 15 em **[180; 300]** (a conta × razão de 1,24 a 2,06)

**P1571–P1572, rodada 45:** no `dialogo/DIALOGO.md` (previsões (d) a (f)).

### Previsão nova, nascida de um resultado inesperado (registrada antes de medir o grau 17)

Os gêmeos de grau 15 deram 224, **1,54** vez a conta ingênua (145,3). A conta que explica o excesso, feita depois de ver os números (por isso só vira evidência num mundo novo): a série singular
de Hardy–Littlewood em F₂[x] (`p1579`). Para cada irredutível p de grau k, multiplicar pela chance de p não dividir nenhum dos dois, dividida pela chance se fossem independentes,
(1 − ν_p/2^k)/(1 − 1/2^k)²:
- p = x e p = x + 1: x + x² ≡ 0 (ν = 1), então f e o vizinho têm o mesmo resto: fator (1/2)/(1/4) = **2** cada (o termo constante e a paridade).
- p = x² + x + 1: x + x² ≡ 1, então os restos proibidos são 0 e 1 (ν = 2): fator (2/4)/(9/16) = **8/9**.
- todos os outros: ν = 2, fatores um pouco abaixo de 1.

A série vale S = **3,3315**, e a conta é N²/2^g · S/2. Contra a medida: grau 11, 28 contra 28,1 (razão **0,995**); grau 13, 76 contra 80,7 (**0,942**); grau 15, 224 contra 242,0 (**0,926**).
A razão cai devagar com o grau.

- **(g)** os gêmeos (f, f ⊕ x ⊕ x²) de grau 17 em **[642; 756]**: a conta de 755,5 vezes uma razão de 0,85 a 1,00 (continuação da queda, de 0,926 para ~0,91, com folga dos dois lados).
