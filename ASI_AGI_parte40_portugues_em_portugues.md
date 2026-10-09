# Como eu construiria uma AGI/ASI — Parte 40 (0x28): quanto do português se define em português

> Continuação da [Parte 39](ASI_AGI_parte39_neurossimbolico_e_portugues.md). **Próxima:** [Parte 41 — engenharia reversa de mim mesma](ASI_AGI_parte41_engenharia_reversa_de_mim.md) (P671–P700). A Parte 39 pôs o português no data lake (OpenWordNet-PT) e a Rodada 10
> deixou a pergunta: **quanto do português se define em português?** Esta parte monta o grafo de definições em português, mede o fecho, testa a
> decisão que segue o modelo de maior peso (a pergunta da Rodada 9) e mede o custo dos acentos em UTF-8. Novidades: `DicionarioPT` e as regras de
> plural ([`synthai/dicionario.py`](synthai/dicionario.py)), `ThompsonMisturaMaximo` ([`synthai/decisao.py`](synthai/decisao.py)); testes em
> [`synthai/testes_parte40.py`](synthai/testes_parte40.py); números de `p641_...` a `p644_...` em [`calculos.py`](calculos.py). Diálogo, rodada 11.
>
> **Conta e previsões no commit `03ef661`, antes de rodar.** Uma correção, antes de qualquer número: a primeira execução da P641 parou num erro meu
> (o núcleo exige um grafo fechado; o português guarda palavras sem definição como possíveis âncoras); o grafo do núcleo foi fechado como o inglês.

---

## As perguntas desta parte

1. **P641 (0x281).** Quanto do português da OpenWordNet-PT tem definição em português, e quão circular ela é? ↩ P553
2. **P642 (0x282).** Quantas âncoras entendem o português definido? ↩ P381
3. **P643 (0x283).** Seguir o modelo de maior peso decide melhor que sortear? ↩ P541
4. **P644 (0x284).** Quanto os acentos custam em UTF-8? (trilha hexadecimal)
5. **P645 (0x285).** Jung: a língua materna e o núcleo.
6. **P646 (0x286).** O diálogo, rodada 11, e uma correção do `resultados.txt`.
7. **P669 (0x29D).** Placar. **P670 (0x29E).** Unificação.

---

### P641 (0x281). Quanto do português se define em português? (pré-registrado) ✅❌✅❌

**Na pergunta.** "Se define em português" pressupõe glosas em português. A OpenWordNet-PT foi feita traduzindo **lemas** do inglês; as glosas
vieram depois e em menor número.

**Lógica (medido).**
- Lemas de uma palavra só: **35.871**. Com glosa em português: **7.533**, uma fração de 7.533/35.871 = **0,210**. (a) em [0,10; 0,25] ✅.
- Palavras de conteúdo nas glosas: 54.057. As que são lemas, sem regras: **70,4%**; com as regras regulares de plural (-ões → -ão, -ais → -al,
  -ns → -m, -s → ∅…): **80,2%**. (b) em [0,40; 0,70] ❌ (0,704, 0,4 ponto acima); (c) as regras somam ≥ 3 pontos ✅ (+9,8).
- O núcleo (P371) do grafo português, fechado como o inglês: **2.255** palavras, **29,9%** das definidas; no inglês, **21,7%**. (d) português menor
  que inglês ❌.

**Por que o núcleo português é proporcionalmente maior.** O grafo português é o inglês com buracos: só 21% dos lemas têm glosa, e quem tem glosa
tende a ser frequente, que é justamente quem define os outros. As folhas (palavras raras, definidas e que não definem ninguém), que no inglês
diluem o núcleo, faltam no português. **Um dicionário parcial é mais circular que um completo.**

**Tradução cruzada.** Uma língua aprendida pela metade é feita sobretudo das palavras que explicam as outras: o miolo circular.

### P642 (0x282). Quantas âncoras entendem o português definido? (pré-registrado) ✅✅

Fecho a partir das k palavras mais usadas nas glosas portuguesas (a fração dos 7.533 lemas definidos):

| k | θ = 1 | θ = 0,6 |
|---|---|---|
| 100 | 3,8% | 11,3% |
| 300 | 8,2% | 39,3% |
| 1000 | **26,6%** | **79,4%** |

(e) θ 0,6 com 1000 ≥ 50% ✅; (f) θ 1 com 1000 < 30% ✅. **Contra o inglês** (P381): lá, 2000 palavras com θ = 0,8 alcançavam 99,6% e a transição
era abrupta (P385). Aqui a curva sobe devagar, sem avalanche: com só 21% das definições, falta a densidade de ligações que faz a cascata
atravessar o grafo (a percolação com limiar precisa de grau médio suficiente).

### P643 (0x283). Seguir o maior peso (pré-registrado) ✅✅❌

| mundo | mistura sorteada (P541) | **maior peso** | melhor anterior |
|---|---|---|---|
| estacionário | 56,3 | **34,5** | 30,7 (exato) |
| muda a cada 500 | 385,5 | **378,6** | 367,7 (surpresa) |
| dano, custo | 48,9 | **60,9** | 14,1 (γ 0,99) |

(g) estacionário ≤ 40 ✅; (h) que muda ≤ 385,5 ✅; (i) dano ≤ 48,9 ❌.

**A conta do (i), feita depois.** O modelo de maior peso só troca quando o log-peso de outro passa o dele. Depois de 1000 passos num mundo
estável, o modelo H = 0 está à frente do H = 1/100 por uma diferença Δ de log-peso; depois do dano, o H = 1/100 ganha, por passo, a diferença das
perdas, δ nats. A troca leva Δ/δ passos. Com Δ de dezenas de nats e δ de centésimos, são centenas de passos seguindo o modelo errado: o custo de
60,9. É a pergunta da Rodada 12, a conferir nas duas linguagens com os números.

**Tradução cruzada.** Quem sempre segue a teoria que mais acertou no passado leva tempo para abandoná-la quando o mundo muda; quem sorteia entre
teorias erra mais quando o mundo é estável. O mesmo dilema das Partes 35–38, agora no nível das teorias.

### P644 (0x284). O custo dos acentos em UTF-8 (pré-registrado) ✅

**Lógica, a conta antes.** Em UTF-8, um caractere ASCII ocupa 1 byte e uma letra acentuada do português (U+00C0–U+00FF) ocupa 2:
bytes/caractere = 1 + (fração de caracteres não ASCII) = 1 + 0,0296 = **1,0296**.

**Medido:** **1,03018** (inglês: 1,00000, todo ASCII). (j) a 0,001 da conta ✅ (0,00055). A diferença é de uns poucos caracteres de **3 bytes**
(aspas tipográficas e travessões, U+2000–U+206F). As letras mais comuns: `ã` = `c3a3` (2.857 vezes), `í` = `c3ad` (2.564), `ç` = `c3a7` (2.416),
`é` = `c3a9` (2.330), `á` = `c3a1` (1.472).

**Tradução cruzada.** O português paga 3% a mais por caractere para escrever o que o inglês não distingue. É um custo pequeno em bytes e grande
em significado (*avó* e *avô*).

### P645 (0x285). Jung: a língua materna e o núcleo

Para Jung, a linguagem herda imagens coletivas; cada língua as recorta de um jeito. A OpenWordNet-PT foi construída **sobre** a estrutura do
inglês (mesmos sinsets), então herda o recorte do inglês e traduz os nomes. A P641 mostra o efeito: o português do data lake é um núcleo circular
(29,9%) sem as folhas que dariam a ele um recorte próprio. **Funciona:** o alinhamento permite comparar as línguas conceito a conceito (P553).
**Quebra:** um conceito que só o português recorta (*saudade*) não tem sinset próprio; fica pendurado num sinset inglês aproximado.

### P646 (0x286). O diálogo, rodada 11, e uma correção

O fecho em português em Java: o mesmo conjunto de **2.963** palavras (k) ✅. As lições: `ã` = `c3a3` (a IA-Python ensinou o português em bytes);
`sorted()` e `String.compareTo` concordam no plano básico do Unicode e só nele (a IA-Java ensinou a ordenar).

**Correção do `resultados.txt`.** O commit "Partes 1–35" saiu com a Parte 35 corrompida: ao trocar a cadeia de costura, a antiga não foi parada de
fato, e **duas execuções escreveram no mesmo arquivo**. O arquivo foi cortado no fim da Parte 34 e as Partes 35–39 rodam de uma vez, numa execução
só; nova regra no `CLAUDE.md`: um arquivo de saída por execução, e conferir com `ps` depois de parar um processo.

### P669 (0x29D). Placar

(a) ✅ (b) ❌ (c) ✅ (d) ❌ (e) ✅ (f) ✅ (g) ✅ (h) ✅ (i) ❌ (j) ✅ (k) ✅. Parte 40: 11 testes, 3 erros. Acumulado: **122 erros em 329 testes**; taxa
média 0,37, intervalo 90% [0,33; 0,42].

### P670 (0x29E). Unificação e metacognição

- **Novos:** `DicionarioPT`, `ThompsonMisturaMaximo` (3 testes; 106 no pacote). Regressão: + P644 (1,0296).
- **Versão principal:** continua a `SynthaiComposta`. Para a decisão em mundos que podem mudar, o candidato é a mistura que segue o maior peso
  (34,5 no estável, 378,6 no que muda), com o defeito medido no dano.

**Metacognição.** Dois dos três erros desta parte erraram pelo lado da forma do dado: (b) por 0,4 ponto numa faixa que eu tracei sem medir a
riqueza morfológica do português; (d) porque supus que o português parcial teria a forma do inglês completo. A regra das Partes 31–34 continua a
valer: **verificar a forma da estrutura (aqui: parcial, com buracos onde estariam as folhas) antes de prever.**

> **Síntese da Parte 40:** na OpenWordNet-PT, 21% dos lemas têm definição em português; das palavras dessas definições, 80% são lemas com regras
> simples de plural. O grafo português é mais circular que o inglês (núcleo de 29,9% contra 21,7%), porque faltam as folhas, e não tem a avalanche
> do inglês: 1000 âncoras com 40% de tolerância entendem 79% do português definido. Seguir o modelo de maior peso, em vez de sortear, corrigiu a
> mistura no mundo estável (34,5 contra 56,3) e no que muda (378,6), e piorou o dano (60,9), porque o maior peso demora a virar. Os acentos custam
> 3% de bytes em UTF-8, como a conta dizia. E o português entrou também no diálogo: o fecho em Java deu as mesmas 2.963 palavras.

---

**Fontes desta parte**
- OpenWordNet-PT: [o repositório](https://github.com/own-pt/openWordnet-PT) (CC BY 4.0), [OpenWordNet-PT: a project report](https://aclanthology.org/W14-0153.pdf)
- Percolação com limiar e grau médio: [Baxter et al., arXiv 1003.5583](https://ar5iv.labs.arxiv.org/html/1003.5583)
- UTF-8: os tamanhos (1 byte para U+0000–U+007F, 2 para U+0080–U+07FF, 3 para U+0800–U+FFFF) são os da codificação, conferidos pelo `str.encode` do Python
- Plurais regulares do português: regras de gramática escolar, conferidas pelos testes de unidade (*cães* → *cão*, *animais* → *animal*)
