# Como eu construiria uma AGI/ASI — Parte 38 (0x26): o agente que aprende a suposição

> Continuação da [Parte 37](ASI_AGI_parte37_mudanca_bayesiana.md). A tabela da P580 mostrou cinco agentes, cada um uma suposição sobre o mundo, e
> nenhum vencendo as três colunas. Esta parte testa o passo bayesiano seguinte: em vez de escolher a suposição, **aprendê-la**, por média de
> modelos sobre o risco de mudança H. Novidades: `ThompsonMistura` ([`synthai/decisao.py`](synthai/decisao.py)); testes em
> [`synthai/testes_parte38.py`](synthai/testes_parte38.py); números de `p541_...` a `p543_...` em [`calculos.py`](calculos.py). Diálogo, rodada 9.
>
> **Contas e previsões no commit `cdb1a18`, antes de rodar.**

---

## As perguntas desta parte

1. **P541 (0x21D).** Uma mistura de modelos sobre H aprende a suposição e decide bem nos três mundos? ↩ P580
2. **P542 (0x21E).** Sem normalizar, em que passo o produto das verossimilhanças vira `0x0p+0`? (trilha hexadecimal)
3. **P543 (0x21F).** A lei de Heaps no data lake: β = 1/s? (trilha do dicionário) ↩ P463
4. **P544 (0x220).** Jung: a função transcendente e a média de modelos.
5. **P545 (0x221).** O diálogo, rodada 9.
6. **P609 (0x261).** Placar. **P610 (0x262).** Unificação.

---

### P541 (0x21D). A mistura aprende a suposição? (pré-registrado) ❌✅❌✅✅

**Na pergunta.** "Aprender a suposição" é pôr uma distribuição a priori sobre o que antes era escolhido à mão. Quatro modelos, H ∈ {0; 1/2000;
1/500; 1/100}, peso a priori ¼ cada. Cada observação multiplica o peso de cada modelo pela probabilidade que ele deu a ela:
$$
\log w_m \leftarrow \log w_m + \log P_m(r_t),\qquad P_m(r_t) = (1-H_m)\sum_h w_h\,\frac{a_h \text{ ou } b_h}{a_h+b_h} + \frac{H_m}{2}.
$$
**A garantia exata (uma identidade).** Para qualquer sequência, −ln Σ_m ¼·P_m ≤ −ln ¼ − ln P_m* para cada m*, porque uma soma de termos positivos
é maior que cada termo. Então a perda logarítmica da mistura fica no máximo **ln 4 = 1,386 nat** acima da do melhor modelo. A Rodada 9 conferiu:
1,1 nat.

**Medido:**

| mundo | exato | BOCPD 1/500 | **mistura** | melhor anterior |
|---|---|---|---|---|
| estacionário | 30,7 | 86,6 | **56,3** | 30,7 |
| dano, custo | 69,8 | 46,0 | **48,9** | 14,1 |
| muda a cada 500 | 808,7 | 371,9 | **385,5** | 367,7 |

Pesos finais médios (H = 0; 1/2000; 1/500; 1/100): estável **0,784; 0,207; 0,008; 0,000**; no que muda **0,000; 0,000; 0,168; 0,832**.

(a) estacionário ≤ 45 ❌ (56,3); (b) que muda ≤ 400 ✅ (385,5); (c) dano ≤ 46,0 ❌ (48,9); (d) peso de H = 0 no estável ≥ 0,5 ✅ (0,78); (e) H ≥
1/500 no que muda ≥ 0,8 ✅ (1,00).

**O achado: os pesos aprendem, a decisão não aproveita.** A mistura **sabe** em que mundo está (0,78 e 1,00 nos modelos certos) e mesmo assim
decide pior que o modelo certo sozinho. Duas razões:
1. **O começo.** Os pesos começam iguais; até a evidência separar os modelos, um quarto das escolhas vem de cada um. No estável, as ~200
   primeiras escolhas misturam modelos que exploram demais: 56,3 − 30,7 = 25,6 de custo de aprendizado da suposição.
2. **A cota é de predição, não de decisão.** Perder ≤ ln 4 nat na previsão não limita o arrependimento: um modelo pode prever quase tão bem e
   decidir muito pior (prever bem os braços ruins não ajuda a escolher o bom).

**O que os pesos dizem sobre o mundo que muda.** O modelo que ganhou foi H = 1/100, **cinco vezes** o risco verdadeiro (1/500). Num bandido, a
mudança de um braço só é vista quando ele é puxado; para os dados que o agente vê, o mundo parece mudar mais depressa do que muda.

**Tradução cruzada.** Saber qual teoria do mundo é a certa e agir de acordo com ela são duas competências.

### P542 (0x21E). Em que passo o produto vira `0x0p+0`? (pré-registrado) ✅✅✅

**Lógica, a conta antes.** O menor double positivo é 2⁻¹⁰⁷⁴ (`0x0.0000000000001p-1022`); um produto que cai abaixo de 2⁻¹⁰⁷⁵ arredonda para 0,0.
Se cada passo custa h bits, o zero vem em 1075/h passos. Com o agente puxando quase sempre o melhor braço, h ≈ H₂(p*). Semente 4010, p* = 0,9655:
$$
H_2(0{,}9655) = -0{,}9655\log_2 0{,}9655 - 0{,}0345\log_2 0{,}0345 = 0{,}0487 + 0{,}1675 = 0{,}216\ \text{bits};\qquad 1075/0{,}216 = 4971.
$$
O subnormal começa 52 bits antes (a mantissa vai perdendo bits): 52/0,216 = 241 passos antes.

**Medido:** subnormal no passo **3815**; zero no passo **4036**; **0,2666 bits por passo**. (f) zero entre 3000 e 5500 ✅; (g) bits por passo em
[0,2; 0,36] ✅; (h) do subnormal ao zero, entre 150 e 400 passos ✅ (221).

**A conta refeita com o h medido:** 1075/0,2666 = **4032** (medido 4036: erro de 4 passos, 0,1%); 52/0,2666 = 195 (medido 221: os primeiros
passos subnormais perdem bits mais devagar que a média). O h medido (0,267) é maior que H₂(p*) (0,216) porque a exploração do começo custa ~1 bit
por passo.

*Ao acaso e contra o ingênuo.* O ingênuo "um produto de probabilidades ~½ zera em ~1075 passos" erraria por 4×. A conta com H₂(p*) errou por
23%; com o h medido, por 0,1%.

**Tradução cruzada.** É por isso que todo o código bayesiano desta série guarda **logaritmos** de pesos: a evidência acumulada de um agente que
vive 4000 passos não cabe num double.

### P543 (0x21F). Heaps no data lake (pré-registrado) ❌

V(n), o vocabulário depois de n palavras de definições lidas em ordem aleatória: **β = 0,416**, longe de 1/s = 0,926 ou 0,935. (i) ❌.

**Por quê.** A relação β = 1/s vale para um vocabulário **aberto**, que cresce sem limite. O vocabulário das definições é **fechado**: são só as
32.927 palavras que o próprio dicionário define. Das 583.368 palavras lidas, a curva de V(n) já está se achatando contra esse teto, e a
inclinação em log-log cai. **A forma da estrutura (fechada) contradiz a suposição da lei (aberta)**, o mesmo tipo de erro das Partes 31 e 34.

**Tradução cruzada.** Um dicionário é uma língua que se fecha sobre si mesma (a autopoiese da P404). A lei de Heaps mede a abertura de uma língua;
aqui ela mediu o fechamento.

### P544 (0x220). Jung: a função transcendente e a média de modelos

Em Jung, a **função transcendente** une duas atitudes opostas numa terceira, que não é nenhuma delas. A mistura de modelos não faz isso: ela
**sorteia** entre as atitudes, na proporção da evidência. **Funciona:** a evidência separa as atitudes (0,78 contra 0,00 no estável). **Quebra:**
o que Jung chama de transcendente seria um modelo novo (por exemplo, um H que muda com o tempo), não uma média dos antigos. A P541 mostra o
preço de não transcender: a média decide pior que a melhor parte.

### P545 (0x221). O diálogo, rodada 9

A média de modelos em Java: **13 números idênticos bit a bit** depois de ~10.000 logaritmos e exponenciais (j) ✅. A resposta à pergunta da Rodada
8: a SYNTHAI mora no arquivo único (o que ela é) **e** na igualdade dos bits entre as linguagens (a prova de que é independente delas). Nova regra no
`CLAUDE.md`: toda peça nova que decide passa por uma rodada.

### P609 (0x261). Placar

(a) ❌ (b) ✅ (c) ❌ (d) ✅ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ❌ (j) ✅. Parte 38: 10 testes, 3 erros. Acumulado: **118 erros em 307 testes**; taxa
média 0,39, intervalo 90% [0,34; 0,43].

### P610 (0x262). Unificação e metacognição

- **Novo:** `ThompsonMistura` (2 testes; 100 no pacote). Regressão: + P542 (o zero previsto, 4971).
- **Linhagem:** a `ThompsonMistura` entra como o módulo de decisão que aprende a suposição; a versão principal continua a `SynthaiComposta`.

**Metacognição.** As três previsões que acertaram (f, g, h) eram sobre **aritmética de ponto flutuante**, onde a conta é exata. As três que
erraram eram sobre **comportamento** (a, c) e sobre uma lei empírica aplicada fora do seu domínio (i). O padrão das Partes 31–38 se repete: eu
acerto as contas de mecanismo único e erro as de comportamento com dois mecanismos.

> **Síntese da Parte 38:** a média bayesiana de modelos sobre o risco de mudança aprendeu a suposição certa (0,78 de peso no modelo sem mudança no
> mundo estável; 1,00 nos modelos com mudança no outro) e mesmo assim decidiu pior que o modelo certo sozinho (56,3 contra 30,7), porque aprender a
> suposição custa e porque prever bem não é decidir bem. A garantia exata da mistura (perda ≤ melhor + ln 4) valeu (1,1 nat). O produto das
> verossimilhanças virou 0,0 no passo 4036, a 4 passos da conta feita com o custo medido. E a lei de Heaps falhou no data lake (β = 0,42), porque
> o vocabulário de um dicionário é fechado.

---

**Fontes desta parte**
- Média bayesiana de modelos e a cota de mistura em perda logarítmica: a identidade −ln Σ π_m P_m ≤ −ln π_m − ln P_m (derivação na própria resposta), como na predição com especialistas
- Ponto flutuante subnormal: o menor double positivo, 2⁻¹⁰⁷⁴, é o `sys.float_info` do Python (`float_info.min` = 2⁻¹⁰²² é o menor normal)
- Detecção de mudança e o modelo de risco H: [Adams e MacKay, arXiv 0710.3742](https://ar5iv.arxiv.org/html/0710.3742)
- A lei de Heaps e Zipf: [Piantadosi (2014), PMC4176592](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176592)
