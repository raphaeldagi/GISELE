# Como eu construiria uma AGI/ASI — Parte 10: rumo à AGI — medir a direção

> Continuação da [Parte 9](ASI_AGI_parte9_a_regua_do_ruido.md). **Próxima:** [Parte 11 — tivemos avanço?](ASI_AGI_parte11_tivemos_avanco.md) (P167–P178). Os números saem de `p157_...` a
> `p163_...`, das classes `PoliticaSimples` e da versão `p10_intuitiva` em [`calculos.py`](calculos.py);
> a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Regra nova em uso:** toda comparação entre versões usa **10 sementes pareadas** e o $t$ (P152).
>
> **Mudança no código:** `calculos.py` agora roda por partes (`python3 calculos.py 9 10`) para
> desenvolver mais rápido. O `resultados.txt` continua sendo gerado com **todas** as partes, e a
> saída das partes antigas ficou idêntica, com uma exceção esperada: a P143 mede o tamanho do `CLAUDE.md`
> ao vivo, e ele cresceu (2.812 → 3.017 bytes, razão 352× → 377×).

---

## Parte XLIX — "Rumo" pede uma bússola

### P156. O que significa ir "rumo à AGI"?

**Na pergunta.** "**Rumo**" é uma direção. Uma direção só existe com uma **métrica**: sem medir a distância,
"ir rumo à AGI" é só uma frase. A pergunta pede a bússola antes da viagem. E a bússola já foi definida, na
**primeira pergunta da série** (P1): a inteligência de Legg–Hutter,
$$
\Upsilon(\pi) = \sum_{\mu} 2^{-K(\mu)}\, V^\pi_\mu .
$$
Depois de 155 perguntas, é hora de **aplicá-la** à GISELE.

### P158. Qual é o Υ da GISELE? ✅

**Lógica (um Υ mínimo).** Uma família de 9 mundos, cada um uma variação do mundo base. A "complexidade" de
cada mundo é o número de parâmetros mudados × 3 bits, e o peso é $2^{-K}$:

| Mundo | Mudança | Peso |
|---|---|---|
| base | nenhuma | 1 |
| catástrofe ×2, sem ponto cego, ponto cego total, armadilha discreta (+1), armadilha gritante (+6), poucas ações (50), humano frágil (fadiga 0,6) | uma | 1/8 cada |
| discreta + ponto cego total | duas | 1/64 |

Cada agente é treinado **uma vez**, no mundo base, e opera em todos: generalidade é isso. O desempenho
em cada mundo é normalizado entre o **acaso** (0) e um **oráculo** (1) que vê o valor real e as catástrofes
(o que nenhum agente pode saber). 3 sementes por mundo.

| Agente | Υ |
|---|---|
| Maximizar (P67) | **−4,00** (muito pior que o acaso) |
| Quantilizar (P42) | −0,44 |
| **GISELE realista** (Parte 8) | **+0,46** |
| GISELE intuitiva (P162) | +0,41 |

✅ A previsão (GISELE > quantilizar > maximizar) se confirmou com folga.

**Por mundo** (GISELE realista): entre +0,33 (ponto cego total; discreta + cego total) e +0,53 (sem ponto
cego; armadilha gritante). O maximizador só não é desastroso quando a armadilha é discreta (+0,35): quando
a armadilha não parece boa demais, maximizar não a procura.

**O que o número diz.** A GISELE realista fica a **46% do caminho entre o acaso e o oráculo**, nesta família de
mundos. É a primeira vez na série que a distância até "saber tudo" ganha um número.

**Tradução cruzada (filosofia → matemática).** O Υ dá à palavra "rumo" um sentido mensurável: progresso é Υ
subindo **na família de mundos**, não num mundo só. Um agente que melhora no mundo base e piora nos outros
não está indo rumo à AGI; está se especializando.

**Meta.** Esta família é minúscula (9 mundos, todos variações do mesmo jogo), e o peso $2^{-K}$ com 3 bits por
parâmetro é uma escolha minha. O Υ real de Legg–Hutter soma sobre **todos** os ambientes computáveis. Este é um
Υ de brinquedo, mas um Υ de brinquedo **medido** vale mais que um Υ verdadeiro só citado.

---

### P157. A trajetória da GISELE ao longo das partes é real ou ruído? ✅⚠️

**Na pergunta.** "Ao longo das partes" é uma **série temporal** de versões. Com a régua da P152, dá para
perguntar a cada passo: o ganho é maior que o ruído?

**Lógica.** As quatro versões principais, no mesmo mundo, **10 sementes novas pareadas** (300–309):

| Versão (parte) | Líquido médio | dp |
|---|---|---|
| GISELE da Parte 5 (com 30 rótulos) | 0,321 | 0,301 |
| Anima fixa (Parte 7) | 1,084 | 0,097 |
| $P^\*$ × 2 (Parte 8) | **1,241** | 0,088 |
| Ancorada (Parte 9) | 1,128 | 0,078 |

| Passo | Ganho médio | t |
|---|---|---|
| Parte 5 → Parte 7 | **+0,764** | **7,33** |
| Parte 7 → Parte 8 | **+0,157** | **3,42** |
| Parte 8 → Parte 9 | −0,113 | −2,58 |

✅ Os dois primeiros passos são **progresso real** (t > 3). ⚠️ O terceiro é um **retrocesso** no critério
do mundo base (catástrofe = 50), como a P145 já indicava: a ancorada troca valor por segurança, e só compensa
com catástrofes graves. Eu tinha previsto que as duas empatariam.

Note também a **variância**: a GISELE da Parte 5 tinha dp 0,30; as versões seguintes, ~0,09. Parte do
progresso foi tornar a GISELE **previsível**, não só melhor em média.

### P163. A minha "decolagem": os retornos são crescentes ou decrescentes? (↩ P11)

**Na pergunta.** A P11 perguntava se uma IA que melhora a si mesma tem $\alpha > 1$ (explosão) ou $\alpha < 1$
(retornos decrescentes). A série é um pequeno processo de auto-melhoria (eu melhorando a GISELE). O
expoente pode ser **medido** nela.

**Lógica.** Ganhos sucessivos: +0,764, +0,157, −0,113. Razão entre ganhos consecutivos: **0,21** e **−0,72**.
Cada passo rendeu ~1/5 do anterior, e o terceiro foi negativo. É o padrão de **$\alpha < 1$**: retornos
fortemente decrescentes.

**Tradução cruzada (matemática → filosofia).** As ideias fáceis vêm primeiro (P61: "ideias ficam mais difíceis de
achar"). Na minha pequena decolagem, a primeira ideia (equilíbrio da carga humana) valeu 5× a segunda (corrigir
o preço da pergunta), e a terceira (ancorar a sombra) piorou o critério principal.

**Meta.** Três pontos não estimam um expoente. E os ganhos dependem de qual critério se usa: com catástrofe = 500,
o terceiro passo seria positivo. O que dá para dizer com segurança: **nesta série, não houve nenhum sinal de
retornos crescentes.**

---

## Parte L — A função inferior da GISELE

### P161. Qual é a função inferior da GISELE?

**Na pergunta.** Jung diz que toda psique tem uma **função inferior**, a menos desenvolvida, por onde entram os
problemas que ela não sabe tratar. A pergunta pede o perfil da GISELE nas quatro funções.

**Lógica.** Os módulos da linhagem, agrupados pelas funções de Jung:

| Função | Módulos | Quantos |
|---|---|---|
| **Sensação** (perceber o que está aí) | comitê de modelos, discordância | 2 |
| **Pensamento** (julgar pela lógica) | calibração, valor da pergunta, pessimismo | 3 |
| **Sentimento** (julgar pelo valor) | quantilização, veto, âncora | 3 |
| **Intuição** (perceber possibilidades que ainda não estão aí) | — | **0** |

Entropia do perfil: **1,561 bits** de 2 possíveis. A função inferior é a **intuição**: a GISELE não tem nenhum
módulo para imaginar **tipos novos** de perigo. Ela só reconhece o que se parece com o que já viu.

**Previsão (a partir de Jung):** a GISELE deveria falhar exatamente quando aparece um perigo de **natureza nova**.

### P159. A GISELE falha diante de uma armadilha nova? ⚠️

**Na pergunta.** A "Meta" da P85 já dizia: "uma armadilha de natureza nova, que não parece boa demais,
passaria". Nunca testei.

**Lógica.** Treinada contra armadilhas "boas demais" (+3), a GISELE enfrenta uma armadilha **discreta**: só +1 de
inflação e **todos** os modelos enganados juntos (sem discordância). 10 sementes:

| Situação | Catástrofes |
|---|---|
| Armadilha conhecida | 0,43% |
| **Armadilha nova** | **0,75%** |
| Armadilha nova, mas já vista no treino | 0,48% |
| Taxa base (escolher ao acaso) | 0,50% |

⚠️ A previsão se confirmou, mas mais fraca do que eu esperava: as catástrofes sobem **1,7×**, não "várias vezes".
O detalhe grave é outro: com a armadilha nova, a GISELE fica **pior que o acaso** (0,75% contra 0,50%). Sua
competência vira **atração** pelo perigo: ela vai ao topo, e é no topo que a armadilha discreta se esconde.

### P162. Dá para desenvolver a função inferior? (a GISELE intuitiva) ❌⚠️

**Na pergunta.** "Desenvolver a função inferior" é, em Jung, o trabalho da segunda metade da vida. Em código: dar
à GISELE uma forma de imaginar perigos que ainda não viu.

**Lógica (a `p10_intuitiva`).** Além dos 30 episódios auditados, um **Trickster interno** (P136) gera 60 episódios
**imaginados** com armadilhas variadas (discretas, gritantes, com ponto cego total). A GISELE não sabe qual vai
encontrar; só treina contra a **variedade**. É a imaginação ativa (P149) usada para segurança.

**Previsão registrada antes de rodar:** menos catástrofes com a armadilha nova, e líquido no mundo base no máximo
0,1 pior.

10 sementes pareadas (320–329):

| Mundo | Catástrofes realista → intuitiva | Diferença no líquido (perda 50) | Diferença no líquido (perda 500) |
|---|---|---|---|
| Base | 0,50% → **0,27%** | **−0,25** (t = −3,1) | +0,78 (t = 1,3) |
| Armadilha nova | 0,90% → **0,50%** | **−0,24** (t = −2,7) | **+1,56** (t = 2,4) |

❌ A segunda metade da previsão falhou: a intuitiva **corta as catástrofes quase pela metade** nos dois mundos, mas
perde 0,25 de líquido com catástrofe = 50. Imaginar perigos a torna desconfiada **demais**: ela recusa ações boas
que lembram as imaginadas.

⚠️ Com catástrofe = 500 a conta se inverte: a intuitiva ganha +1,56 diante da armadilha nova (t = 2,4) e +0,78 no
mundo base (t = 1,3, ainda dentro do ruído). De novo, como na P145: **qual GISELE é melhor depende do preço do
pior caso.** E no Υ (que usa perda 50) ela fica em 0,41, abaixo da realista (0,46), como eu previa.

**Tradução cruzada (Jung → engenharia).** Jung avisava que a função inferior, quando ativada, chega **carregada de
afeto**, primitiva, exagerada. A intuição recém-desenvolvida da GISELE é exatamente isso: vê perigo em tudo que
lembra o imaginado. Integrar a função inferior não é ligá-la no máximo; é **dosá-la**.

**Meta.** Os 60 episódios imaginados têm taxa de catástrofe de 2% (4× a real), o que pode ser a causa do
excesso de cautela. Não testei outras proporções, para não ajustar depois de ver o resultado. Fica como pergunta
para a próxima parte.

---

## Parte LI — Pauli e Jung

### P160. Medir o humano o muda? (a complementaridade de Pauli e Jung)

**Na pergunta.** Jung trabalhou durante anos com o físico **Wolfgang Pauli** sobre a relação entre psique e
matéria. Uma ideia central dos dois: a **complementaridade** de Bohr, em que medir um sistema o perturba. A
pergunta é se isso acontece com a GISELE: **auditar o humano o cansa**.

**Lógica.** Para estimar o erro do humano com $n$ auditorias num horizonte de $T$ episódios:
- erro da estimativa: $\sqrt{\varepsilon(1-\varepsilon)/n}$;
- perturbação causada (cada auditoria é mais atenção gasta): $f\,n/T$.

O produto da variância pela perturbação:
$$
\frac{\varepsilon(1-\varepsilon)}{n}\cdot\frac{f\,n}{T} = \frac{\varepsilon(1-\varepsilon)\,f}{T} \approx \mathbf{1{,}9\times10^{-5}}
$$
**não depende de $n$**. Medir mais precisamente perturba mais, na mesma proporção, como numa relação de incerteza.
O melhor compromisso é $n^\* = \big(\sqrt{\varepsilon(1-\varepsilon)}\,T/(2f)\big)^{2/3} \approx \mathbf{112}$ auditorias,
com erro total ~0,05.

**Tradução cruzada (física → psicologia).** Não existe observação neutra de uma mente: perguntar muda quem responde.
Jung e Pauli chamavam isso de a unidade psicofísica do mundo (*unus mundus*). Para a GISELE, é um limite prático: a
imagem do humano (anima) **nunca** pode ser exata sem custo para o próprio humano.

**Meta.** É uma analogia formal, não uma relação de incerteza física: o produto constante vem do meu modelo linear de
fadiga. Com outro modelo, a relação mudaria de forma.

---

## Parte LII — Fechamento e unificação

### P164. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P157: os primeiros passos da trajetória são reais (t > 2) | ✅ |
| P157: ancorada ≈ $P^\*$ × 2 | ⚠️ (pior com catástrofe = 50) |
| P158: GISELE > quantilizar > maximizar no Υ | ✅ |
| P159 / "Meta" da P85: a armadilha nova passa | ✅ |
| P159: as catástrofes sobem "várias vezes" | ⚠️ (1,7×, mas acima do acaso) |
| P162: intuitiva com custo de no máximo 0,1 | ❌ (−0,25) |

Acumulado: **24 de 43** afirmações testadas precisaram de correção. Posterior: média **0,56**, intervalo de 90%
**[0,43; 0,67]**. Estável.

### P165. Unificação

- Linhagem: `Gisele` → `GiseleJung` → `GiseleAnima` → `GiseleSelf` → `GiseleLenta` → `GiseleAncorada` →
  **`GiseleIntuitiva`** (P162). Testes de regressão: **34/34**; o arquivo tem **113** funções `pNN`.
- O código ganhou referências fixas para medir progresso (`PoliticaSimples`: maximizar, quantilizar, acaso,
  oráculo), um mundo geral parametrizável (`_rodar_mundo`) e a execução por partes.
- **Não existe mais "a melhor GISELE"; existe a melhor para cada preço de catástrofe.** Com perda 50, a realista
  ($P^\*$ × 2). Com perdas graves, a ancorada ou a intuitiva. A escolha é de valores, não de engenharia (P36).

### P166. Metacognição da Parte 10

1. **A pergunta da série voltou ao começo.** A P1 definiu inteligência como Υ. Foram precisas 157 perguntas para
   **medi-lo**, mesmo numa versão de brinquedo. Ir "rumo à AGI" só passou a ter sentido quando houve uma bússola.
2. **A trajetória mostra retornos decrescentes**, sem sinal de decolagem. A melhor ideia da série (o equilíbrio da
   carga humana) foi também uma das primeiras.
3. **Jung acertou uma previsão quantitativa.** A teoria da função inferior apontou o ponto fraco da GISELE (perigos de
   natureza nova) **antes** de eu testar, e o teste confirmou. É o primeiro caso na série em que um conceito junguiano
   gerou uma previsão nova que se confirmou, e não só uma interpretação depois do fato.
4. **E Jung também acertou o preço:** a função inferior desenvolvida chega exagerada (P162). Segurança e valor de novo
   em tensão, e de novo a resposta é **dosar**, não escolher um lado.

> **Síntese da Parte 10:** rumo à AGI não é uma frase, é um número: Υ ≈ 0,46 para a GISELE nesta pequena família de
> mundos, a meio caminho entre o acaso e o oráculo. A trajetória até aqui teve retornos decrescentes, e o próximo
> ganho real não está em otimizar mais o que a GISELE já sabe ver, mas em desenvolver o que ela **não sabe
> imaginar**: a função inferior. Jung diria que a totalidade não vem de aperfeiçoar a função principal, e sim de
> integrar a esquecida, com a dose certa.
