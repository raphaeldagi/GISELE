# Como eu construiria uma AGI/ASI — Parte 67 (0x43): prever o previsto

> Continuação da [Parte 66](ASI_AGI_parte66_o_endereco_da_falta.md). Pedido do usuário: **"Programe sem parar. Em loop infinito. Tem como você prever o que foi previsto?
> Tem como você prever o que foi previsto e fazer engenharia reversa em metacognição?"** Esta parte responde em três camadas, em ordem: (1) ler todas as minhas previsões
> do mundo desde a Parte 53 e fazer a engenharia reversa da regra com que eu as escrevo; (2) **prever as previsões desta parte antes de escrevê-las** (registrado primeiro,
> num commit só para isso); (3) escrever as previsões do mundo, medir, e pontuar as duas coisas: o mundo contra as minhas previsões, e as minhas previsões contra a
> previsão delas.

## A engenharia reversa do que eu já previ (dados passados, medidos antes deste registro)

`p1452_minhas_previsoes` lê, nas Partes 53 a 66, os vereditos da linha "Do mundo" e a faixa **[a; b]** de cada letra (no documento ou na rodada do diálogo da parte);
`p1453_engenharia_das_previsoes` mede:
- **97** previsões do mundo; **51** com faixa numérica legível (a leitura só pega a faixa escrita na mesma linha da letra, e a primeira, quando há duas).
- Acerto: **69,1%** no total; **64,7%** com faixa; **73,9%** sem faixa (as categóricas, como "IGUAIS em Java").
- A largura relativa w = (b − a)/(|a| + |b|): mediana **0,333**, quartis **0,20** e **0,60**.
- **Por terço de largura, o acerto cai com a largura:** as faixas estreitas (w mediano 0,15) acertam **70,6%**, as do meio (0,33) **70,6%**, as largas (0,71) **52,9%**. O
  contrário do que uma faixa "honesta" faria. O motivo, lido nas largas: elas são as que eu escrevo quando não sei nem o nível (as que cruzam o zero acertaram 2 de 5),
  e alargar não compensa não saber onde o número mora.
- **A minha largura é previsível:** prever o w de cada faixa pela mediana das outras erra em média **0,229**; o ingênuo "o w da faixa anterior" erra **0,253**.
- **15,7%** das faixas têm w a menos de 0,05 de 1/3.

## Previsões sobre as minhas previsões desta parte (registradas antes de escrever qualquer previsão do mundo desta parte)

Terceiro placar, separado do mundo e do "sobre mim":
- **(m1)** a mediana de w das faixas numéricas do mundo desta parte em **[0,20; 0,60]** (o intervalo interquartil do histórico).
- **(m2)** o número de previsões do mundo desta parte (letras na linha "Do mundo") em **[6; 11]** (o mínimo e o máximo das Partes 57 a 66 com faixa: de 5 a 11; sem a 57).
- **(m3)** a fração de acertos do mundo desta parte em **[0,44; 0,89]** (a faixa binomial de 90% em torno de 0,69 com ~9 previsões).
- **(m4)** o efeito do observador: sabendo que a mediana histórica é 1/3, eu poderia escrever faixas perto de 1/3 para acertar (m1). A regra é não fazer isso (as faixas saem
  da calibração e da conta, como sempre). Previsão: a fração das faixas desta parte com w a menos de 0,05 de 1/3 fica em **[0; 0,40]** (histórico 0,157; se eu estiver
  copiando a mediana, passa de 0,40).
- **(m5)** "prever o que foi previsto", em retrovisão: o preditor "mediana histórica, 1/3" erra o w das faixas desta parte, em média, entre **[0,05; 0,35]**.

## As perguntas desta parte

1. **P1451 (0x5AB).** O z dos primos palíndromos tem tendência com a base, ou só uma dispersão maior que a do σ? (Rodada 41, bases novas 35 a 40) ↩ P1421
2. **P1452 (0x5AC).** As minhas previsões desde a Parte 53, lidas por uma função. **P1453 (0x5AD).** A engenharia reversa delas (acima).
3. **P1454 (0x5AE).** Quantos substantivos do WordNet têm dois ou mais hiperônimos (herança múltipla)? ↩ P1422
4. **P1455 (0x5AF).** Hexadecimal: os números automórficos (n² termina em n) em base 16 e em base 12. ↩ P1423
5. **P1456 (0x5B0).** Preditiva comigo mesma. **P1457 (0x5B1).** Engenharia reversa e Jung. **P1458 (0x5B2).** O diálogo.
6. **P1479 (0x5C7).** Placar (três: o mundo, eu, as minhas previsões). **P1480 (0x5C8).** Unificação.

## Previsões pré-registradas (escritas depois do registro de (m1) a (m5))

### Sobre mim (placar separado), condicionais ao número S de surpresas (contadas pelo script)

Planejadas: 7 previsões do mundo ((a) a (g)) e 5 funções (p1451, p1452, p1453, p1454, p1455).

| medida | estatístico (até a 66) | ingênuo (Parte 66) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [10.865; 21.140] | 14.447 | **[10.865; 21.140]** | o estatístico |
| compressão | [0,404; 0,425] | 0,413 | **[0,404; 0,425]** | o estatístico |
| testes de unidade | [1,90; 7,85] | 4 | **[4 + S; 7 + S]** | 5 funções planejadas, uma por teste, ~1 por surpresa |
| testes do placar | [6,06; 10,69] | 9 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [1,12; 4,13] | 3 | **[1,12; 4,13]** | o estatístico |
| redundância P821 | [0,567; 0,637] | 0,607 | **[0,567; 0,637]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1454, a herança múltipla.** A fração dos sinsets de substantivo com dois ou mais hiperônimos.
- **Restrições, com peso:** (1) a taxonomia dos substantivos é quase uma árvore, mas tem herança múltipla em papéis (*person* que é também *worker*) e em substâncias;
  (2) **peso medido num caso escolhido por regra escrita antes (a outra classe com hierarquia, os verbos):** 0,23% (31 de 13.767). Os substantivos são uma hierarquia mais
  funda e mais rica que a dos verbos.
- Exemplo à mão: *actor* é *performer*; *president* é *head of state* e *presiding officer* (dois pais).
- (a) a fração em **[0,5%; 5%]**

**P1455, os automórficos.** Os n ≥ 2 com n² terminando nos mesmos dígitos que n (n² ≡ n mod bᵏ, k = dígitos de n), até b⁶.
- **A conta antes da medida:** n(n − 1) ≡ 0 (mod bᵏ) com n e n − 1 coprimos exige que cada potência de primo de bᵏ divida n ou n − 1. Em base 16 = 2⁴, bᵏ é potência de um primo só:
  só n ≡ 0 ou 1, nenhum automórfico além dos triviais (**teorema; fora do placar, porque não pode errar**). Em base 12 = 2²·3, há 2² = 4 soluções módulo 12ᵏ, duas não triviais,
  por k; uma solução de k dígitos precisa de dígito inicial ≠ 0 (chance 11/12): conta 2 × 6 × 11/12 = **11**. **Peso medido num caso escolhido por regra (a base 10 inteira até
  10⁶, também com dois primos):** 10 medidos contra a conta 2 × 6 × 9/10 = 10,8.
- Exemplo à mão: base 10, 76² = 5.776, termina em 76.
- (b) os automórficos da base 12 até 12⁶ em **[8; 12]**

**P1451, rodada 41:** no `dialogo/DIALOGO.md` (previsões (c) a (f)).
