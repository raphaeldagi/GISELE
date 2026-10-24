# Parte 153 — O erro do campo médio, medido por enumeração exata

↩ Nasce da Parte 152 (a conta do colapso em campo médio prevê o braço aleatório em 15 casos com razão 1,009) e da sua pendência 1: o campo médio esquece que uma
vizinha livre já vista reaparece com a MESMA letra, e que o `setdefault` fica com a primeira casa de cada letra.

## O recolhimento do contêiner, 11º lote
Despertar às 07h15, depois de cerca de 55 minutos ociosa: "up 0 min", como previsto. Onze lotes a favor.

## O enumerador exato
`synthai/tabuleiro.py`, `aleatorio_exato`: numa grade pequena e com um alfabeto pequeno, soma sobre TODAS as atribuições de letras às casas (peso Π p) e, em
cada uma, sobre todos os caminhos com a regra real do `valid_actions` (vizinhas na ordem (−1, −1), …, (1, 1); uma ação por letra, com a primeira casa daquela
letra; PARAR com 3 letras ou mais; só PARAR com 5). Numa grade 3 × 3: 2⁹ = 512 atribuições com 2 letras, 3⁹ = 19.683 com 3.

**Os casos** (definidos antes de qualquer execução):
- **A**: letras {a, b} com p = (0,5; 0,5); dicionário = as palavras de 3 a 5 letras que começam com "a" e terminam com "b".
- **B**: letras {a, b, c} com p = (0,5; 0,3; 0,2); dicionário = as palavras de 3 a 5 letras sem duas letras iguais seguidas.
- **controle**: as letras de B e o dicionário com TODAS as palavras de 3 a 5 letras: as duas contas têm de dar a chance de o caminho chegar ao PARAR, que na
  grade 3 × 3 é 1 (toda casa tem vizinha livre até 5 letras); identidade.

## Previsões, registradas antes de qualquer execução do enumerador ou do campo médio nesses casos
**Procedência:** (a)-(c) mecanismo sem calibração (não há caso medido com alfabeto pequeno; regra da Parte 62: a faixa é larga e o centro é 1); (d) e (e)
identidade e binomial.
- **(a)** razão exato / campo médio no caso B em **[0,80; 1,20]**. O único caso perto, a grade 3 × 3 com 26 letras (Parte 152), deu medido / campo médio = 1,076,
  com ruído de 4,1%; com 3 letras as coincidências são muito mais frequentes e o erro deve ser maior. Faixa: ± 0,20, escrita sem código (é o "estatístico"
  sem dados da Parte 62; registro isso como o que é).
- **(b)** razão exato / campo médio no caso A em **[0,70; 1,30]**: com 2 letras, toda vizinha repete letra com chance 1/2.
- **(c)** |razão A − 1| − |razão B − 1| em **[0,00; 0,25]**: o erro cresce quando o alfabeto encolhe (mecanismo: as coincidências que o campo médio esquece).
- **(d)** o controle: exato e campo médio em **[1,0; 1,0]**, com tolerância 1e-12 (identidade: a soma das chances de parar é 1 e todo PARAR é palavra).
- **(e)** o enumerador contra a SIMULAÇÃO do jogo real (o `WordGridEnv` e o `run_episode` da Parte 111, caso B, 200.000 episódios): z = (simulado − exato)/σ em
  **[−1,645; 1,645]**, com σ = √(p(1 − p)/200.000) e p o exato (forma fechada binomial). É a prova de que o enumerador reproduz a regra do jogo, e não outra.

### Previsões sobre as previsões (m), registradas (régua: P2837)
A régua sobre o rascunho com "Do mundo:" provisória: m1 = 5, m2 = 2, m3 = 0,200, m5 = 0. E = 3 de mecanismo × 0,4 + 1 binomial × 0,10 = 1,3 (código: a própria
soma); m1 em [5; 5 + 2E] = [5; 7,6], arredondado para cima. Acertos como contagem: 2 a 5 das 5 (2/5 = 0,4000).
- **(m1)** nº de previsões do mundo em **[5; 8]**
- **(m2)** nº que cruzam ou tocam o zero em **[2; 3]**
- **(m3)** mediana de w em **[0,15; 0,30]**
- **(m4)** fração de acertos em **[0,4000; 1,0000]**
- **(m5)** nº com w > 0,6 em **[0; 1]**
- **(m6)** surpresas em **[0; 1]**

### Sobre mim, registrado
Erros no mundo em **[0; 4]**, centro 1,3.

## Um lote novo, registrado depois de ver (a)-(e) e antes de rodar os casos novos
O caso A deu 0,25 EXATO nas três contas (exato, campo médio, geometria): com duas letras meio a meio e um dicionário "começa com a, termina com b", a primeira
letra é "a" com chance 1/2 e a última escolhida é "b" com chance 1/2, com ou sem colapso, por simetria. O caso não podia medir o colapso; o erro de desenho é
meu (a regra da Parte 127: conferir a chave contra o conteúdo antes do registro). Casos novos, sem essa simetria:
- **A'**: letras {a, b} com p = (0,7; 0,3), o dicionário de A.
- **C**: letras {a, b, c} uniformes, o dicionário de B.
- **D**: letras {a, b} com p = (0,7; 0,3), as palavras de 3 a 5 letras que alternam (aba, bab, abab, …).

Procedência: mecanismo, sem calibração além do caso B (razão 1,043). Faixas largas, centro 1,04 (o caso B):
- **(f)** razão exato / campo médio em A' em **[0,85; 1,25]**
- **(g)** razão exato / campo médio em C em **[0,85; 1,25]**
- **(h)** razão exato / campo médio em D em **[0,85; 1,25]**
- **(i)** |razão A' − 1| − |razão B − 1| em **[0,00; 0,25]**: a hipótese de (c), agora num caso que pode testá-la.
