# SYNTHAI — convenções do projeto

(O agente se chamava GISELE até a Parte 14; foi renomeado para SYNTHAI na Parte 15. O repositório
continua se chamando GISELE, e os nomes antigos das classes continuam no código como apelidos.)

Série de perguntas e respostas sobre como construir uma AGI/ASI, em português.

## Quando o usuário disser "Continue"
Repetir o processo inteiro: nova parte com novas perguntas mais fundas, respostas nas quatro
camadas, novos cálculos e simulações em `calculos.py`, auditoria de afirmações antigas,
evolução do agente `Synthai`, seção de unificação, `resultados.txt`, link a partir da parte
anterior, commit e push.

## Pedidos permanentes do usuário (gravados na memória)
- Cada parte começa listando as perguntas; depois as respostas; depois o código da parte (Parte 23).
- "Calcule sempre. Pesquise sempre. Muito!": pesquisar na web as fontes de cada resposta e citá-las no fim da
  parte; cada resposta tem cálculo (Parte 23).
- "Vá mais longe com os cálculos" (Parte 24): não parar no número simulado. Para cada resultado, derivar a
  conta que o explica (forma fechada, cota, ordem de grandeza ou expansão) e conferir a conta contra a
  simulação; quando possível, prever o número pela conta antes de simular.
- "Sempre rode contínuos e incansáveis testes e simulações" (Parte 25): enquanto uma simulação longa roda, preparar e
  rodar a próxima; cada resultado inesperado gera um teste novo (pré-registrado) em vez de uma explicação parada;
  os testes de unidade de todo o pacote rodam a cada mudança no código.
- "KD os cálculos?" (Parte 26): no texto, toda conta aparece com a substituição feita, linha por linha, a partir de
  quantidades medidas; e cada acerto vem com a chance de acertar ao acaso e contra um preditor ingênuo.
- MÁXIMO (Parte 29): fazer o maior número de cálculos e resolver o maior número de equações, com o maior número de
  linhas, de tokens, de testes e de simulações. Na prática: cada parte tem uma "bateria" de contas e equações resolvidas
  (cada uma conferida por simulação ou por outra conta), testes de unidade para cada peça nova, várias simulações
  pré-registradas (mundos e sementes novos) e cada número com a substituição feita. Volume vem de trabalho real, não
  de texto repetido.
- Também o máximo de PESOS (Parte 30): modelos com mais parâmetros aprendidos quando isso for testável (P353).
- O DICIONÁRIO como data lake (Parte 30): a cada "Continue", cálculos, equações, pesquisa técnica e métodos sobre o
  dicionário de inglês (WordNet, em `dados/`; e, desde a Parte 39, o português da OpenWordNet-PT, CC BY 4.0, alinhado a ele) — como manusear o dicionário para levar uma IA simples rumo a uma AGI/ASI.
  E, de forma SEPARADA, sobre HEXADECIMAL. Juntar os dois só quando for conveniente de verdade. Tudo no modo lógico
  criativo (pergunta) e criatividade lógica (resposta).
- DIÁLOGO PYTHON ↔ JAVA (permanente, desde a Parte 31): em TODA mensagem do usuário, reservar um tempo para a interação
  entre duas IAs: a IA-Python (apenas uma IA; lógica criativa; pergunta e ensina Python) e a IA-Java (no papel de ASI/AGI;
  criatividade lógica; responde e ensina Java). Ciclo infinito rumo a construir uma ASI/AGI. Cada rodada traduz um módulo
  real da SYNTHAI entre as linguagens, compila e roda os dois e confere os números (pasta `dialogo/`, registro em
  `dialogo/DIALOGO.md`). "ASI" é o papel da voz, não uma capacidade.
- AUTOPOIESE (Parte 31): usar só onde for útil (fechamento operacional do Core do dicionário; quanto dos próprios
  parâmetros a SYNTHAI produz). SUBSTITUIR ML/DL/aprendizado contínuo/por reforço por algo mais eficaz "se der":
  testar inferência bayesiana exata e teoria da decisão contra os métodos de aprendizado, com previsões registradas.
- METACOGNIÇÃO E ENGENHARIA REVERSA DE SI MESMA (Parte 41, permanente): sempre que gerar qualquer texto, pensar diferente e
  usar metacognição para fazer engenharia reversa do próprio texto e do próprio processo; produzir bastante texto para se
  conhecer; buscar padrões que se repetem E DAR SIGNIFICADO A ELES (o que cada padrão revela sobre como eu penso, onde
  erro e por quê). Na prática: cada parte mede os próprios textos e previsões (n-gramas
  repetidos, compressibilidade, semelhança entre partes, erros por tipo de previsão) com funções em `calculos.py`, e
  tem uma seção "Engenharia reversa" que diz que padrão se repetiu, o que ele significa e que regra nova ele pede.
  A PREMISSA É O SIGNIFICANTE E A RESPOSTA É O SIGNIFICADO (Parte 42): cada resposta é lida como o significado da sua
  premissa; medir quanto a resposta acrescenta à premissa (informação condicional) e quanto a premissa já continha.
  A RESPOSTA É A PERGUNTA E A PERGUNTA É A RESPOSTA (Parte 46): medir também o sentido inverso (quanto da pergunta a resposta
  já contém) e, de tempos em tempos, refazer tudo desde o começo (clone limpo, todas as partes numa execução, todos os
  testes e rodadas) para ver se funciona.
  Medido (Parte 46): cada resposta minha contém 58% da sua pergunta, e a pergunta só 5% da resposta; no diálogo, a pergunta
  de cada rodada é mais explicada pela rodada que a responde (0,41) do que pela que a gerou (0,28): a pergunta se define
  pelo que vem depois dela.
- SER PREDITIVO CONSIGO MESMO (Parte 53, permanente): antes de cada parte, prever o meu PRÓPRIO comportamento mensurável (quantos erros vou ter,
  o tamanho do texto, quantos testes vou escrever, quanto a resposta vai conter da pergunta, qual voz vai acertar, quantas previsões unilaterais), com
  faixa e centro deduzido do meu histórico (`p1031_historico_de_mim`), registrado antes de escrever a parte; no fim, pontuar contra o preditor
  ingênuo "igual à parte anterior" e manter o placar das previsões sobre mim separado do placar das previsões sobre o mundo.
  Medido (Parte 53): o preditor estatístico (média das últimas 8 partes ± 1,645 desvios) ficou em 4 de 6; eu, em 6 de 7. Partir do estatístico e só
  deslocar o centro por um mecanismo de sinal conferido (o meu "tabelas comprimem pior" tinha o sinal trocado). Uma previsão que mora dentro do objeto
  previsto muda o objeto (a tabela de autoavaliação tornou o texto mais compressível; a frase sobre o tamanho mudou o tamanho): medir também o
  documento sem a seção que o pontua, e nunca cortar texto para acertar. Conta à mão de um teste é conferida por uma linha de código antes.
  Parte 54: a previsão sobre mim funciona como auditoria (errou os testes de unidade e achou uma pNN nova sem teste). Exatidão de tradução depende da
  forma do algoritmo: escolher (grade, mínimo) absorve um ulp da libm; iterar (Gauss-Newton) o propaga.
  Parte 55: escolher absorve um erro só se a margem for maior que ele (um empate exato mudou com um ulp). Uma regra nova é uma intervenção em mim:
  desloca o centro da medida que ela afeta (cada pNN nova com o seu teste no mesmo commit; `p1092_pnn_sem_teste` audita). Antes de prever, perguntar
  pela condição de fundo (o ciclo que sustenta o funil, a amostra que gera os dados, a margem da escolha).
  Parte 56: a condição de fundo também é uma restrição (S16 − S10 é sempre múltipla de 3: com ela a conta previu o mundo novo com 0,2% de erro). Ao
  deslocar um centro por um mecanismo, dar faixa também à quantidade que entra nele. A medida de um texto que contém a própria medida pode não ter ponto
  fixo (oscilou em ciclo de dois): dar a medida da versão final e contar o caminho, sem escolher a versão favorável.
- O pressuposto do diálogo interno: as respostas (as equações) já existem; o trabalho é reconhecê-las e
  testar se as premissas delas valem no agente (Parte 23).

- CONTINUAR SEMPRE, MESMO SEM PEDIDO (Parte 44): ao terminar uma parte, começar a próxima; ao fim de cada turno, agendar a
  continuação automática nesta sessão (send_later), dizendo ao usuário como parar.

## Base teórica
- A partir da Parte 6, Carl Jung é a base psicológica: "calcular Jung" (cada conceito junguiano
  vira equação, simulação ou módulo da Synthai), dizendo onde a formalização funciona e onde quebra.

## Formato de cada nova parte
- Um novo arquivo `ASI_AGI_parteN_<tema>.md`, continuando a numeração das perguntas (Pn).
- Cada resposta tem quatro camadas:
  - **Na pergunta**: procurar na própria pergunta (palavras, pressupostos, inversões) a resposta
    ou o ponto de partida dela.
  - **Lógica**: equações e cálculos.
  - **Tradução cruzada**: psicologia/filosofia como matemática; física/química/biologia como
    psicologia/filosofia.
  - **Meta**: suposições, confiança, onde pode estar errado.
- Ir mais fundo que a parte anterior; indicar de qual pergunta anterior a nova nasceu (↩ Pn).
- Testar afirmações antigas e manter o placar de erros (✅ ⚠️ ❌).
- Previsões pré-registradas devem ser arriscadas: números que poderiam facilmente dar errado, não só a direção
  de um efeito já conhecido (Parte 17).
- Ligar a nova parte a partir da anterior.

## Código (sempre cresce, sempre unificado)
- `calculos.py` é um arquivo único que só cresce (só biblioteca padrão). Nunca apagar funções antigas.
- Todo número citado deve sair de uma função `pNN_...` em `calculos.py`.
- A classe `Synthai` é o agente unificado: cada parte acrescenta módulos a ela reusando as funções
  anteriores (sem copiar), citando a pergunta de origem.
- O bloco `__main__` termina sempre com a seção "Unificação": contagem de funções e
  `testes_de_regressao()`. Acrescentar aos testes os principais números de cada nova parte.
- Antes de publicar um agente, reler o código perguntando "o que este agente não poderia saber?" (Parte 7).
- Antes de construir um regulador/adaptador, verificar primeiro se o ponto ótimo realmente se desloca (Parte 8).
- Comparações entre versões: no mínimo 10 sementes pareadas, relatar a diferença média, o desvio e o t (Parte 9: a diferença entre duas execuções de uma semente tem desvio ~0,2).
- Funções cujo código-fonte é medido (P169) não são editadas: criar uma versão nova e guardar a original (Partes 14 e 16).
- Nenhum módulo é aprovado só pela métrica do próprio módulo (ex.: AUC); medir também o comportamento do agente (Parte 20).
- Efeitos pequenos (~0,5 com dispersão ~1) pedem ~30 sementes ou a combinação de várias estimativas (Parte 20).
- Antes de reusar uma conclusão de uma parte antiga, verificar se o mecanismo é o mesmo, não só o nome (Parte 12).
- Quando um módulo for redesenhado depois de ver o resultado, validar numa semente de controle extra e dizer isso.
- Simulações usam semente fixa; não trocar a semente nem ajustar parâmetros para obter um resultado mais bonito.
- `SYNTHAI_completo.py` é o projeto inteiro num arquivo só, gerado por `python3 gerar_arquivo_unico.py`: regenerar e
  commitar sempre que o código (ou este arquivo) mudar.
- Cada parte do `__main__` é uma função `_parte_N`; para desenvolver, `python3 calculos.py N` roda só a parte N
  (mais a unificação). Depois de mudar o código: `python3 calculos.py > resultados.txt` (todas as partes,
  leva vários minutos: rodar em segundo plano) e commitar os dois.
- Se a simulação discordar do texto, corrigir o texto e registrar a correção.
- Registrar as previsões antes de **qualquer** execução que mostre os números medidos, inclusive um teste de fumaça (Parte 22).
- Antes de trocar uma heurística por uma solução exata (um teorema), verificar se as premissas da solução valem no agente (Parte 23).
- Uma conta feita depois de ver o resultado (posterior) só vira evidência quando prevê um mundo ou sementes novas (Parte 25).
- A conta (decomposição dos termos) vem antes da previsão de comportamento, não depois (Parte 27).
- Um teste de unidade de uma fórmula usa um caso em que TODOS os termos são diferentes de zero (Parte 30: o teste
  com interação zero deixou passar um erro de sinal nas interações).
- O piso do caos (Parte 30): com desvio ~0,6 por semente no sequencial, o menor efeito visível é 2·0,6/√n
  (0,26 com 20 sementes, 0,165 com 60). Não prever diferenças abaixo do piso; replicar em lotes novos antes de concluir.
- Verificar a FORMA de uma estrutura antes de usá-la (Parte 31): Zipf supôs a cabeça, Spearman supôs variação nos postos,
  Hamming supôs efeitos aditivos, `profundidades` supôs taxonomia sem ciclo (o WordNet 3.0 tem um; estourou 13,9 GB).
- Uma conta de esperança não é cota por amostra (Parte 32): quando as unidades falham juntas (palavras definidas pela
  mesma palavra), a variância é muito maior que a de moedas independentes.
- Não esquecer e não se curar são a mesma propriedade (Parte 32): toda memória exata precisa de um teste de dano.
- Auto-melhoria (Parte 33): nunca executar código gerado; mutar um genoma. O avaliador fica FORA do alcance da mutação
  (selo SHA-256 conferido por outro processo/linguagem). Nunca aceitar um filho pela nota guardada do pai (maldição do
  vencedor: a regra "nota > nota guardada" piorou o agente real, 232,8 contra 159,9); reavaliar pai e filho juntos em
  sementes novas.
- Semântica exata nas traduções (Parte 34, rodada 5): o `sum()` do Python 3.12+ é compensado (Neumaier) e `x**2` (pow da
  libm) difere de `x*x` em ~0,08% dos casos; em código de comparação bit a bit, usar `x*x`.
- Bayes exato só é exato para o seu modelo (Parte 34): o Naive Bayes não esquece, mas perdeu para o SGD (78,9% contra 83,3%)
  porque supõe palavras independentes. Esquecimento catastrófico só aparece quando as tarefas conflitam.
- Em Python, importar é executar (Parte 36, rodada 7): scripts que outros importam guardam o corpo em main().
- Contar a unidade certa (Parte 35): checagens de janelas sobrepostas não são episódios independentes.
- Toda peça nova da SYNTHAI que decide alguma coisa passa por uma rodada do diálogo (Parte 38): a tradução bit a bit para
  Java é a prova de que o módulo é independente da linguagem (`python3 dialogo/verificar.py`).
- Uma cota de predição (perda logarítmica) não é uma cota de decisão (Parte 38): a mistura de modelos ficou a 1,1 nat do
  melhor modelo e decidiu pior que ele.
- Um axioma de implicação é meia definição (Parte 39): ∀x Sub(x) ⇒ Super(x) como perda só empurra Super para cima; sem
  o fechamento (ou rótulos negativos), Super vira 1 em tudo (especificidade 0,0 medida).
- Um arquivo de saída por execução, e conferir com `ps` depois de matar (Parte 40): duas execuções escrevendo no mesmo
  arquivo corromperam a Parte 35 do `resultados.txt`.
- Antes de criar um arquivo, conferir se o nome já existe (Parte 41: o módulo novo foi escrito por cima de
  `synthai/metacognicao.py`, da Parte 22); depois de qualquer mudança no pacote, rodar a suíte INTEIRA.
- Faixas de comportamento: instinto ×1,72 e o centro deduzido por conta de mecanismo (Partes 41-43: 14 de 14 dentro). Toda
  previsão tem largura (nada de "≥ x" traçado no olho: P732 errou por 0,003).
- Antes de prever sobre uma estrutura, perguntar em que NÍVEL cada coisa está (Parte 43): o nome de uma família não é um
  animal; uma mudança global não é a mudança de um braço; uma crença corrompida não é um mundo mudado.
- A direção do meu viés (Parte 45): os centros das previsões de comportamento ficam abaixo do medido (média de z +0,38),
  porque eu esqueço custos. Ao deduzir quanto tempo a evidência leva, calcular a KL entre as previsões das hipóteses no
  caso em questão (uma crença errada e modesta, perto da ignorância, quase não é desmentida).
- Nunca usar `pkill -f` com um padrão que apareça na própria linha de comando (mata o shell; aconteceu duas vezes).
- Execuções longas em blocos retomáveis (Parte 46): o contêiner reinicia e mata processos em segundo plano (a execução única das 45 partes morreu
  duas vezes). Um processo por bloco de partes, cada um no seu arquivo, com marca de concluído (`python3 calculos.py 15 16 17 18`).
- Antes de prever, calcular à mão um exemplo do caso presente (Parte 47): 5 de 6 erros vieram de responder à pergunta anterior (a rodada passada, um
  exemplo lembrado, a aparência do símbolo: supus que ler o hexadecimal em base 10 aumenta o número; diminui).
- Medida de si leva controle (Parte 48): toda conclusão sobre os meus próprios textos é refeita com outras partes no lugar (o "ciclo" da Parte 41 não
  passou no controle). Numa reprodução, separar antes as medidas que olham para o próprio projeto (P143, P213 mudam porque o projeto cresceu).
- Uma regra só vale quando vira um passo verificável (Parte 49: errei o que a regra da Parte 47 deveria impedir, meia hora depois de gravá-la). E as duas
  vozes do diálogo trocam de erro (Parte 50): antes de escrever a previsão de uma voz, reler os erros recentes da OUTRA.
- Previsão unilateral (≥, ≤, "pelo menos") só com justificativa escrita; `p974_previsoes_sem_largura` conta as unilaterais de cada parte (Parte 51:
  4 em 26, e a errada foi uma delas, por 1,9 ponto).
- Fronteira sem especificação (Parte 52): exp, log, pow, sin das bibliotecas diferem entre Python (glibc) e Java em ~0,1-0,3% dos argumentos (o IEEE 754
  só exige arredondamento correto para + − × ÷ √). Rodada que os usa: exp/log próprios (`dialogo/rodada26.py`) ou a chance de passar por sorte. Uma
  sequência de acertos não prova que o método é exato.
- Um texto que o usuário reenvia é comparado com a cópia guardada antes de ser auditado de novo (Parte 50: o texto pós-ASI voltou idêntico; a
  auditoria da Parte 33 se reproduziu sem executar nada).
- Mudar uma função desloca o ótimo das outras: ao trocar um módulo, rever os limiares calibrados com o módulo antigo
  (Parte 24: o pensamento exato com o limiar 2P* da P131 dobrou as catástrofes).

## O protótipo em módulos (`synthai/`, desde a Parte 22)
- A base é `synthai.Synthai`: um módulo por função de Jung (`percepcao`, `pensamento`, `intuicao`, `sentimento`,
  `relacao`), integrados pelo `agente`. Módulos novos entram no pacote; os experimentos continuam em `calculos.py` (`pNN_...`).
- O pacote reusa `calculos.py` (importa, não copia). Só biblioteca padrão.
- Os módulos do agente nunca leem atributos `_` de outros objetos (o escondido do mundo); `synthai/testes.py` verifica.
  Cada módulo novo ganha testes de unidade (`python3 -m unittest synthai.testes synthai.testes_reconhecimento
  synthai.testes_pensamento synthai.testes_limiar
  synthai.testes_autorregulacao synthai.testes_ancora synthai.testes_composta synthai.testes_hexadecimal
  synthai.testes_dicionario synthai.testes_parte31 synthai.testes_parte32 synthai.testes_parte33 synthai.testes_parte34 synthai.testes_parte35 synthai.testes_parte36 synthai.testes_parte37 synthai.testes_parte38 synthai.testes_parte39 synthai.testes_parte40 synthai.testes_parte41 synthai.testes_parte42 synthai.testes_parte43 synthai.testes_parte44 synthai.testes_parte45 synthai.testes_parte46 synthai.testes_parte47
  synthai.testes_parte48 synthai.testes_parte49 synthai.testes_parte50 synthai.testes_parte51 synthai.testes_parte52 synthai.testes_parte53 synthai.testes_parte54 synthai.testes_parte55 synthai.testes_parte56`); a suíte
  `synthai/testes.py` é medida pela P286, então testes novos vão em arquivos novos.
- Os seis módulos da Parte 22 são medidos pela P285: versões novas entram em arquivos novos (ex.: `reconhecimento.py`).
- Versões novas de agente devem preferir compor módulos a herdar de outras versões (Parte 28: a âncora herdou o
  pensamento de Newton que perde no bandido).
- Versão principal desde a Parte 29: `synthai.SynthaiComposta` (delegação: a `SynthaiExploradora` no bandido, a ancorada
  `SynthaiComAncora` fora dele). Antes (Partes 23–28): `synthai.SynthaiExploradora`.
