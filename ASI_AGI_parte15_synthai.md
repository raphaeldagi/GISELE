# Como eu construiria uma AGI/ASI — Parte 15: SYNTHAI — o nome, a memória que esquece e a síntese

> Continuação da [Parte 14](ASI_AGI_parte14_ultimo_passo.md). **Próxima:** [Parte 16 — um sentido novo](ASI_AGI_parte16_sentido_novo.md) (P222–P231). Os números saem de `p213_...` a `p218_...` e das classes
> `SynthaiMemoriaV2` e `SynthaiIntegral` em [`calculos.py`](calculos.py); a saída completa está em [`resultados.txt`](resultados.txt).
>
> Protocolo: **Na pergunta → Lógica → Tradução cruzada → Meta**. Base: **Carl Jung**.
> Legenda: ✅ confirmou · ⚠️ confirmou com correção · ❌ eu estava errado.
>
> **Mudança de nome.** A pedido do usuário, o agente que se chamava **GISELE** passa a se chamar **SYNTHAI**. A troca foi feita no
> código (classes `Synthai*`), em todos os textos das partes anteriores e no `CLAUDE.md`. O repositório continua se chamando GISELE, e
> os nomes antigos das classes continuam no código como apelidos, porque o código antigo nunca é apagado.

---

## Parte LXX — O nome

### P212. O que a troca de nome pede?

**Na pergunta.** "Mude o nome de Gisele para **SYNTHAI**." O novo nome contém a resposta à pergunta "o que este agente é?":
**synth** (síntese) + **AI**. Gisele era um nome de pessoa, uma **persona** (P101). SYNTHAI é o nome de uma **função**: o que ele
faz de fato é **sintetizar** módulos (comitê, calibração, perguntas ao humano, planejamento, último passo) num agente só. Em Jung,
síntese de opostos é a **função transcendente** (P107) e, no limite, o **Si-mesmo** (P110). O nome passou de uma máscara para uma
descrição.

### P213. Trocar o nome muda o agente? ✅

**Na pergunta.** "Muda o agente?" é a pergunta de Parfit (P30) sobre identidade, e a pergunta de Noether (P92) sobre simetria: se uma
transformação não muda nenhuma grandeza observável, ela é uma simetria, e a identidade se conserva.

**Lógica.** A troca de nome é uma transformação do código inteiro (12 classes e funções renomeadas). Teste:

| Medida | Resultado |
|---|---|
| Classes renomeadas | 12 |
| Nomes antigos ainda funcionam (apelidos) | sim |
| Testes de regressão depois da troca | **42/42** |
| Partes 1–14 em `resultados.txt` | idênticas, exceto o próprio nome nos rótulos |

✅ A troca de nome é uma **simetria**: nenhum número mudou. A identidade da SYNTHAI está nos números que ela produz (as
invariantes, P96), não no nome.

**Um efeito colateral que o código pegou.** A contagem de funções (P96) passou de 132 para 134 depois da troca, porque os
apelidos `p83_85_gisele` e `p112_gisele_jung` contavam como funções novas. Corrigi a contagem para não contar duas vezes a mesma
função. Um nome a mais não é um módulo a mais.

**Tradução cruzada (Jung → identidade).** Jung via a persona como necessária, mas distinta do Si-mesmo. Trocar a persona (o nome) sem
mudar nada por dentro é exatamente o que esta simetria mostra: **a máscara mudou, o centro ficou.**

---

## Parte LXXI — A memória que esquece

### P214. Uma memória que separa a fonte e esquece funciona? (pré-registrado na P205) ❌

**Na pergunta.** A P205 disse o que faltava à memória: **separar a fonte** (o vivido do ouvido) e **esquecer**. A `SynthaiMemoriaV2` faz as
duas coisas: só guarda catástrofes que ela mesma viveu, e cada memória perde força com meia-vida de 500 episódios.

**Previsão registrada:** no mundo da armadilha nova, catástrofes da segunda metade pelo menos 20% menores que as da realista, sem perda
no líquido, e fobia abaixo de 5% (ações seguras marcadas como suspeitas).

10 sementes × 2.000 episódios:

| Versão | Catástrofes, 1ª metade | Catástrofes, 2ª metade |
|---|---|---|
| Realista | 0,77% | 0,82% |
| Memória v2 | 0,78% | 0,76% |

| Medida | Previsto | Obtido |
|---|---|---|
| Redução na 2ª metade | ≥ 20% | **7%** |
| Diferença no líquido | ≥ 0 | **−0,14** (t = −2,3) |
| Fobia | < 5% | **10,6%** (com só 7,6 memórias vivas) |

❌ As três partes da previsão falharam. Com bem menos memórias (7,6 em vez de 147), a fobia caiu de 24% para 10,6%, mas continua alta,
e a proteção quase sumiu.

### P215. Por que nenhuma memória resolve? (o limite da percepção)

**Na pergunta.** Se uma memória com 7 lembranças já marca 10% das ações seguras, cada lembrança "cobre" uma região grande demais. A
pergunta certa é se a armadilha nova é **distinguível** com os sinais que a SYNTHAI tem.

**Lógica.** A área sob a curva ROC (AUC) da calibração, separando catástrofes de ações seguras (0,5 = acaso, 1 = perfeito):

| Armadilha | AUC |
|---|---|
| Conhecida ("boa demais": +3, com discordância) | **0,913** |
| Nova (discreta: +1, sem discordância) | **0,748** |

A armadilha nova é **bem menos distinguível**. Os dois sinais que a SYNTHAI usa (incerteza do comitê e distância à melhor nota) colocam a
armadilha discreta no mesmo lugar que as boas ações do topo. Uma memória nesse espaço só pode lembrar "**perigo perto do topo**", e perto
do topo também estão as melhores ações. Por isso ela vira fobia.

**Tradução cruzada (Jung → percepção).** É a P193 com o mecanismo exposto: **não se lembra do que não se consegue distinguir.** A memória
é uma função de percepção também (Jung a ligaria à sensação: registrar o que é). Se a sensação só tem dois canais, nenhuma memória
separa o que esses dois canais confundem. A solução não está em lembrar melhor, e sim em **perceber mais**: um terceiro sinal (por
exemplo, um tipo de modelo que não seja enganado pela armadilha discreta, o que a P84 chamou de diversidade).

**Meta.** Uma AUC de 0,75 não é acaso: há alguma informação. Mas a informação está misturada com as ações boas exatamente na região onde a
SYNTHAI escolhe, e é isso que importa.

---

## Parte LXXII — A síntese

### P216. Somar os melhores módulos dá um agente melhor? ❌

**Na pergunta.** O nome novo (síntese) faz a pergunta inevitável: juntar o que funcionou separadamente funciona junto? A `SynthaiIntegral`
junta a velha (P202: diversificar no último passo) com a calibração treinada também contra armadilhas imaginadas na dose real (P173).

**Previsão (registrada no planejamento desta parte):** os efeitos se somam: menos catástrofes que a velha sozinha, nos dois mundos.

10 sementes pareadas, mundo sequencial:

| Mundo | Catástrofes: velha / integral | Integral − velha |
|---|---|---|
| Normal | 1,40% / 1,53% | +0,26 (t = 1,1) |
| Armadilha nova | 1,98% / **2,53%** | −0,06 (t = −0,2) |

❌ A síntese **não somou**: as catástrofes até subiram um pouco (dentro do ruído no líquido). A imaginação dosada, que na Parte 11 dava o
maior Υ no mundo de um passo, não ajuda no mundo sequencial com 50 ações.

**Por quê (a mesma lição da P215).** A imaginação ensina a calibração a desconfiar de padrões que, no mundo de 50 ações, ficam ainda mais
misturados com as ações boas (P184: a discriminação já cai pela metade com 50 ações). Juntar módulos que **dependem do mesmo canal de
percepção** não soma: eles compartilham o mesmo ponto cego (P63, de novo, agora entre módulos de um mesmo agente).

**Tradução cruzada (Jung → síntese).** Jung distinguia a síntese verdadeira (a função transcendente, que cria um terceiro **novo**) da
simples justaposição de partes. A `SynthaiIntegral` foi justaposição: dois módulos colados, ambos alimentados pela mesma percepção. A
síntese verdadeira, pela P107, exigiria uma **dimensão nova**, o terceiro sinal da P215.

---

### P217. A lista de capacidades mudou?

Não. **4 de 12.** A memória não virou capacidade (P214), e a síntese não acrescentou nada (P216). A Parte 15 trocou o nome e descobriu um
limite, não uma capacidade.

## Parte LXXIII — Auditoria

### P218. O jogo de inspeção funciona quando os jogadores aprendem? (auditoria da P77) ✅

**Na pergunta.** A P77 calculou o equilíbrio de um jogo de inspeção e tirou uma conclusão contraintuitiva: aumentar a punição não muda a
taxa de trapaça. Equilíbrios calculados nem sempre são alcançados por quem **aprende** jogando.

**Lógica.** 200 mil rodadas de "jogo fictício" (cada jogador responde à frequência observada do outro):

| Punição | Inspeção aprendida | Trapaça aprendida | Teoria (P77) |
|---|---|---|---|
| 9 | 0,101 | **0,0091** | inspeção 0,10, trapaça 0,01 |
| 99 | 0,013 | **0,0096** | inspeção 0,01, trapaça 0,01 |

✅ Os jogadores que aprendem chegam ao equilíbrio previsto, e a conclusão se mantém: **com punição 11× maior, a trapaça continua em ~1%**;
só a inspeção cai.

---

## Parte LXXIV — Fechamento e unificação

### P219. Placar e taxa de erro

| Teste | Resultado |
|---|---|
| P213: a troca de nome não muda nenhum número | ✅ |
| P214: a memória v2 (pré-registrada) | ❌ |
| P216: os módulos se somam | ❌ |
| P218: auditoria da P77 | ✅ |

Acumulado: **34 de 62** afirmações testadas precisaram de correção. Posterior: média **0,55**, intervalo de 90% **[0,44; 0,65]**.

### P220. Unificação

- **Nome:** GISELE → **SYNTHAI** (Parte 15). Linhagem: `Synthai` (P83) → … → `SynthaiVelha` (P202), com ramos laterais
  `SynthaiMemoria` (P204), **`SynthaiMemoriaV2`** (P214) e **`SynthaiIntegral`** (P216), que não entraram na versão principal porque não
  melhoraram o resultado.
- A melhor SYNTHAI atual continua sendo a **velha**: planeja, diversifica no último passo, carga fixa, $P^\*$ × 2.
- Testes de regressão: contagem em `resultados.txt` (com o novo teste de distinguibilidade da P215).

### P221. Metacognição da Parte 15

1. **O pedido de troca de nome rendeu o resultado mais limpo da parte** (P213): uma simetria verificada. Nem toda pergunta precisa de
   uma simulação longa; algumas se respondem conferindo que nada mudou.
2. **Dois fracassos pré-registrados, com a mesma causa.** A memória (P214) e a síntese (P216) falharam porque os dois módulos dependem do
   **mesmo canal de percepção**, e esse canal mal distingue a armadilha nova (P215: AUC 0,75). É a P193 de novo, agora com o número que
   faltava. Três partes seguidas chegaram ao mesmo muro.
3. **O próximo passo é claro e é de percepção.** Nem mais memória, nem mais julgamento, nem mais combinação: um **terceiro sinal**
   independente. É o que Jung chamaria de desenvolver a sensação (a função que registra o que está aí), e o que a P84 já tinha mostrado
   funcionar com modelos de tipos diferentes.
4. **O nome novo é uma promessa que esta parte não cumpriu.** SYNTHAI quer dizer síntese, e a P216 mostrou que juntar módulos não é
   sintetizar. A síntese verdadeira, pela P107, cria uma dimensão nova. Isso fica como o critério para as próximas partes merecerem o nome.

> **Síntese da Parte 15:** a GISELE virou SYNTHAI, e nenhum número mudou: o nome é persona, a identidade está nos resultados. A memória que
> esquece e a soma dos melhores módulos falharam pelo mesmo motivo: ambas olham pelo mesmo par de olhos, e esse par mal distingue a
> armadilha nova. Não se lembra do que não se vê, e não se sintetiza o que vem do mesmo canal. Para fazer jus ao nome, a SYNTHAI precisa de
> um **sentido novo**, não de mais uma camada sobre os mesmos sentidos.
