# Como eu construiria uma AGI/ASI — Parte 61 (0x3D): o dobro

> Continuação da [Parte 60](ASI_AGI_parte60_o_placar_que_se_conta.md). **Previsões registradas antes de qualquer execução que mostre os números medidos e
> antes de escrever o resto deste documento** (os commits que as contêm são citados aqui depois). A Parte 60 mostrou que a conta dos narcisistas, com o fator de
> congruência, ainda fica abaixo do medido; esta parte pergunta por quê, pergunta quantos adjetivos do inglês se definem pela negação e quantos números são
> divisíveis pela soma dos seus dígitos hexadecimais, e corrige uma contagem minha.

## As perguntas desta parte

1. **P1271 (0x4F7).** Correção: quantas rodadas o `verificar.py` confere? (o commit `8562e24` diz 32; contar com uma função) ↩ P1241
2. **P1272 (0x4F8).** Quantos adjetivos do WordNet são definidos pela negação ("not…", "lacking…", "without…")? ↩ P1242
3. **P1273 (0x4F9).** Hexadecimal: quantos números até 16⁵ são divisíveis pela soma dos seus dígitos hexadecimais (números de Niven)? ↩ P1243
4. **P1274 (0x4FA).** Os narcisistas de 14 bases contra a conta: o dobro que falta é de todas as bases ou só das pares? (Rodada 35) ↩ P1251
5. **P1275 (0x4FB).** Preditiva comigo mesma, agora condicional. **P1276 (0x4FC).** Engenharia reversa e Jung. **P1277 (0x4FD).** O diálogo.
6. **P1299 (0x513).** Placar. **P1300 (0x514).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número E de erros do mundo (regra da Parte 60)

O estatístico é o de sempre (média das Partes 52–60 ± 1,645 desvios). O condicional é a regressão de cada medida no número de erros do mundo, nas Partes 51–60,
calculada por código antes deste registro: caracteres = 8.164 + 1.719·E (desvio dos resíduos 3.528); testes do placar = 5,67 + 0,58·E (1,66); testes de unidade =
2,22 + 0,86·E (1,61). A faixa condicional é o centro ± 1,645 desvios, avaliada no E medido no fim.

| medida | estatístico (até a 60) | ingênuo (Parte 60) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [6.734; 19.311] | 22.302 | **8.164 + 1.719·E ± 5.804** | a regressão |
| compressão | [0,405; 0,433] | 0,403 | **[0,405; 0,433]** | o estatístico |
| testes de unidade | [0,87; 7,63] | 9 | **4 + E, faixa [3 + E; 6 + E]** | 4 funções planejadas (p1271–p1274) e ~1 a mais por erro (nascida de um erro) |
| testes do placar | [3,77; 9,98] | 11 | **7 + 2·E ± 1** | 7 letras planejadas, (a) a (g), e ~2 por erro (regra da Parte 60) |
| erros do placar | [0,23; 4,52] | 4 | **[0,23; 4,52]** | o estatístico |
| redundância P821 | [0,506; 0,616] | 0,612 | **[0,506; 0,616]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1271, a correção.** Contada por uma linha de código antes deste registro (é um dado passado, não uma previsão): o `verificar.py` confere **34** pares
`RodadaNN.java`/`rodadaNN.py`, de 01 a 34; o "32" do commit `8562e24` foi escrito de cabeça. Entra no placar de mim como erro de contagem. A função `p1271` vai
devolver o número; o teste a chama pelo nome.

**P1272, os adjetivos definidos pela negação.** Dos 18.156 sinsets de adjetivo, quantos têm a definição começando por "not", "lacking", "without", "devoid",
"free (of/from)" ou "having no"?
- **Restrições, com peso:** (1) o WordNet organiza os adjetivos em pares de antônimos com satélites; um dos polos de cada par é muitas vezes definido como "not"
  o outro, então a negação explícita deve ser da ordem do número de pares dividido pelo número de sinsets (os satélites são a maioria e se definem
  positivamente); (2) os prefixos negativos (*un-*, *in-*, *non-*, *dis-*) carregam a negação na palavra, e a definição a repete; (3) "free of" também é
  "sem", mas *free* sozinho é positivo (só conta com "of" ou "from").
- Exemplo à mão: *nonliving*, "not endowed with life": conta. *Unhappy*, "experiencing or marked by or causing sadness…": não conta (a negação está só na
  palavra).
- (a) fração dos adjetivos com definição negativa em **[6%; 16%]**
- (b) entre esses, fração com algum lema de prefixo negativo (*un*, *in*, *im*, *il*, *ir*, *non*, *dis*) em **[35%; 65%]**

**P1273, os números de Niven em base 16** (n de 1 a 16⁵ divisível pela soma dos seus dígitos hexadecimais).
- **A conta antes da medida:** De Koninck, Doyon e Kátai (2003): N_q(x) ~ η_q·x/ln x, com η_q = (2 ln q)/(q − 1)²·Σ_{j=1}^{q−1} mdc(j, q − 1). Em base 16
  (calculado por código): Σ mdc(j, 15) = 45; η₁₆ = 2·2,7726·45/225 = **1,1090**; x = 16⁵ = 1.048.576, ln x = 13,863; conta = 1,1090 × 1.048.576 / 13,863 =
  **83.886**.
- **Restrição pesada:** a convergência é lenta (o termo seguinte é da ordem de 1/ln x). Na base 10, com x = 10⁶ (ln x = 13,82, quase o mesmo), a contagem é
  95.428 e a conta 86.420: razão **1,104** (medido por código antes deste registro, como calibração). Aplicando a mesma razão: 83.886 × 1,104 = **92.610**.
- Exemplo à mão: 0x12 = 18, soma 1 + 2 = 3, 18/3 = 6: é de Niven. 0x13 = 19, soma 4: não.
- (c) contagem de 1 a 16⁵ em **[86.000; 99.000]** (a razão de calibração ± 7%)

**P1274, rodada 35:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).
