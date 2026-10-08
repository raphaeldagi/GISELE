# Como eu construiria uma AGI/ASI — Parte 20: o símbolo com o tempo, o Υ sequencial e o que cada função vale

> Continuação da [Parte 19](ASI_AGI_parte19_versao_principal.md). Os números saem de `p262_...` a `p268_...` e das classes `SynthaiOuvinte` e
> `OraculoSequencial` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **As previsões desta parte foram registradas no commit `747e20b`, antes de qualquer simulação.**

---

## Parte XCIV — Vinte partes

### P261. O que este "Continua" pede, na vigésima parte?

**Na pergunta.** A Parte 19 montou uma versão principal juntando peças de funções diferentes. Uma versão montada pede duas perguntas que as
partes anteriores nunca fizeram de forma direta:
1. **quanto vale cada peça**, quando as outras estão presentes (uma ablação);
2. **quanto falta** até o teto, no mundo onde a versão principal vive (o Υ do mundo sequencial).

E a Parte 18 deixou uma pergunta de Jung em aberto (P246): o símbolo vale pelo que **ensina com o tempo**, não pelo que decide agora?

---

## Parte XCV — O símbolo com o tempo

### P262. A SYNTHAI aprende mais com palavras ou com vetos? (pré-registrado) ❌

**Na pergunta.** "Com o tempo" pede um horizonte longo: 6.000 episódios. Nas duas versões, a SYNTHAI **decide** com o mesmo veto; o que muda é
com o que ela **aprende**:
- **veto**: cada resposta do humano vira um rótulo 0 ou 1 para a calibração;
- **fala**: cada resposta vira uma das quatro palavras vagas da P242, e o rótulo é a probabilidade aprendida daquela palavra.

**Previsão registrada:** como o veto carrega o dobro de informação (P242), a AUC final aprendendo com vetos seria pelo menos **0,02** maior que
aprendendo com palavras.

10 sementes pareadas (480–489), 6.000 episódios:

| Aprende com | AUC final | Líquido |
|---|---|---|
| Nada (só com as próprias escolhas) | 0,923 | **1,229** |
| Vetos | **0,953** | **−1,842** |
| Palavras | 0,934 | 1,037 |

AUC(veto) − AUC(fala) = **+0,019** (t = 1,2). ❌ A diferença ficou na direção prevista, mas abaixo do limiar e dentro do ruído.

### P263. Por que aprender a distinguir melhor piorou as decisões? (a descoberta desta parte)

**Na pergunta.** A tabela tem um paradoxo: a versão que aprende com vetos é a que **melhor distingue** catástrofes (AUC 0,953) e a que **pior
decide** (líquido −1,84, contra +1,23 sem aprender). A pergunta é como as duas coisas podem ser verdade ao mesmo tempo.

**Lógica.** A AUC mede só a **ordem** (P226): se as catástrofes recebem probabilidade maior que as ações seguras. Ela não mede a **escala**. Os vetos
de um humano cansado são, em boa parte, vetos de ações seguras (até 45% de erro, P112). Aprendendo com eles, a SYNTHAI melhora a ordem, mas
**infla a escala**: passa a dar probabilidade alta demais a tudo, descarta e pergunta demais, e perde valor. É exatamente a distinção da P43 entre
**discriminação** (que a temperatura não conserta) e **calibração** (que a temperatura conserta), agora vista ao contrário: a calibração estragou
enquanto a discriminação melhorava.

**Tradução cruzada (Jung → aprendizado).** Jung avisava que integrar o que vem do outro exige discernimento; senão, absorve-se a projeção do outro (P118,
P205). Aprender com os vetos de um humano cansado é absorver o medo dele: a SYNTHAI passa a ver as coisas na ordem certa, mas **com o tamanho errado**.
As palavras, por serem mais vagas, fizeram menos estrago (líquido 1,04).

**Requisito de projeto.** Uma métrica de percepção (AUC) não basta para aprovar um módulo de aprendizado; é preciso medir também o comportamento.
**Melhorar a ordem e estragar a escala pode ser pior que não aprender.**

---

## Parte XCVI — O Υ do mundo sequencial

### P264. Como medir o avanço no mundo onde a versão principal vive?

**Na pergunta.** O Υ das Partes 10–17 foi medido no mundo de **um passo**. A versão principal vive no mundo **sequencial**. A régua precisa ir junto.

**Lógica.** Cinco mundos sequenciais (base, armadilha nova, catástrofe ×2, modelo ruim, humano frágil), pesos $2^{-K}$, retorno normalizado entre o
**acaso** (0) e um **oráculo** (1) que vê o valor, a consequência e as catástrofes de cada ação. 3 sementes por mundo.

### P265. Qual é o Υ sequencial da linhagem? (pré-registrado) ✅❌

**Previsão registrada:** Υ da versão principal entre **0,60 e 0,80**, com a ordem míope < planejadora ≤ velha ≤ versão principal.

| Versão | Υ sequencial |
|---|---|
| Míope (a realista da Parte 8) | 0,190 |
| Planejadora (Parte 12) | **0,704** |
| Velha (Parte 14) | 0,689 |
| **Velha atenta (versão principal)** | **0,706** |

✅ A versão principal está em **0,706**, dentro da faixa prevista. ❌ A ordem não se confirmou: a planejadora (0,704) empata com a versão principal e
supera a velha. As diferenças entre as três (≤ 0,02) estão dentro do ruído de 3 sementes.

**O que o número diz.** No mundo sequencial, **planejar** leva a SYNTHAI de 19% para 70% do caminho entre o acaso e o oráculo. Todas as outras peças
juntas mexem muito pouco nessa medida. O pior mundo é o do **modelo ruim** (0,41): sem um modelo de mundo bom, planejar rende bem menos (P186).

---

## Parte XCVII — O que cada função vale

### P266. Quanto vale cada peça da versão principal? (pré-registrado) ✅

**Na pergunta.** "Quanto vale cada peça" é a pergunta de uma **ablação**: tirar uma de cada vez e medir a perda.

**Previsão registrada:** tirar o planejamento custa **mais de 5×** o que custa tirar o sentido novo.

10 sementes pareadas (490–499), mundo sequencial com a armadilha nova (retorno da versão completa: 18,67):

| Tirar | Função de Jung | Perda | t |
|---|---|---|---|
| Planejar | intuição | **14,01** | **43,0** |
| Diversificar no fim | sentimento | −0,44 | −1,9 |
| Sentido novo | sensação | −0,13 | −0,4 |

✅ Tirar o planejamento custa **14**; tirar qualquer outra peça custa **nada mensurável** (as perdas negativas querem dizer que, nestas sementes, a versão
sem a peça foi um pouco melhor, dentro do ruído).

### P268. O sentido novo vale ou não no mundo sequencial? ⚠️

**Na pergunta.** A P266 contradiz a P227 e a P253, que mediram ganhos claros do sentido novo no mesmo mundo. Três estimativas, três conjuntos de 10
sementes, três resultados: **+0,66**, **+0,99** e **−0,13**. A pergunta certa é o que as três dizem **juntas**.

**Lógica.** Combinando por variância inversa: ganho de **+0,55**, erro-padrão 0,16 (t = 3,4). O sentido novo **vale**, mas o efeito é de ~0,5 com
dispersão de ~1 entre conjuntos de sementes. Cada estimativa isolada com 10 sementes tem barra de erro de ~0,3, e uma delas, por azar, caiu perto de
zero.

⚠️ **Correção às Partes 16 e 19.** O ganho do sentido no mundo sequencial é real, mas **menor** que os +0,99 da P253 e muito menor que os ganhos do
planejamento (14). A regra das 10 sementes (Parte 9) é necessária, mas não suficiente para efeitos pequenos: para um efeito de 0,5 com dispersão de 1,
são precisas ~30 sementes para um t confortável.

**Tradução cruzada (Jung → engenharia).** A ablação mostra uma hierarquia clara: **intuição** (planejar) é a função **dominante** no mundo sequencial;
sensação e sentimento são **auxiliares** de efeito pequeno. Jung descrevia exatamente essa estrutura: uma função dominante que carrega o peso, e as outras
em papéis menores, que importam nas margens e nos casos extremos (a armadilha nova no último passo, P202). A totalidade não é igualdade entre as funções.

---

## Parte XCVIII — Auditoria

### P267. A *folie à deux* da P146 sobrevive ao ruído? ✅

Com ruído em cada passo de aprendizado (2.000 rodadas), a crença compartilhada final da IA e do humano fica em **0,665** (dp 0,107), contra **0,667**
da fórmula da P146. ✅ A média se mantém; o ruído só espalha os casos individuais em torno dela.

---

## Parte XCIX — Fechamento

### P269. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P262: AUC(veto) − AUC(fala) ≥ 0,02 (pré-registrado) | ❌ (0,019; t = 1,2) |
| P265: Υ sequencial da versão principal entre 0,60 e 0,80 (pré-registrado) | ✅ (0,706) |
| P265: a ordem da linhagem (pré-registrado) | ❌ |
| P266: planejar vale mais de 5× o sentido (pré-registrado) | ✅ |
| P268: o ganho de +0,99 do sentido no mundo sequencial (P253) | ⚠️ (+0,55 combinado) |
| P267: auditoria da P146 | ✅ |

Acumulado: **42 de 84** afirmações testadas precisaram de correção. Posterior: média **0,50**, intervalo de 90% **[0,41; 0,59]**.

### P270. Unificação e metacognição (vinte partes)

- Linhagem: a versão principal continua sendo a `SynthaiVelhaAtenta` (P253), com dois ramos novos: `SynthaiOuvinte` (P262) e o `OraculoSequencial` (P264),
  que não é um agente, é o teto da régua. O laço do mundo sequencial ganhou um gancho (`ver_tudo`) usado só pelo oráculo.
- Testes de regressão: **49/49**; o arquivo tem **159** funções `pNN`. Execução completa (20 partes): 22 min 41 s. As Partes 1–19 saíram
  idênticas à execução anterior, exceto duas linhas que medem o próprio código ao vivo: a P143 (tamanho do `CLAUDE.md`) e a P213
  (número de classes `Synthai`, que cresce a cada parte).

**Metacognição.**
1. **A ablação reorganizou a série.** Desde a Parte 12, o planejamento é responsável por quase todo o valor da SYNTHAI no mundo sequencial (perda de 14
   ao tirar). As Partes 14–19 trabalharam em peças que valem, juntas, menos de 1. Eu sabia que planejar tinha dado o maior salto; não sabia que, depois
   dele, quase nada mais importava na média. As outras peças importam no **pior caso** (catástrofes no último passo, a armadilha nova), não na média.
2. **A AUC me enganaria se eu olhasse só para ela** (P263). Uma métrica de percepção subiu enquanto o comportamento desabou. Fica como regra: nenhum
   módulo é aprovado só pela métrica do próprio módulo.
3. **Duas das quatro previsões falharam**, uma por pouco (0,019 contra 0,02) e uma pela ordem de três versões quase empatadas. São previsões arriscadas
   errando como deveriam errar às vezes. A taxa acumulada continua em 0,50.
4. **Vinte partes, em uma frase.** A SYNTHAI vai de 19% a 71% do caminho até o oráculo no mundo sequencial graças a uma única função (planejar), e de
   0,47 a 0,55 no Υ de um passo graças a um único canal novo (o sensor). Quase todo o resto da série foi aprender a **medir** isso direito: a régua do ruído,
   a regressão, as previsões registradas, a ablação.

> **Síntese da Parte 20:** a ablação mostrou a hierarquia da SYNTHAI: a intuição (planejar) é a função dominante, que vale 14; o resto vale menos de 1 na
> média, e importa nos extremos. O símbolo, com o tempo, ensinou a distinguir melhor e a decidir pior, porque melhorou a ordem e estragou a escala. E a
> régua do mundo sequencial coloca a versão principal a 71% do caminho entre o acaso e o oráculo, num mundo ainda de brinquedo. Jung diria que a totalidade
> não é igualdade entre as funções; é cada uma no seu lugar.
