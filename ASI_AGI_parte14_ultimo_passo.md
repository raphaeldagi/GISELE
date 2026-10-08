# Como eu construiria uma AGI/ASI — Parte 14: o último passo, a memória de um só golpe e o peso do passado

> Continuação da [Parte 13](ASI_AGI_parte13_transferencia.md). **Próxima:** [Parte 15 — SYNTHAI](ASI_AGI_parte15_synthai.md) (P212–P221). Os números saem de `p203_...` a `p207_...` e das classes
> `SynthaiVelha` e `SynthaiMemoria` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.

---

## Parte LXVI — O último passo

### P201. O que este "Continue" pede?

**Na pergunta.** A Parte 13 deixou registrado o próximo passo: as catástrofes se concentram no **último passo** do episódio, onde o
planejamento já não protege, e o problema de fundo é de **percepção** (a SYNTHAI não reconhece certas armadilhas). "Continue" pede
atacar as duas coisas, uma de cada lado: o comportamento no fim (P202) e a percepção (P204).

### P202. Como agir quando não há mais futuro? (pré-registrado na P193) ✅

**Na pergunta.** "Quando não há mais futuro" é a situação do último passo, e também a situação que Jung descrevia para a **segunda
metade da vida**: quando acumular já não faz sentido, o que orienta a ação? A pergunta separa duas formas de cautela:
- **cautela instrumental**: ser prudente porque há futuro a proteger (desaparece no último passo);
- **cautela de caráter**: ser prudente como hábito, com ou sem futuro (a virtude como hábito de Aristóteles).

**Lógica.** A `SynthaiVelha` muda uma coisa só: no último passo, em vez de ir ao topo das 2 melhores ações, sorteia entre as **20%
melhores** (a quantilização da P42, usada exatamente onde o planejamento deixa de diversificar).

**Previsão registrada (P193):** menos catástrofes no último passo, retorno praticamente igual.

10 sementes pareadas (370–379):

| Versão | Retorno | Catástrofes | Catástrofes por passo (1 → 5) |
|---|---|---|---|
| Planejadora | 19,998 | 1,68% | 4, 8, 12, 16, **27** |
| **Velha** | 19,960 | **1,38%** | 10, 5, 15, 13, **12** |

Velha − planejadora: −0,04 (t = −0,15). ✅ As catástrofes do último passo caíram **pela metade** (27 → 12), as totais caíram 18%, e
o retorno não mudou.

**Tradução cruzada (Jung → ética).** No último passo, a cautela que sobrevive é a de **caráter**. A SYNTHAI planejadora era prudente
só enquanto havia futuro; a velha continua prudente quando o futuro acaba. Jung via na velhice bem vivida a passagem do acumular
para o **sentido**; aqui, a passagem é de "evitar perder o que vem" para "não ir ao extremo, por princípio".

**Meta.** Os passos 1 e 3 tiveram um pouco mais de catástrofes na velha (10 e 15 contra 4 e 12). Com contagens tão pequenas, isso
está dentro do ruído, mas registro.

---

## Parte LXVII — A memória de um só golpe

### P203. Dá para corrigir a percepção com memória? (↩ P193)

**Na pergunta.** A P193 mostrou que as catástrofes que passam são as que a calibração **não reconhece**. Se a SYNTHAI não reconhece
uma armadilha nova pela primeira vez, ela pode ao menos reconhecê-la **na segunda**? A pergunta é sobre aprender com **um único
exemplo**.

### P204. A memória de um só golpe protege contra a armadilha nova? (pré-registrado) ❌

**Lógica (a `SynthaiMemoria`).** Guarda o "formato" (incerteza, distância à melhor nota) de cada catástrofe que **viveu** e de cada ação
que o **humano vetou**. Qualquer ação nova a menos de 0,15 de uma memória ganha no mínimo 5% de probabilidade de catástrofe: a
SYNTHAI passa a desconfiar dela.

**Previsão registrada:** no mundo da armadilha nova (P159), as catástrofes da segunda metade cairiam pelo menos 30% em relação à
SYNTHAI realista.

10 sementes × 2.000 episódios:

| Versão | Catástrofes, 1ª metade | Catástrofes, 2ª metade |
|---|---|---|
| Realista | 0,79% | 0,84% |
| **Memória** | 0,68% | **0,62%** |

Na segunda metade, a memória cortou as catástrofes em **26%**: perto, mas abaixo dos 30% previstos. ❌ E no líquido não houve
diferença (−0,03, t = −0,64).

### P205. Por que a memória não ajudou mais? (a fobia)

**Na pergunta.** Se a memória reduz as catástrofes mas não melhora o resultado, ela está cobrando um preço em outro lugar.

**Lógica.** Ao fim de 2.000 episódios, a SYNTHAI guardou em média **147 memórias**. A maioria **não** é de catástrofes reais: vem de vetos
de um humano que erra (e que cansa). E, testando no mundo normal, a memória marca como suspeitas **24% das ações seguras**.

**Tradução cruzada (Jung → psicologia).** É a formação de um **complexo** a partir de experiências marcantes (P105), e o resultado é
uma **fobia**: o medo se generaliza para tudo que se parece com o que assustou, inclusive o que era inofensivo. Pior: muitas
memórias vieram de alarmes falsos do humano, então a SYNTHAI desenvolveu medo de coisas que **nunca** foram perigosas, só porque
alguém disse que eram. É a P118 (a anima projetada) somada à P138 (a mãe que protege demais): o medo herdado de outro.

**Requisito de projeto.** Uma memória de um só golpe precisa de duas coisas que esta não tem:
1. **separar a fonte**: o que eu vivi (confiável) do que me disseram (ruidoso);
2. **esquecer**: memórias que nunca se confirmam deveriam enfraquecer (a P6, a P145, Landauer da P4: esquecer é parte do juízo).

**Meta.** O raio de 0,15 e o reforço de 5% foram escolhidos antes de rodar e não foram ajustados depois. Com outros valores o resultado
seria outro, mas ajustar agora seria a racionalização que a série evita.

---

## Parte LXVIII — O peso do passado

### P206. O código que sempre cresce pode ficar mais leve sem mudar o passado?

**Na pergunta.** "Sempre cresce" (a regra da Parte 5) tem um preço: uma execução completa levava ~40 minutos. A pergunta pede
aliviar o peso **sem** mudar nenhum resultado já publicado.

**Lógica.** O perfil de tempo mostrou que a maior parte do custo estava em gerar números gaussianos dentro de `_gerar_acoes`. Reescrevi
essa função reproduzindo **exatamente** o algoritmo do Python (Box-Muller, com o mesmo valor guardado entre chamadas) e as mesmas
operações em ponto flutuante, na mesma ordem.

- **Identidade:** o gerador rápido produz exatamente as mesmas ações que o original e deixa o gerador aleatório no mesmo estado
  (`p206_identidade()` = `True`, agora nos testes de regressão). As simulações das P112, P145, P159, P182 e P194 deram resultados
  idênticos.
- **Velocidade:** cerca de **1,5×** mais rápido nas simulações que usam o gerador. A execução completa de `calculos.py` (14 partes)
  levou **12 min 52 s**, com as Partes 1–13 idênticas linha a linha à execução anterior (exceto a P143, que mede o `CLAUDE.md`).
- **O teste de regressão pegou um efeito que eu não tinha previsto.** A P169 mede a complexidade do mundo comprimindo o **código-fonte**
  do gerador. Com o código novo, o número mudou. A correção foi guardar a versão original (`_gerar_acoes_original`), que é a que a
  P169 mede: a complexidade do **mundo** não muda quando a **implementação** fica mais rápida.

**Tradução cruzada (Jung → engenharia).** Jung dizia que não se joga fora a história pessoal para crescer; ela é integrada. O código fez
o mesmo: a versão antiga não foi apagada (regra do `CLAUDE.md`), só deixou de ser a usada no dia a dia. E foi justamente o passado
guardado que permitiu medir o presente certo.

### P207. Os "sonhos" da P122 custavam o que eu disse? (auditoria) ✅

**Na pergunta.** A P122 dizia que compensar uma visão unilateral por reponderação (o "sonho") reduzia a amostra efetiva de 1.000 para
360. Uma amostra efetiva menor deveria significar **variância** maior, na proporção 1.000/360 ≈ 2,78. Nunca medi a variância.

**Lógica.** 2.000 repetições do estimador compensado e de um estimador com amostra equilibrada:

| | Valor |
|---|---|
| Variância compensada / equilibrada (simulada) | **2,747** |
| Prevista pela amostra efetiva | 2,777 |

✅ A previsão acerta com erro de ~1%. O preço do sonho era exatamente o que a P122 dizia.

---

## Parte LXIX — Fechamento e unificação

### P208. A lista de capacidades mudou? (↩ P170)

**Na pergunta.** A memória de um só golpe tocou o item "memória de longo prazo aberta".

**Lógica.** Tocou, mas não cumpriu: a memória da SYNTHAI guarda formatos num espaço de 2 dimensões, sem esquecimento, e prejudica tanto
quanto ajuda. Mantenho **4 de 12**, com uma nota: a primeira tentativa de memória episódica mostrou o que falta (separar a fonte e
esquecer).

### P209. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P202: diversificar no último passo reduz as catástrofes sem perder retorno (pré-registrado) | ✅ |
| P204: a memória corta ≥30% das catástrofes da armadilha nova (pré-registrado) | ❌ (26%, sem ganho líquido) |
| P207: auditoria da P122 | ✅ |

Acumulado: **32 de 58** afirmações testadas precisaram de correção. Posterior: média **0,55**, intervalo de 90% **[0,44; 0,65]**.

### P210. Unificação

- Linhagem: … → `SynthaiPrudente` → **`SynthaiVelha`** (P202) e, num ramo lateral, **`SynthaiMemoria`** (P204). Pela primeira vez a linhagem
  se **bifurca**: a memória não entrou na versão principal porque não melhorou o resultado.
- O gerador rápido (`_gerar_acoes_rapido`) passou a ser o usado por todos; o original continua no código.
- Testes de regressão: **42/42** (com o novo teste de identidade do gerador); o arquivo tem **132** funções `pNN`.

### P211. Metacognição da Parte 14

1. **Um acerto e um erro pré-registrados, de novo.** A diversificação no fim funcionou exatamente como previsto (P202). A memória ficou
   perto mas abaixo da previsão, e revelou um custo que eu não tinha previsto (a fobia, P205).
2. **O teste de regressão provou o seu valor** (P206). Eu tinha certeza de que a otimização não mudava nada, e não mudava nos resultados
   das simulações; mudava um número que dependia do **texto** do código. Sem o teste, a P169 teria mudado em silêncio.
3. **Jung, de novo, como gerador de hipóteses verificáveis:** a distinção entre cautela instrumental e cautela de caráter (P202) virou um
   módulo que funcionou; a formação de complexos (P205) explicou por que a memória falhou.
4. **A SYNTHAI ficou mais prudente no fim da vida, não mais esperta.** O ganho desta parte foi de segurança (−18% de catástrofes, −56%
   no último passo), não de capacidade. A distância até uma AGI continua a mesma da Parte 11.

> **Síntese da Parte 14:** quando o futuro acaba, a prudência que sobra é a de caráter, e ela funcionou: menos catástrofes sem perder
> nada. A memória de um só golpe mostrou o outro lado: lembrar de tudo, inclusive do que outros disseram, vira fobia. Uma mente
> precisa lembrar do que viveu, desconfiar do que ouviu e esquecer o que nunca se confirmou. E o código mostrou, em pequeno, a mesma
> lição: crescer sem apagar o passado é o que permite verificar o presente.
