# Parte 154 — Os dois esquecimentos do campo médio, separados

↩ Nasce da Parte 153 (o campo médio erra de 4% a 8% para os dois lados) e da sua pendência 2: o erro tem DUAS fontes que a conta junta. Uma é a **memória das
letras**: uma vizinha já vista volta com a mesma letra. A outra é o **setdefault**: o jogo fica com a PRIMEIRA casa de cada letra, na ordem das vizinhas, e não com
uma casa qualquer daquela letra.

## O recolhimento do contêiner, 12º lote
Despertar às 08h39, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto. Doze lotes a favor.

## A separação
`aleatorio_exato(..., casa="uniforme")`: o mesmo enumerador da Parte 153, mas a casa escolhida é sorteada uniforme entre as casas livres da letra escolhida. Então:
- exato (primeira) / exato (uniforme) é o efeito do setdefault, sozinho;
- exato (uniforme) / campo médio é o efeito da memória das letras (o resto do campo médio).

O produto das duas razões é a razão total da Parte 153 (identidade).

**A regra da Parte 153, aplicada antes:** a conta com e sem o mecanismo, num caso de CALIBRAÇÃO diferente do teste (a mesma grade 3 × 3, mas de 3 a 4 letras em vez
de 3 a 5), nos quatro casos:

| caso (3 a 4 letras) | primeira | uniforme | campo médio | uniforme / primeira | uniforme / campo médio | primeira / campo médio |
|---|---|---|---|---|---|---|
| B | 0,338912 | 0,343204 | 0,326522 | 1,0127 | 1,0511 | 1,0379 |
| A' | 0,239770 | 0,251897 | 0,267445 | 1,0506 | 0,9419 | 0,8965 |
| C | 0,364834 | 0,368453 | 0,347127 | 1,0099 | 1,0614 | 1,0510 |
| D | 0,163340 | 0,168373 | 0,160912 | 1,0308 | 1,0464 | 1,0151 |

Os dois mecanismos existem nos quatro casos (nenhuma razão é 1). O setdefault sempre DIMINUI o acerto (uniforme > primeira): ficar sempre com a primeira casa puxa
o caminho para o mesmo lado da grade, e um caminho encostado na borda tem menos vizinhas. A memória das letras tem o sinal do caso.

## Previsões para o teste (3 a 5 letras), registradas antes de rodar
O centro é a razão uniforme / primeira da calibração (3 a 4 letras). A meia-largura vem de quanto a razão total primeira / campo médio mudou de 3-4 para 3-5 letras
nos quatro casos (já medida: +0,0050, +0,0191, +0,0058, +0,0165; raiz da média dos quadrados 0,0132), vezes 1,645 · 1,36 = **0,0295** (código no texto da parte,
e na P3213). Procedência: calibração por um caso vizinho (outro comprimento), sem conta fechada.
- **(a)** B, uniforme / primeira, em **[0,9832; 1,0422]**
- **(b)** A', uniforme / primeira, em **[1,0211; 1,0801]**
- **(c)** C, uniforme / primeira, em **[0,9804; 1,0394]**
- **(d)** D, uniforme / primeira, em **[1,0013; 1,0603]**
- **(e)** a identidade: (uniforme / primeira) · (primeira / campo médio) = uniforme / campo médio, nos 4 casos, a menos de 1e-12, em **[4; 4]** casos.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 5, m2 = 0, m3 = 0,0286, m5 = 0. E = 4 faixas de calibração × 0,25 + 1 identidade × 0 = 1,0; m1 em
[5; 5 + 2E] = [5; 7]. Acertos como contagem: 3 a 5 das 5 (3/5 = 0,6000).
- **(m1)** nº de previsões do mundo em **[5; 7]**
- **(m2)** nº que cruzam ou tocam o zero em **[0; 0]**
- **(m3)** mediana de w em **[0,020; 0,040]**
- **(m4)** fração de acertos em **[0,6000; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 0]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 3]**, centro 1,0.
