# Como eu construiria uma AGI/ASI — Parte 66 (0x42): o endereço da falta

> Continuação da [Parte 65](ASI_AGI_parte65_o_que_nao_e_divisor.md). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de
> escrever o resto deste documento.** A Parte 65 deixou a base 21 a −3σ da conta dos primos palíndromos, com todas as correções. Esta parte pergunta se a falta tem
> endereço (alguns primeiros dígitos, alguns dígitos do meio), se os sinsets de verbos têm mais sinônimos que os de substantivos, e quantos números têm a mesma soma de
> dígitos em base 10 e em base 16.

## As perguntas desta parte

1. **P1421 (0x58D).** A falta de primos palíndromos da base 21 tem endereço? E o viés continua nas bases 23 a 28? (Rodada 40) ↩ P1391
2. **P1422 (0x58E).** Os sinsets de verbos do WordNet têm mais sinônimos que os de substantivos? ↩ P1392
3. **P1423 (0x58F).** Hexadecimal: quantos n < 16⁵ têm a mesma soma de dígitos em base 10 e em base 16? ↩ P1393
4. **P1424 (0x590).** Preditiva comigo mesma. **P1425 (0x591).** Engenharia reversa e Jung. **P1426 (0x592).** O diálogo.
5. **P1449 (0x5A9).** Placar. **P1450 (0x5AA).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 3 funções (p1421, p1422, p1423).

| medida | estatístico (até a 65) | ingênuo (Parte 65) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [9.945; 21.332] | 16.022 | **[9.945; 21.332]** | o estatístico |
| compressão | [0,404; 0,425] | 0,410 | **[0,404; 0,425]** | o estatístico |
| testes de unidade | [1,90; 7,85] | 4 | **[2 + S; 5 + S]** | 3 planejados, ~1 por surpresa |
| testes do placar | [5,73; 10,52] | 9 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,63; 4,12] | 2 | **[0,63; 4,12]** | o estatístico |
| redundância P821 | [0,548; 0,641] | 0,608 | **[0,548; 0,641]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1422, os sinônimos por classe.** O tamanho médio do sinset (número de lemas) no WordNet, por classe.
- **Restrições, com peso:** (1) os verbos do WordNet são muito polissêmicos e agrupados em sinsets largos de verbos frasais e sinônimos (*take*, *get*, *have*); (2) os
  substantivos incluem muitos nomes próprios e termos técnicos de um lema só. **Peso medido num caso escolhido por regra escrita antes (o português inteiro da
  OpenWordNet-PT, mesma estrutura, outra língua), por código antes deste registro:** verbos 1,726, substantivos 1,574: razão **1,097**.
- Exemplo à mão: o sinset de *dog* tem 3 lemas (*dog*, *domestic dog*, *Canis familiaris*); o de *run* (correr) tem 1.
- (a) a razão (tamanho médio dos sinsets de verbo)/(de substantivo) em **[0,95; 1,30]**
- (b) o tamanho médio dos sinsets de substantivo em **[1,45; 1,95]**

**P1423, a mesma soma em base 10 e em base 16.** A fração dos n de 1 a 16⁵ − 1 com s₁₀(n) = s₁₆(n).
- **Restrições, com peso:** (1) s₁₀(n) ≡ n (mod 9) e s₁₆(n) ≡ n (mod 15), então as duas somas têm o mesmo resto módulo 3, **sempre**: a chance de igualdade é ~3 vezes
  a de duas somas independentes; (2) as distribuições das duas somas têm médias diferentes (~27 e ~37 para n < 16⁵) e só se sobrepõem nas caudas. **A conta antes da
  medida (por código):** independência × 3 = **0,0662**. **O peso medido em casos escolhidos por regra (os intervalos inteiros n < 10⁴ e n < 10⁵):** medido/conta =
  1,079 e 1,022, indo para 1.
- Exemplo à mão: n = 10: s₁₀ = 1, s₁₆ = 10 (0xA): não. n = 1: 1 = 1: sim.
- (c) a fração em **[0,0630; 0,0715]** (a conta × [0,95; 1,08])

**P1421, rodada 40:** no `dialogo/DIALOGO.md` (previsões (d) a (h)).
