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
  dicionário de inglês (WordNet, em `dados/`) — como manusear o dicionário para levar uma IA simples rumo a uma AGI/ASI.
  E, de forma SEPARADA, sobre HEXADECIMAL. Juntar os dois só quando for conveniente de verdade. Tudo no modo lógico
  criativo (pergunta) e criatividade lógica (resposta).
- O pressuposto do diálogo interno: as respostas (as equações) já existem; o trabalho é reconhecê-las e
  testar se as premissas delas valem no agente (Parte 23).

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
  synthai.testes_dicionario`); a suíte
  `synthai/testes.py` é medida pela P286, então testes novos vão em arquivos novos.
- Os seis módulos da Parte 22 são medidos pela P285: versões novas entram em arquivos novos (ex.: `reconhecimento.py`).
- Versões novas de agente devem preferir compor módulos a herdar de outras versões (Parte 28: a âncora herdou o
  pensamento de Newton que perde no bandido).
- Versão principal desde a Parte 29: `synthai.SynthaiComposta` (delegação: a `SynthaiExploradora` no bandido, a ancorada
  `SynthaiComAncora` fora dele). Antes (Partes 23–28): `synthai.SynthaiExploradora`.
