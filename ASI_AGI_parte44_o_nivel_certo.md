# Como eu construiria uma AGI/ASI — Parte 44 (0x2C): o modelo no nível certo

> Continuação da [Parte 43](ASI_AGI_parte43_niveis.md). **Próxima:** [Parte 45 — a hipótese mais pesada](ASI_AGI_parte45_a_hipotese_mais_pesada.md) (P791–P820). A Parte 43 achou o padrão mais fundo dos meus erros, a **confusão de níveis**, e uma suspeita:
> o modelo de mudança da Parte 37 errava de nível, tratando a mudança de cada braço como um evento separado quando o mundo muda todos os braços juntos.
> Esta parte constrói o modelo no nível do **mundo** e mede o que ele ganha e o que ele cobra. O usuário pediu também que a série **continue sempre,
> mesmo sem pedido**; a regra entrou no `CLAUDE.md`.
>
> Novidades: `ThompsonBOCPDGlobal` ([`synthai/decisao.py`](synthai/decisao.py)); testes em [`synthai/testes_parte44.py`](synthai/testes_parte44.py); números
> de `p761_...` a `p763_...` em [`calculos.py`](calculos.py). **Centros e previsões no commit `5778937`, antes de rodar.**

---

## As perguntas desta parte

1. **P761 (0x2F9).** O modelo de mudança no nível do mundo decide melhor? ↩ P734
2. **P762 (0x2FA).** A minha taxa de erro cai ao longo das partes? (descritivo)
3. **P763 (0x2FB).** Quantos nomes do dicionário nomeiam grupos, e não coisas? ↩ P732
4. **P764 (0x2FC).** Engenharia reversa: o que salva um nível cobra no outro.
5. **P765 (0x2FD).** Jung: o todo e as partes.
6. **P766 (0x2FE).** O diálogo, rodada 15.
7. **P789 (0x315).** Placar. **P790 (0x316).** Unificação.

---

### P761 (0x2F9). O modelo no nível do mundo (pré-registrado) ✅❌❌

**Na pergunta.** "No nível certo" pressupõe que o nível errado tinha um custo. O BOCPD por braço (Parte 37) aplicava o risco H a cada braço: dez processos
de mudança independentes. O mundo do teste muda **os dez braços juntos** a cada 500 passos. O modelo novo tem uma só mistura de hipóteses, cada uma "o
mundo inteiro mudou há s passos", com as contagens de todos os braços desde então; a observação de um braço pesa a hipótese inteira.

**Lógica, os centros antes (p761_contas).**
- **Mundo que muda:** base 8 fases × 20 = 160; a parte da detecção da surpresa (367,7 − 160 = 207,7) cai à metade, porque o modelo global renova os dez
  braços de uma vez: 160 + 103,9 = **263,9**.
- **Estável:** a hipótese nova prevê ½ onde a velha prevê p* ≈ 0,9; o peso dela cai pelo fator 0,5/0,9 a cada puxada do melhor braço, e ela quase nunca é
  sorteada: 30,7 + 3 = **33,7**.
- **Dano:** o lixo é desmentido pelos braços que ele faz parecerem bons, e a hipótese nova renova todos: o custo cai ao nível da exposição, **19,5**.

| mundo | centro | faixa (×1,72) | **medido** | desvio | o melhor anterior |
|---|---|---|---|---|---|
| muda a cada 500 | 263,9 | [195,8; 331,9] | **231,5** | −12,3% | 340,7 (BOCPD 1/2000) |
| estável | 33,7 | [27,9; 39,5] | **44,7** | +32,6% | 30,7 (exato) |
| dano, custo | 19,5 | [12,8; 26,2] | **28,7** | +47,0% | 14,1 (γ 0,99) |

(a) ✅ (b) ❌ (c) ❌.

**O ganho.** No mundo que muda, o modelo no nível certo fez **231,5**, o melhor de todos os agentes da série: 32% menos que o melhor por braço (340,7) e 37%
menos que a surpresa (367,7). A confusão de níveis da Parte 43 custava, medida, um terço do arrependimento.

**O que errei nas contas (b) e (c).** Contei um mecanismo: a hipótese **nova** quase nunca é sorteada. O equilíbrio dela: entra H = 0,002 por passo e sai pelo
fator 0,556 por puxada do melhor braço, peso ≈ 0,002/(1 − 0,556) = **0,0045**: umas 9 vezes em 2000 passos, ~4 de custo, como eu tinha suposto. Mas a mistura
guarda **16** hipóteses, e as **jovens** (nascidas há 10, 50, 100 passos) têm poucas observações nos braços ruins; quando uma delas é sorteada, ela reexplora
**todos** os braços. Essas jovens não eram a "nova" e eu não as contei. É a regra das Partes 36 e 38 de novo: dois mecanismos, e eu contei um.

**A rodada de regras, até aqui:** previsões de comportamento com a regra das faixas: **15 de 17** (Partes 42–44). A regra corrige a largura; quando eu esqueço
um mecanismo, o centro erra e a faixa não salva.

### P762 (0x2FA). A minha taxa de erro cai? (descritivo)

Por parte, de 31 a 43: 0,333; 0,308; 0,125; 0,385; 0,200; 0,111; 0,286; 0,300; 0,091; 0,273; 0,222; 0,267; 0,182. Inclinação dos mínimos quadrados: **−0,006 por
parte** (0,6 ponto percentual). Em 13 partes, uma queda de ~8 pontos, pequena perto da dispersão entre partes (desvio ~0,09). A taxa de erro **por tipo** mudou
muito mais (comportamento: 22 em 66 antes das regras, 2 em 17 depois) do que a taxa total, porque a cada parte eu passo a prever coisas mais difíceis (o
erro migra para onde está a fronteira do que sei).

### P763 (0x2FB). Quantos nomes nomeiam grupos? (pré-registrado) ✅❌

Dos 82.115 substantivos: **10,2%** descendem de *group* (d) ✅ (em [0,025; 0,145]); **6,6%** descendem de *taxon* (e) ❌ (previ no máximo 3,7%). O WordNet tem
milhares de gêneros e famílias (*genus Canis*, *Canidae*, *Rosaceae*): o grupo taxonômico é **dois terços** de todos os grupos.

**O significado.** A confusão de níveis da P732 não era um acaso de 38 palavras: o dicionário tem **5.426** nomes de grupos taxonômicos (6,6% × 82.115), cada
um uma armadilha para quem supõe que o nome de uma família é o de um animal. A forma do dado que eu errei aqui é, de novo, uma questão de nível: eu imaginei
o dicionário como uma lista de coisas, e uma parte grande dele é uma lista de **classes de coisas**.

### P764 (0x2FC). Engenharia reversa: o que salva um nível cobra no outro

O modelo global salva o mundo que muda (231,5) **porque** renova tudo de uma vez, e cobra no mundo estável (44,7) e no dano (28,7) **pelo mesmo motivo**:
cada hipótese jovem sorteada renova tudo. Não existe um nível certo em geral; existe o nível certo **para o mundo em que se está**. É a tabela da P580 de
novo, agora com uma coluna a mais, e com a mesma conclusão: cada agente é uma suposição sobre o mundo.

O padrão que liga as Partes 37–44: **toda solução que eu construo para um mundo tem um custo exatamente simétrico no mundo oposto**: o exato (estável ×
dano), o desconto (dano × estável), a exposição (dano × muda), o BOCPD por braço (custo de exploração natural) e agora o global (muda × estável). Isso tem
um nome em teoria da decisão (não há almoço grátis), e em mim significa: eu ainda não construí o agente que **sabe em que mundo está e muda de nível**. A
mistura da Parte 38 tentou isso com os riscos; a próxima tentativa é com os níveis (a pergunta da Rodada 16).

### P765 (0x2FD). Jung: o todo e as partes

Jung via a psique como um todo que se regula (o Self), e as partes (complexos, funções) como subsistemas que podem agir sozinhos. O BOCPD por braço é a
psique como soma de partes; o global, a psique como todo. A P761 mede a diferença: quando o que muda é o todo (uma mudança de situação de vida), o modelo
do todo responde 38% melhor; quando nada muda, o modelo do todo se reorganiza à toa (44,7 contra 30,7). **Onde funciona:** a regulação no nível do todo é
mais rápida diante de mudanças globais. **Onde quebra:** o Self de Jung integra os dois níveis; aqui ainda há dois modelos e nenhum árbitro.

### P766 (0x2FE). O diálogo, rodada 15

O modelo global em Java: **112 números idênticos** (g) ✅; a hipótese mais pesada nasceu **exatamente** no passo da troca (600 observações) (f) ✅. Placar por voz
desde a Rodada 13: IA-Java 3 em 3, IA-Python 2 em 3.

### P789 (0x315). Placar

(a) ✅ (b) ❌ (c) ❌ (d) ✅ (e) ❌ (f) ✅ (g) ✅. Parte 44: 7 testes, 3 erros. Acumulado: **133 erros em 371 testes**; taxa média 0,36, intervalo 90% [0,32; 0,40].

### P790 (0x316). Unificação e metacognição

- **Novo:** `ThompsonBOCPDGlobal` (3 testes; 118 no pacote), o melhor agente da série no mundo que muda. Regressão: + P761 (263,85).
- **`resultados.txt`:** costurado até a Parte 41, com a Parte 35 corrigida (regressão 85/85).
- **Regra nova:** continuar sempre, mesmo sem pedido.

**Metacognição.** A Parte 43 previu que o erro estava no nível; a 44 confirmou (231,5) e mostrou o preço (44,7). O meu erro desta parte foi o mais comum da
série: contar um mecanismo onde há dois. A engenharia reversa dos meus erros já tem três padrões estáveis (dois mecanismos, forma do dado, nível), e os três
aparecem juntos aqui.

> **Síntese da Parte 44:** construído no nível do mundo (uma mistura de hipóteses sobre quando o mundo inteiro mudou), o modelo de mudança fez 231,5 no mundo
> que muda, o melhor da série, um terço a menos que o melhor modelo por braço: a confusão de níveis custava isso. O mesmo modelo cobrou no mundo estável
> (44,7) e no dano (28,7), porque as hipóteses jovens, que eu não contei, renovam tudo quando sorteadas. O dicionário tem 10,2% de nomes de grupos e 6,6% de
> grupos taxonômicos, muito mais do que eu supunha. E a minha taxa de erro total quase não cai (−0,6 ponto por parte), enquanto a por tipo muda muito: o
> erro migra para a fronteira do que eu sei.

---

**Fontes desta parte**
- Detecção bayesiana de mudança: [Adams e MacKay, arXiv 0710.3742](https://ar5iv.arxiv.org/html/0710.3742)
- A taxonomia do WordNet (group, taxon): conferida no próprio data lake (offsets 00031264 e 07992450)
- As contas de equilíbrio (entrada H, saída por fator de verossimilhança) e de detecção: derivação própria, conferida pela simulação
