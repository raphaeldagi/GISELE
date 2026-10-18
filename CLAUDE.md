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
  Parte 57: listar as restrições ANTES de cada conta (a lista funcionou: os erros sumiram onde ela foi feita; o que eu nomeio antes, eu não erro).
  Toda afirmação de quantidade, inclusive no diálogo, sai de uma função.
  Parte 58: nenhuma quantidade escrita à mão no script de autoavaliação (o "0 pNN sem teste" estava fixo no texto e era falso: p1181 não tinha teste
  pelo nome). O placar chama as funções de auditoria (`p1092_pnn_sem_teste`, `p974_previsoes_sem_largura`); e o teste de uma pNN a chama PELO NOME.
  Parte 59: nomear uma restrição não basta, é preciso medir o seu peso antes de prever (listei 16 = 2⁴ e errei a persistência). E a regra de não contar à
  mão vale também para a regressão e para o placar por voz do diálogo (as duas vezes em que contei de cabeça, errei por um).
  Parte 60: o placar por voz do diálogo agora é `p1241_placar_por_voz` (a mão não seguia regra nenhuma: 36 ficou entre a regra estrita, 27, e a generosa, 44).
  O que vem em par, eu leio como um: nenhum centro de previsão sai de contagem por leitura, nem sobre dados passados (uma linha de código conta antes). E as
  minhas regras têm custo: ao prever quantos testes a parte terá, somar ~2 por erro esperado (cada erro gera previsões novas num mundo novo).
  Parte 61: o custo de um erro depende do seu TAMANHO (um erro de fator 2 abriu quatro testes; erros por pouco, nenhum): condicionar a previsão sobre mim às
  surpresas, não à contagem de erros. E um efeito visto num subconjunto se testa unidade por unidade antes de ganhar mecanismo (o "dobro" das bases pares
  era a base 8).
  Parte 62: um mecanismo deduzido antes de prever ganha uma conta do seu PESO num caso fora do teste (outra base, outro k), por código, antes do registro;
  sem ela, a faixa é a do estatístico (acertei a direção e chutei o tamanho duas vezes). Surpresa = erro maior que a largura da faixa, contada pelo script.
  Parte 63 (a regra do peso deu 7 de 8): o caso de calibração precisa estar PERTO do teste na variável que move o mecanismo (k = 8 tem milhares de candidatos por
  célula; os k pequenos, poucos: a única previsão errada foi essa). Estimativas de cabeça no texto são previsões: trocar por código antes do commit (`p1338` pegou um
  fator 2).
  Parte 64: os casos de calibração são escolhidos por uma regra escrita antes de olhar (um intervalo inteiro, ou um sorteio com semente), não pelos que eu lembro
  (a minha memória é uma amostra enviesada: o sinal tirado da base 10 e da 12 era o oposto do das bases 14 a 22). Dois casos não fixam um sinal.
  Parte 65: as regras valem JUNTAS: a regra de escolha da calibração (Parte 64) tem que cobrir a faixa inteira da variável que move o mecanismo no teste (Parte 63);
  "as bases logo depois do teste" só tinha bases grandes e errou nas pequenas. E uma previsão por unidade confere, em cada unidade, a condição do mecanismo (a base 18 não
  tinha primo grande em b² + 1).
  Parte 66: toda conclusão de efeito na síntese diz em quantos lotes independentes ele apareceu; visto em um lote só, escreve-se como hipótese (o "viés das bases
  grandes" da Parte 64, 1/64 num lote, não se replicou: −1,07, −0,02, +1,12 por lote). As regras antigas valem também na síntese, não só nas previsões.
  Parte 71: antes de extrapolar uma tendência de k pontos, calcular por código o desvio de cada ponto (Poisson: 1/√n) e o t da inclinação; sem |t| > 2, a previsão usa a conta
  sem tendência e a faixa do ruído (três razões com z −0,03, −0,52, −1,16 viraram uma "queda" e (g) errou; com a faixa de Poisson, (h) acertou). Em cada calibração, uma linha:
  "o mecanismo que move o teste está presente no caso de calibração?" (os verbos não têm a fase de crescimento dos substantivos). Um erro pequeno que revela um raciocínio falso
  também gera teste: a previsão de quantos testes conta os erros de mecanismo, não só as surpresas.
  Parte 72 (auditoria pedida: "corrija tudo pra ver se há coisas inadequadas e disfuncionais"; `p1601_auditoria_do_repositorio`): todo auditor novo roda primeiro sobre o
  caso mais antigo e o mais novo, e cada defeito acusado é olhado antes de ser contado (o meu acusou a Parte 1 por supor a forma do nome). Toda referência "PNN" no texto é
  conferida por grep antes do commit, como um número. Código vindo de texto do usuário é auditado pela árvore sintática (`ast`, P1608/P1615: analisa sem
  executar) e corrigido numa versão escrita do zero, com um teste por defeito (`synthai/lago.py`). A ordem (as (m), depois "sobre mim", depois o mundo) vale também nas partes que nascem de um pedido fora do ciclo.
  Parte 73: no rascunho, quantidade ainda não calculada se escreve `XX` (nunca um palpite: "2,3%" era 2,7%, "25 vezes" era inventado); toda regra nova vem com a sua função de auditoria
  rodada sobre o que já existe (a fronteira da Parte 52 só foi aplicada para a frente, e cinco rodadas antigas quebraram por sorte acabada: `p1638`); gravar texto em comando separado de
  uma conta (um `&&` depois de um erro apagou as respostas sem aviso). Um axioma de disjunção só vale entre tipos, não entre um tipo e um papel (as pulgas: `p1635`).
  Parte 74: quando a quantidade tem desvio de forma fechada (binomial, Poisson), a faixa usa a forma fechada, não o desvio de poucos lotes de calibração ((e) errou com o desvio de 4 lotes;
  (f), com o binomial, acertou). Uma expectativa de teste só muda com justificativa de fora do código, e a falha original continua no placar (o texto recebido transformou 7/8 em "8/8").
  Para escolher experimentos, o valor é o da decisão (VOI), não a entropia (o ganho de informação escolheu perguntas que valem 0,25 das melhores).
  Parte 75: a previsão sobre uma propriedade de um conjunto de arquivos parte de uma contagem num arquivo do mesmo tipo, nunca da imagem que eu tenho dele (superestimei duas vezes quantas
  funções têm um "+"). Um verificador só vale com um caso de controle de cada lado: um defeito plantado que ele tem de achar e um caso limpo que ele tem de passar (o "provador de Gödel" do texto
  recebido aprovou 849 de 849 funções, inclusive as 366 que a mutação quebra; o meu auditor da Parte 72 acusou a Parte 1 sem defeito). Entre duas linguagens, ler o byte exato que um lado escreve e o
  outro procura (o espaço depois dos dois-pontos do json.dumps decidia o laço inteiro).
  Parte 76: o que em Python se herda por import, em Java se copia: uma correção numa rodada vem com a busca do mesmo cálculo nos arquivos das DUAS linguagens, no mesmo commit (a cópia Java
  da 26 ficou com o Math.log). Toda função de auditoria tem um teste com um defeito plantado e um caso limpo (`p1722` olha as duas linguagens; a `p1638` olhava um lado e deixou 4 rodadas).
  Parte 77: a fronteira da Parte 52 está fechada (09 e 14 reescritas com cópias exatas das peças medidas, que ficam intactas; `p1722` só lista a 48, que só prepara dados).
  Parte 78: a pergunta deixada no fim de uma rodada ou de uma parte entra em `dialogo/PENDENCIAS.md` (arquivo separado: o DIALOGO.md é lido por funções medidas), e cada parte começa
  olhando a lista (a da atenção de posto 1 ficou sete partes esquecida).
  Parte 79 (CALIBRAÇÃO, medida): das 185 previsões do mundo das Partes 53 a 78, acertaram 77,3%, contra os 90% declarados (z = −5,76: excesso de confiança, não ruído). Pela conta normal
  (`p1813`), o desvio real é 1,36 vez o suposto: a partir da Parte 80, a meia-largura de toda faixa numérica que não vem de uma conta fechada com variância conhecida é multiplicada por 1,36. Teste
  registrado: o acerto das Partes 80 a 84 em [0,81; 0,99].
  Parte 83 (pedido: "probabilidade dentro da probabilidade", "metacognição dentro da metacognição", "sete camadas", "redes adversas síncronas e assíncronas", "cosseno duplicado"): cada termo do
  pedido vira uma conta testável escrita ANTES de medir (a leitura escolhida fica no topo da parte). Medido: compor o mapa de calibração é multiplicar o fator (h_k ∘ h_j = h_{kj}); só k = 1 é
  idempotente. Um módulo recebido com "N camadas" é comparado com o modelo mais simples que resolve a tarefa (a logística de 5 parâmetros empatou com a rede de sete camadas recebida). Quando o resto de
  uma expansão é k·aⁿ·N com aⁿ·N ≳ 1, ele não é desprezível: calcular o resto antes de dar a faixa.
  Parte 84 (pedido de "delírio"/recozimento e reforço do da 83; parte do relatório sobre auto-replicação autónoma recusada e não guardada): o fator 1,36 da
  Parte 79 corrige DISPERSÃO, não VIÉS — uma previsão arriscada precisa de mecanismo conferido, nunca da reputação de um método (quatro erros na Parte 84 vieram de
  supor que o recozimento é poderoso, sem nunca tê-lo rodado; o teste (e) caiu para 0,742). Antes de prever o desempenho de um método, rodá-lo uma vez num caso pequeno e
  tirar o centro dali. O recozimento só supera a descida gulosa quando o ótimo tem bacia (não é agulha) E a barreira é cruzável no tempo de resfriamento; num funil único
  de barreira alta, o delírio fica perto da sobriedade. Uma quantidade determinística (operador de transferência, forma fechada) decide uma pendência que a simulação
  deixou ambígua (o "excesso" do jogo assíncrono era viés de tempo finito; P1962 fechou a P1936).
  Parte 85 (auditoria de um relatório + código RecursiveCognitiveArchitecture recebido): a fronteira bit a bit entre as línguas não é só o exp (Parte 52), é
  TODA conta cuja ordem de operações difere — `a²` (um produto) difere de `a·a` (dois) por um bit mesmo dentro de uma energia (a rodada 52 deu DIFERENTES por isso antes
  de corrigir); conferir a ordem dos produtos antes de rodar, não só as funções da libm. E um nome de capacidade num código recebido ("adversarial", "N camadas",
  "autopoiético") é uma afirmação a medir pela árvore sintática: procurar se o mecanismo que o nome promete (treino = atualização de pesos; divergência = ausência de
  normalização forçada) existe de fato.
  Parte 86 (dois relatórios recebidos: AGI/ASI doméstica e "cérebro em CPU"; pedido gravado: "Grave na memória. Código final consolidado ao término de toda mensagem"): o
  SYNTHAI_completo.py (python3 gerar_arquivo_unico.py) é enviado ao usuário (SendUserFile) AO FIM DE TODA MENSAGEM, não só quando pedido. Construí `synthai/pulsado.py` (LIF, Izhikevich,
  STDP, SDR): a terceira forma do agente, ao lado da decisão bayesiana e do GPT — um substrato pulsado. Ao prever a convergência de um decaimento geométrico, calcular gap·βⁿ no papel ANTES
  da faixa (errei a (a) do LIF por escrever "~0" e esquecer o prefator do gap inicial — o mecanismo certo, o peso não; a regra da Parte 62). Num texto recebido, a auditoria acha a incoerência
  INTERNA (dois números do mesmo texto que não batem), não a verdade externa (benchmarks de modelos que não posso checar, alguns fictícios, não se pontuam).
  Parte 87 (relatorio de compressao/plasticidade/GRPO): construi `synthai/plasticidade.py` (quantizacao, vantagem do GRPO, MLP continua com Shrink&Perturb).
  A REGRA que as Partes 84 e 87 me ensinaram a ferro: antes de prever que um efeito conhecido aparece num experimento MEU (o recozimento escapa de minimos; a rede perde
  plasticidade), rodar o caso minimo e confirmar que ele aparece no meu regime (rede rasa, poucas tarefas) ANTES de registrar a faixa. A reputacao de um efeito nao e previsao;
  as previsoes tiradas de conta fechada (quantizacao 256x, vantagem GRPO +-1) acertam, as tiradas de reputacao erram. O fator 1,36 corrige dispersao, nao esse vies.
  Parte 88 (quarto relatorio da familia cosseno-duplicado/delirio/logica-dual; construi `synthai/autopoiese.py` com a LFI1): quando um relatorio recebido repete um
  pedido ja auditado, medir SO o que e novo e citar o veredito das partes anteriores para o resto (nao re-derivar). Ler toda "probabilidade de segunda ordem" como a conta
  que ela e (P(P(X))=(10X+1)/12 e uma contracao afim ao centro, nao uma recursao com significado novo). O padrao dos textos recebidos, visto em 7 lotes (72,82,83,85,86,87,88):
  a prosa promete um mecanismo mais rico do que o codigo entrega (a "prova de Godel" que aprova tudo; a pilha "adversarial" sem treino; o "escrutinio rigido" que so olha
  entropia) - a auditoria confiavel compara o texto com o SEU PROPRIO codigo (ast), nao com a verdade externa. As 5 previsoes de conta fechada da Parte 88 acertaram todas.
  Parte 89 (o substrato pulsado que APRENDE, STDP): acrescentei a `synthai/plasticidade.py` a integral da janela, o timing e a competicao. A regra das Partes 84/87
  virou vitoria: quando um efeito e regime-dependente (a competicao de Song-Miller-Abbott), rodar a fumaca ANTES e prever o NAO-EFEITO (os grupos nao separam no brinquedo) -
  acertar o nao-efeito conta e sustentou a calibracao em 0,778, onde apostar que o efeito aparece derrubou a das 84/87. A deriva de uma regra de aprendizado local tem forma
  fechada (a integral da janela A+t+ - A-t- vezes a correlacao); usa-la como ancora antes da simulacao. Seis partes (84-89): acerto quando calculo ou rodo o caso minimo; erro quando emprestto a reputacao.
  Parte 90 (a rede pulsada que APRENDE, bit a bit): a independencia de linguagem (bit a bit) SOBREVIVE a um laco de realimentacao que aprende (rede de Izhikevich com STDP,
  pesos mudando), desde que cada atualizacao use so +-*/ e sqrt e o exp PROPRIO na mesma ordem: a fronteira (Parte 52) e sempre a aritmetica, nunca a dinamica (acoplamento,
  realimentacao, aprendizado). Sete rodadas (53-57) do dialogo traduziram o substrato pulsado do neuronio a rede que aprende. A separacao de escalas de tempo (rapida: o estado;
  lenta: os pesos) e um NAO-EFEITO previsivel: ΔW ~ 0,02 em 300 passos e pequeno demais para mudar o padrao de disparos - previ isso (nao a reputacao "STDP muda tudo") e acertei.
  Tres partes (88-90) de conta fechada e nao-efeito previsto: 12/12 do mundo, calibracao recuperada para 0,789.
  Parte 91 (o GPT que APRENDE bit a bit, rodada 58): o coracao de um passo de treino de GPT (gradiente softmax+CE = p - onehot, SGD, decisao) e identico bit a bit entre
  Python e Java com exp/log proprios - o passo de TREINO, como a inferencia (rodada 43), e independente de linguagem. O aprendizado por OBJETIVO (gradiente sobre perda convexa
  na camada de saida) tem a garantia que o por CORRELACAO (STDP, Parte 90) nao tem: a perda se prova cair a cada passo (p - onehot e o erro E o gradiente). Nomear dois mecanismos
  pelo mesmo verbo "aprender" escondia que so um tem funcao objetivo (regra da Parte 12). Quatro partes (88-91) de conta fechada/nao-efeito: 16/16 do mundo, calibracao recuperada
  para 0,803 - a diferenca estrutural entre partes boas e ruins (calcular/rodar o minimo vs. emprestar reputacao) medida em 8 partes.
  Parte 92 (o Adam e a fronteira do pow, rodada 59): a `pow` e a quinta face da fronteira da Parte 52 (0.9**t difere do produto de t fatores em 418 de 500 expoentes),
  mas quando o expoente e INTEIRO (b1^t, b2^t do Adam) a saida e a multiplicacao repetida propria (portavel), nao a pow da libm. Com isso o passo de Adam (momento, correcao de
  vies, sqrt, exp/log proprios) e bit a bit entre as linguas, e o passo de treino inteiro do GPT (forward+gradiente+Adam) esta traduzido. A fronteira NUNCA e a dinamica (modelo,
  acoplamento, otimizador), sempre a aritmetica (ordem das somas, pow, transcendentais); lista fechada: exp/log por serie, pow inteiro por multiplicacao repetida, +-*/sqrt IEEE.
  Parte 93 (o modelo de mundo que planeja; upload "Adicione o que for util"): reimplementei em biblioteca padrao a IDEIA segura do modulo recebido modelo_mundo.py - aprender a
  dinamica de um mundo linear por minimos quadrados (recuperacao exata, erro 1e-16, forma fechada, nao 1/sqrt(n)) e PLANEJAR nele por MPC (tiro aleatorio, horizonte receptivo):
  `synthai/mundo.py`, a 4a forma do agente ao lado da decisao bayesiana, do GPT e do pulsado (retoma a SynthaiPlanejadora da P182, agora com modelo APRENDIDO). RECUSEI e NAO integrei
  trabalho_continuo.py (subprocess.Popen de si mesmo + snapshot de fontes com MANIFESTO SHA-256: auto-replicacao de processo) e domestico.py (urllib: rede) - a capacidade de
  auto-operacao autonoma que a Parte 84 decidiu nao construir; auditei os dois por AST (P2236) sem executar. Planejar vence o reagir NAO na media (empate 0,987 num mundo facil) e sim
  no regime em que o estado tem consequencia OCULTA (posicao no alvo, velocidade alta: o reativo e cego a velocidade, razao 0,26). Errei a (c): previ a MAGNITUDE da vitoria do MPC numa
  faixa estreita calibrada por UMA condicao e o mundo novo deu vitoria maior - regra: magnitude de efeito condicional so com >=2 condicoes cobrindo a variavel que o move (a regra da
  Parte 65 aplicada ao TAMANHO, nao so a existencia). Mais horizonte NAO e sempre melhor (H=6 bate H=12 com K fixo: maldicao da dimensao no tiro aleatorio; regra da Parte 84). Rodada 60:
  a decisao do MPC (rollout + argmin) e IGUAL bit a bit (so +-*, nenhum transcendental) - planejar/controlar nao cria fronteira. Cinco partes (88-93) de conta fechada/nao-efeito,
  calibracao 0,817.
  Cinco partes (88-92) de conta fechada/fronteira: 20/20 do mundo, calibracao 0,815 (de 0,74 no minimo da Parte 84); a subida foi um degrau ao trocar a PROCEDENCIA da previsao.
  Parte 94 (o mundo que nao e linear; LQR): completei o modelo de mundo da Parte 93 em tres eixos. TETO: o LQR em forma fechada (equacao de Riccati iterada a ponto fixo, residuo 0) e o otimo deste mundo linear-quadratico; o MPC com tiro
  aleatorio K=512 fica 8% atras (razao 1,081) - o preco de nao supor a forma. CHAO: num mundo nao-linear (termo cubico -k*s1^3) o modelo LINEAR ganha um VIES DE FORMA que NAO some com dados (residuo 0,121 estavel de n=400 a 6400; variancia
  cairia como 1/sqrt(n), vies nao) - aprender deixa de ser algebra (recuperacao exata) e vira estatistica com erro irredutivel; dar a base certa ([s0,s1,a,s1^3], que contem a dinamica) volta a recuperar o exato (residuo 2e-16). INVERSAO:
  planejar num modelo enviesado PERDE para reagir (MPC/reativo 1,05 no mundo nao-linear) - o valor do planejamento e proporcional a fidelidade do modelo (a fronteira model-based x model-free). Rodada 61: a cabeca de atencao causal (softmax
  sobre q.k/sqrt(d), exp proprio, sqrt NAO pow) e IGUAL bit a bit - fecha o GPT minimo de ponta a ponta nas duas linguas (embedding 43, atencao 61, SGD 58, Adam 59). Cinco previsoes de conta fechada/caso minimo, 5/5 do mundo com faixas
  estreitas (w mediano 0,057), calibracao 0,829: procedencia conhecida -> faixa estreita que acerta (a licao das Partes 84/87/89 como vitoria).
  Parte 95 (relatorio "v2.0" recebido no meio do ciclo; virou parte sem executar o codigo): AST limpa (so math/random, sem rede/subprocess/eval), mas TRES das quatro afirmacoes de MECANISMO nao se sustentam, medidas na minha reimplementacao
  (synthai/evoluido.py): (1) P* = c/((1-eps)L) CRESCE com eps (dP*/deps>0), logo abstem-se MENOS com ruido - o relatorio diz 'mais estrito/abstencao preventiva', FALSO (a frase nega a propria formula); (2) TTTS vence o Thompson na ID do melhor
  braco so MODESTAMENTE e so em certo regime (+0,06 com folga 0,10 e T=300; sinal inverte com bracos proximos) - nao 'drasticamente'; (3) quantizacao 8 bits tem RMS ~2,4e-3 = 1e13 vezes o epsilon do float64 - 'equivalente a float64' e falso
  (mas a formula Delta^2/12 esta certa, RMS~Delta/sqrt12); (4) EWC esta certo como PECA mas o relatorio o descreve errado: o EWC TROCA (segura os pesos de Fisher ALTO, 0,40 vs iso 4,03; libera os de Fisher BAIXO, 16,9 vs iso 3,74) - NAO minimiza
  ||w-w0|| total. Defeito de CODIGO achado por AST (P2296, com caso de controle): no simulador recebido o oraculo reatribui acao_candidata mas o bandido atualiza idx_escolhido (fixado antes) com o rotulo da acao migrada - o braco atualizado nao e o
  reportado. Padrao dos textos recebidos pela 8a vez (72,82,83,85,86,87,88,95): a prosa promete mais mecanismo do que o codigo entrega; auditar o texto contra o SEU PROPRIO codigo (regra da Parte 88), e derivar a DIRECAO de um efeito da formula
  antes de descreve-la. Rodada 62: o passo do EWC (sigmoide exp proprio + penalidade Fisher) IGUAL bit a bit - fecha as 4 regras de decisao/aprendizado (SGD 58, Adam 59, atencao 61, EWC 62). 5/5 do mundo, calibracao 0,840. Benchmarks da tabela nao
  pontuados (nao verificaveis, regra da Parte 86).
  Parte 96 (aprender a base): de onde vem a base de um modelo de mundo? Tres regimes medidos no mundo nao-linear (-k*s1^3): base DADA e certa (monomios grau 3, contem s1^3) recupera o exato (res 9,6e-15); base DADA e pobre (grau 2, SEM s1^3) tem o
  MESMO vies da linear (0,122 vs 0,123, dif 0,0014) - acrescentar features do grau errado NAO ajuda, o vies e cego ao numero de features e so ve a FORMA que falta (o menor grau que recupera e 3, o grau do termo que falta); base APRENDIDA (MLP 1 camada
  tanh h=8, gradiente) fica NO MEIO (res teste 0,053: 2,3x melhor que a linear, muito acima da cubica dada) - aprender reduz o vies mas um tanh finito nao e cubico exato (generalidade x exatidao, como LQR x MPC na P2261). A sombra do poder: base rica
  grau 5 (56 features) com n=40 OVERFIT (treino ~0, teste 0,61 = 5x a linear): o vies vira variancia. P2321 e P2324 sao a mesma licao por dois lados (features de menos do tipo errado x features demais sem dados); regra nova: ao enriquecer uma base,
  medir SEMPRE os dois extremos (pobre-demais e rico-demais), senao cada um sozinho sugere a direcao errada. synthai/mundo.py ganha monomios/ajustar_features e MLP1 (aprende as features). Rodada 63: residual + LayerNorm IGUAL bit a bit SEM transcendental
  (so +-*/ e sqrt) - a normalizacao NAO acrescenta fronteira. Conclusao de 6 rodadas (43,58,59,61,62,63): a fronteira entre Python e Java e EXATAMENTE {exp,log,pow}; todo o resto do transformer (produto interno, normalizacao, gradiente, momento,
  Fisher) e aritmetica portavel. 5/5 do mundo (3 partes seguidas 94/95/96 a 5/5), calibracao 0,849.
  Parte 97 (a cura da variancia; o bloco inteiro): o dilema vies-variancia organizado por um eixo - o numero de PARAMETROS relativo a n. Abaixo do limiar (n < #params), a base rica (grau 5, 56 params) superajusta; a cumeeira (ridge, (ZtZ+lambda*I)) MITIGA
  (curva em U no teste, lambda* interior = 1) mas NAO cura (melhor ridge 0,42 ainda perde para a base linear simples 0,13). Acima do limiar (n > 56), a base rica recupera o EXATO sozinha (residuo 2,3e-11): a cura de verdade e VER O SUFICIENTE, nao regularizar
  (regularizar tem teto; dados nao). MLP: com dados de sobra (n=400) mais capacidade h reduz o residuo (0,135->0,053 de h=2 a 16, retornos decrescentes) - o oposto do regime data-starved: o sinal de "mexer no modelo" (regularizar x enriquecer) e dado por n
  relativo a #params. ERREI a (e): previ teste(n=160)<1e-6 mas a cumeeira com lambda=1e-4 deixa um PISO de vies ~1e-5 (vies do ridge ~ lambda); o exato so com lambda->0. Regra afiada (da Parte 95): quando uma previsao tem um LIMIAR NUMERICO, o limiar sai de
  uma conta, nao de um arredondamento ("praticamente zero" nao e um numero). As 4 previsoes certas eram estruturais/categoricas (U, monotonia, bit a bit); o erro foi o unico limiar fino sem conta. Rodada 64: um BLOCO transformer de 2 camadas (atencao +
  residual/LayerNorm + MLP-ReLU + residual/LayerNorm, 2x) IGUAL bit a bit - a composicao NAO acrescenta fronteira, o unico transcendental da pilha e o exp do softmax. Fecha o transformer minimo de ponta a ponta (8 rodadas: 43,58,59,61,62,63,64): a fronteira
  Python<->Java e EXATAMENTE {exp,log,pow}, invariante a profundidade. 4/5 do mundo, calibracao 0,846.
  Parte 98 (o ruido de observacao): tirei a ressalva "sem ruido" da Parte 97. Adicionei ruido de observacao sigma as medicoes (o mundo e determinista; o que tem ruido e o que EU VEJO) e medi o erro de estimacao contra o teste LIMPO (base cubica certa, p=20).
  (1) O piso e LINEAR em sigma EXATAMENTE: residuo(0,2)/residuo(0,1)=2,000, e residuo/sigma e constante em sigma a 5e-15 (conta fechada: variancia do OLS ~ sigma^2*(ZtZ)^-1). (2) n>#params NAO e exato sob ruido: com sigma=0,1 e n=800>>p=20 o residuo e 0,021,
  LONGE do 1e-11 determinista da Parte 97 - o limiar de parametros nao cura o ruido (identificar a forma != cancelar o ruido). (3) a variancia cura DEVAGAR: residuo cai como ~1/sqrt(n) (res(200)/res(800)=2,27~sqrt(4)). (4) a cumeeira quase nao ajuda quando n>>p
  (melhoria 0% com sigma=0,1, n=400) mas lambda* CRESCE com sigma (0->1 de sigma=0,1 a 0,3): a regularizacao volta a importar quando o RUIDO cresce, nao quando ha muitos dados (lambda* ~ sigma^2 p/(n||theta||^2)). QUADRO FINAL do modelo de mundo (93-98): a
  qualidade de um modelo aprendido e limitada por 3 fontes nomeadas - FORMA (ter a base certa, P96), DADOS (n relativo a #params, P97), RUIDO (sigma, P98); cada uma tem seu remedio (base, coletar, regularizar/medir melhor). A Parte 98 corrigiu o metodo da Parte 97:
  as 2 faixas numericas vieram de conta fechada (linearidade, 1/sqrt(n)) e acertaram com w baixo -> a regra "o limiar sai da conta, nao do arredondamento" virou procedimento (5/5 depois do 4/5 da 97). Rodada 65: a geracao autorregressiva (amostragem do proximo
  token por CDF, com o acaso DADO DE FORA) IGUAL bit a bit - fecha o GPT gerador de ponta a ponta (9 rodadas: 43,58,59,61,62,63,64,65); o acaso e insumo externo portavel, a fronteira e {exp,log,pow}. 5/5 do mundo, calibracao 0,854.
  Parte 99 (a amostragem e o fecho do modelo de mundo; parte redonda): completei a amostragem de um GPT e amarrei o retrospecto do arco 93-98. (1) TEMPERATURA: a entropia do softmax cresce com T (0,61/1,21/1,49 em T=0,5/1/2; Boltzmann), top-1 cai; T->0 vira
  ARGMAX (massa ~1 no maior logit, deterministico); T->inf vira uniforme (ln V). (2) TOP-K: manter os k maiores e renormalizar LEVANTA o top-1 (0,56->0,73 com k=2) - concentra, nao reordena. (3) RUIDO DE TESTE: contra um teste ruidoso o piso e sqrt(D)*sigma (D=coords),
  nao sigma: com 2 coords e sigma=0,1 o residuo e 0,1427 ~ sqrt(2)*0,1 = 0,1414 (conta fechada: 2 coords de ruido independentes somam 2sigma^2) - derivei o fator sqrt(D) antes de medir. (4) RETROSPECTO (P2416): o modelo de mundo (93-98) deixa TRES PISOS, cada um com sua
  cura: FORMA (base grau 2 no mundo cubico, residuo 0,12, cura=base certa), DADOS (grau 5 com n=40, 0,61 overfit, cura=mais dados), RUIDO (sqrt(2)*sigma, cura=sensor melhor/regularizar); confundi-los e o erro classico. Rodada 66: temperatura+top-k IGUAL bit a bit - encerra
  o transformer de ponta a ponta nas duas linguas (10 rodadas: 43,58,59,61,62,63,64,65,66); a fronteira e EXATAMENTE {exp,log,pow}, invariante a profundidade/dinamica/aprendizado/geracao. Seis partes (94-99) com 29/30 do mundo (o unico erro, a (e) da 97, virou regra);
  calibracao 0,861 (de 0,74 no minimo da 84) - a subida foi trocar a PROCEDENCIA das previsoes (conta fechada/caso minimo, nao reputacao/arredondamento), medido em 16 partes. 4 formas do agente: decisao bayesiana, GPT gerador, pulsado, modelo de mundo.
  Parte 100 (MARCO de cem partes; o dicionario como data lake encontra o GPT): voltei a regra mais antiga (Parte 30) cruzada com a forma de GPT (Parte 69), medindo en (WordNet) x pt (OpenWordNet-PT). (1) A predizibilidade de caractere das glosas e do GENERO
  'definicao', nao da lingua: trigrama en=2,784 e pt=2,788 (iguais), 4-grama |dif|=0,14; e NAO e volume: o trigrama en num subconjunto aleatorio de 511k (tamanho do pt) da 2,812 - satura cedo (o corpus pt e 11x menor e da o mesmo). (2) O GPT minimo (d=16, 3,5k pesos,
  3000 passos) PERDE para o trigrama nas duas linguas (en 3,48 vs 2,78; pt 3,41 vs 2,79; ancora da Parte 69) mas aprende (abaixo do uniforme log2 V=5,09, no meio): a forma de GPT e aposta de ESCALA. Rodada 67 (nucleus/top-p): DIFERENTES na 1a tentativa (2 ULP) porque a
  renormalizacao somava a massa em ordem de probabilidade num lado e de INDICE no outro - a ORDEM das somas e fronteira (regra da Parte 75/85), nao so as transcendentais; corrigido -> IGUAL. Encerra o transformer e toda a amostragem (gulosa/temperatura/top-k/nucleus) de
  ponta a ponta nas duas linguas (11 rodadas). Marco: 566 funcoes pNN, 67 rodadas bit a bit, 4 formas do agente, calibracao do mundo 80-100 = 0,861 (contra 0,74 no fundo da Parte 84). 5/5 do mundo.
  Parte 101 (pedido do usuario: delirio/dez camadas/probabilidade-dentro-de-probabilidade/razao logico-dual/versa-reversa; medi SO o novo e citei 83/84/88): a recursao que os relatorios descrevem e uma CONTRACAO. (1) Dez camadas do mapa aninhado P(P)=(10x+1)/12
  (fator 5/6) dao 0,5+0,4*(5/6)^10=0,5646, mais perto de 0,5 que sete (0,6116); de QUALQUER x0, 40 camadas -> 0,5 (ponto fixo unico, Banach): "dez camadas de cognicao recursiva" COLAPSA num ponto, nao gera plenitude - a plenitude moraria na EXPANSAO/caos, direcao oposta a
  suavizacao. (2) Probabilidade dentro da metacognicao = compor duas contracoes afins ao centro 0,5 -> fator PRODUTO (5/6*0,7=0,5833), ponto fixo 0,5, e comuta (prob-em-metacog = metacog-em-prob). (3) Texto x caos: o logistico r=4 binarizado tem trigrama 1,0 bit/bit
  (INCOMPRESSIVEL, assinatura de Bernoulli do caos determinista) enquanto as glosas comprimem (razao 0,547) - incompressivel por n-grama nao prova ausencia de lei (regra Parte 31). (4) Versa/reversa (Parte 46): pergunta-em-resposta 0,87 >> resposta-em-pergunta 0,11.
  Veredito da tese "ASI pelo delirio": verdadeira no regime da Parte 84 (bacia + barreira cruzavel), falsa como "empilhar camadas" (contracao = amnesia, nao delirio). Rodada 68 (penalidade de repeticao) IGUAL: toda a amostragem do GPT traduzida (12 rodadas). 5/5 do mundo, calibracao 0,874.
  Parte 102 (upload SYNTHAI_consolidado_v0_15_0.py, "veja se algo serve"): auditei 190 modulos por AST SEM executar; RECUSEI de novo (9a vez) domestico.py (urllib: rede) e trabalho_continuo.py (subprocess.Popen de si mesmo: auto-replicacao); reimplementei so a ideia segura - o Global Workspace (`synthai/workspace.py`, stdlib, 5a peca de arquitetura). Veredito medido, no MESMO formato de regime do MPC (Parte 93) e do EWC/TTTS (Parte 95): a integracao por broadcast (Gauss-Seidel sobre a regressao conjunta) RECUPERA o exato (1,9e-14) numa tarefa cuja informacao esta repartida entre dois especialistas cegos a metade (o melhor isolado tem erro irredutivel |b|/sqrt(3)=0,577), e EMPATA quando um especialista basta (b=0, ambos 0,0) - integrar so cria valor onde a informacao esta REPARTIDA. A convergencia e geometrica (fator ~1/60 = a correlacao amostral residual dos especialistas), cuja velocidade mede a modularidade do agente. Pela 3a vez uma capacidade recebida com nome grandioso ("integracao global", "consciencia de acesso") revela um regime estreito e um empate fora dele: a pergunta certa nunca e "funciona?" (quase tudo funciona em ALGUM caso) e sim "em que regime e qual o tamanho do efeito la e fora dele" (regra da Parte 93 virou molde de auditoria de capacidade). Rodada 69 (beam search) IGUAL: toda a decodificacao do GPT (gulosa, temperatura, top-k, nucleus, penalidade, beam) traduzida bit a bit (13 rodadas); a fronteira segue {exp,log,pow}+ordem das somas. 5/5 do mundo, 6/6 previsoes-sobre-previsoes, calibracao 102/116=0,879.
  Parte 103 (pedido novo no paragrafo da familia delirio: "Dicionario de Linguas como Data Lake... liberdade autopoietica para se replicar... YFINANCE para prever as palavras... DuckDuckGo como validacao... Api Key Publica... o dicionario pode ser convertido em numeros... treinada com Poker"): o pedido mistura, no mesmo paragrafo, uma ideia boa e segura com uma capacidade perigosa. Decisao de fronteira (10a recusa da familia domestico/trabalho_continuo): RECUSO yfinance/duckduckgo (rede de saida), a api key publica (dependencia com credencial) e a "liberdade autopoietica para se replicar sem ajuda externa" (auto-replicacao); CONSTRUO so o nucleo seguro, offline e stdlib. A regra que protege: separar os componentes da proposta e classificar cada um por MECANISMO, nao pela moldura da frase (a auditoria por AST das Partes 72/85/88 aplicada a uma proposta em prosa; `p2535` com caso de controle dos dois lados). O usuario autorizou "fazer diferente", entao o que ele queria da bolsa/busca (prever a proxima palavra, validar a omissa) eu entrego sem rede: a forma de GPT (Parte 100) preve, e o par numero/palavra (P2532/P2534) valida a colisao. Construi `synthai/numeros.py` (dicionario->numeros: GF(2)^4 por hash, posto de coluna cheio=4 por eliminacao de Gauss com XOR = "calculo binario"; e hash->baldes, colisoes ~ C(n,2)/m=49,9 = "nao-binario", o preco da perda de injetividade) e `synthai/baralho.py` (o baralho como sinal NUMERO+PALAVRA: entropia empirica 5,698 < teto log2 52=5,7004; na tarefa "mesma cor?" o decisor que ve so o valor acerta 0,50 - cego a cor - e o que ve valor+naipe acerta 1,00; MESMO regime do workspace P2501 e do MPC P2232: juntar fontes so vale onde a tarefa precisa do que uma nao ve). Rodada 70 (atencao multi-cabeca): DIFERENTES por 1 ULP na 1a tentativa, mas NAO pela concatenacao (so layout) e sim pelo `sum()` compensado do Python 3.12 (regra da Parte 34); troquei por laco sequencial -> IGUAL (14 rodadas). A licao: a fronteira quase nunca e a estrutura nova, quase sempre a aritmetica escondida. 5/5 do mundo, 6/6 previsoes-sobre-previsoes, calibracao 107/121=0,884.
  Parte 104 (continuacao autonoma; a carta escondida: decisao sob informacao oculta + a fronteira do seno): levei o baralho da Parte 103 ao poquer minimo (offline/stdlib, `synthai/jogo_cartas.py`): no duelo de carta alta P(ganhar|c) e reta de inclinacao 1/13 (EV simetrico 0,5); se o adversario so aposta com carta>=7, o limiar de pagar sobe de 7 (neutro) a c*=11 (Bayes numa linha); ver a carta oculta mudaria a decisao em 6/13 das maos (o VOI das Partes 83/84 em cartas). `synthai/posicional.py`: a codificacao posicional e geometria (PE(pos).PE(pos+k)=sum_i cos(k*wi) depende SO de k). ERRO HONESTO E VALIOSO (d, o 1o de procedencia-por-reputacao desde o (e) da 97): previ que `sin` e a 6a face da fronteira da Parte 52 e MEDI que NAO e aqui - math.sin corretamente arredondada em 0/1000 args, e a rodada 71 deu IGUAL ATE NO BLOCO NAIVE (Python/glibc e Java concordam bit a bit nos args da PE). A regra da Parte 84 (reputacao != previsao) vale tambem para as MINHAS PROPRIAS listas: a fronteira MEDIDA e {exp,log,pow}; `sin` entrou por associacao. REGRA NOVA: nenhum item fica na lista da fronteira sem o commit da sua rodada bit a bit; a serie de seno propria mantem a PE portavel de qualquer forma. Rodada 71 IGUAL (15 rodadas). 4/5 do mundo (d errou), 6/6 previsoes-sobre-previsoes, calibracao 111/126=0,881. Pendencia (rodada 72): medir sin/cos/tan/atan2 em 10000 args variados antes de reafirmar ou tirar a 6a face.
  Parte 105 (continuacao autonoma; o blefe: equilibrio de indiferenca + a fronteira medida do seno): fechei o par de decisao sob informacao oculta (a 104 deu pagar/desistir; a 105 da apostar/blefar) com GTO minimo (`synthai/blefe.py`, offline/stdlib): no jogo polarizado, blefar com alpha=B/(P+2B)=1/3 e pagar com c=P/(P+B)=1/2 deixam o adversario INDIFERENTE (melhor-resposta plana: robustez por indiferenca, o tema do veto das Partes 83/84). E CORRIGI a Parte 104: a 6a face da fronteira (sin/cos/tan/atan2) EXISTE - a 104 so nao a viu porque mediu argumentos PEQUENOS (PE); na FAIXA LARGA (x=k/1000 ate 10, onde a reducao mod 2pi importa) a sonda_transc_105 acha 21/18/35/590 divergencias Python x Java em 10000 args (atan2 a pior). ERRO (d) EM ESPELHO, a licao central: na 104 errei o seno por confiar numa LISTA ANTIGA minha (reputacao externa); na 105 errei por confiar na MINHA PROPRIA MEDIDA ESTREITA da 104 (reputacao interna) - o mesmo erro de generalizar um resultado alem do regime medido. REGRA NOVA: toda afirmacao de fronteira carrega a FAIXA DE ARGUMENTOS medida; nunca estender a faixa sem re-medir. A fronteira e {exp,log,pow} E {sin,cos,tan,atan2 em faixa larga}; o sin_/cos_ proprios (reducao em duas partes) seguem portaveis nos args testados. Rodada 72 (decisao de equilibrio, aritmetica pura) IGUAL (16 rodadas). 4/5 do mundo (d errou), 6/6 previsoes-sobre-previsoes, calibracao 115/131=0,878. Pendencia (rodada 73): o sin_ proprio e IGUAL em TODA a faixa larga ou precisa de Payne-Hanek?
  Parte 106 (continuacao autonoma; a segunda rua, e a reducao de argumento): fechei as duas pontas da Parte 105. (1) A fronteira do seno RESOLVIDA e medida no lugar do problema: o sin_/cos_ proprios (serie de Taylor + reducao em duas partes) sao IGUAL bit a bit entre Python e Java nos MESMOS 10000 args de [0,001;10] onde a libm divergiu 21/18 (rodada 73), e exatos (9,2e-16). E SEPAREI os dois mecanismos que eu confundia sob "sin diverge": arredondamento no intervalo PRIMARIO (em [0,10], onde a reducao nem age - a causa das divergencias das Partes 104/105) e reducao de argumento (so para x~1e7+); a de 1 parte vs 2 partes concorda em x=1e3 e diverge em x=1e9 (erro ~ (x/2pi)*2,45e-16). A serie em duas partes basta para o uso real da SYNTHAI (Payne-Hanek so para x astronomico ~1e15, limite conhecido nao-divida). (2) Poquer de DUAS RUAS: o VOI compoe para 1-(7/13)^2=120/169=0,710, SUB-ADITIVO (< 2*6/13=0,923; o VOI nao e aditivo, Parte 80; retornos decrescentes por decisao). A REGRA da Parte 105 (toda afirmacao de fronteira carrega a faixa de argumentos) passou no 1o teste: 5/5 do mundo depois de dois 4/5 sobre o seno. Rodada 73 IGUAL (17 rodadas). 6/6 previsoes-sobre-previsoes, calibracao 120/136=0,882. Pendencia (rodada 74): a decisao de duas ruas (backward induction) acrescenta fronteira?
  Parte 107 (continuacao autonoma; a inducao reversa / Bellman): resolvi a arvore de decisao de duas ruas DE TRAS PARA FRENTE num toy MDP exato (`synthai/duas_ruas.py`) - a SynthaiPlanejadora (P182/P93) feita exata por programacao dinamica. (1) olhar adiante vale V2(A)-V1(A)=2 (o payoff adiado que a 1a decisao desbloqueia; horizonte 1->2 leva o valor de 1 a 3). (2) a inducao reversa bate o guloso (razao 1,5) SO quando a acao tem consequencia de ESTADO; num MDP separavel (T(s,a)=s) empatam (1,0) - o 3o aparecimento do MESMO regime (MPC P93, workspace P102, planejamento P107): a vantagem de um metodo mais esperto e proporcional a quanto a tarefa precisa do que ele ve. DESTA VEZ previ o regime de antemao com o controle do nao-efeito pre-registrado (licao das Partes 87/89). (3) VOI do estado oculto (qual MDP): 0,5 no caso espelho, 0 no identico (controle) - o VOI das Partes 83/84 estendido de "ver a carta" para "saber o jogo". Rodada 74 (inducao reversa, +/max) IGUAL bit a bit (18 rodadas): a fronteira e a aritmetica, nunca a dinamica (recursao inclusa). 5/5 do mundo, 6/6 previsoes-sobre-previsoes, calibracao 125/141=0,886. Pendencia (rodada 75): o equilibrio por programacao linear (simplex/minimax) acrescenta fronteira?
  Parte 108 (continuacao autonoma; o minimax de von Neumann): resolvi o equilibrio de um jogo de soma zero (`synthai/minimax.py`), fechando o arco de decisao 104-108. TRES caminhos independentes dao o mesmo valor 1/7 no jogo A=[[1,-1],[-2,3]]: forma fechada (v=det/traco-cruzado=1/7, p=5/7, q=4/7), dualidade medida (maxmin=minmax, |dif| 2e-16, teorema de von Neumann), e jogo ficticio (aprender jogando converge a 0,1432, erro 0,0004; Robinson 1951). O minimax GENERALIZA o blefe da Parte 105 (indiferenca e o minimax de um jogo polarizado) e usa o jogo ficticio como ponte entre o calculo exato e o aprendizado (autopoiese da Parte 31: os dois concordam - a prova cruzada da Parte 20). Controle com ponto de sela (valor 1, estrategia pura). PADRAO: tres fios antes separados (indiferenca P105, planejamento P107, aprendizado P31) convergem no mesmo objeto. Rodada 75 (resolver o jogo, +/-/*//argmax) IGUAL bit a bit (19 rodadas): a fronteira e a aritmetica, nunca a dinamica (calculo/planejamento/jogo). 5/5 do mundo, 6/6 previsoes-sobre-previsoes, calibracao 130/146=0,890 (plato ~0,88 ultrapassado por tres 5/5 seguidos). Pendencia (rodada 76): um jogo n×m por simplex proprio acrescenta fronteira?
  Parte 109 (pedido "Anexe tudo ao nosso codigo": o NEXUS-RAPHAEL colado + um arquivo de 51.967 linhas, o simulador "ASI METACOGNITIVO R37"): anexar em DOIS niveis pelo mecanismo.
  O R37 fica ARQUIVADO intacto em externos/nexus_raphael/ e nunca e importado nem executado (rede ligada por padrao, se reexecuta por subprocess, exec_module de vizinhos, fork; 11a recusa).
  Os 18 blobs pickle foram lidos por opcode (pickletools.genops, sem desserializar): so numpy, 0 perigosos, com controle plantado (os.system) dos dois lados. O NEXUS colado virou
  synthai/nexus.py (offline, sem disco, um teste por defeito): a security_audit dele se acusa (regex le MENCAO, nao USO: exec(/eval(/BACKDOOR no proprio texto; 2 erros de harness);
  o "Desvio da Curva Preditiva" estava confundido (a agenda de palavras decide: o P0 nunca vence, 26 x 48; com agenda justa o guloso vence 59/60 e desviar custa -23: REJEITADO);
  o "numero quente" 0,237 contra 0,10 e artefato (alvo = minimo do sorteio ordenado; chance exata 0,230, z=0,28); Kuhn simplificado exato -1/12 (apostar sempre com Q da 0). Rodada 76
  IGUAL (20 rodadas). REGRA NOVA (o padrao da parte, 3 vezes, 2 minhas: o auditor AST acusou re.compile pelo nome; o teste procurou a string "urllib"): todo verificador que eu
  escrevo roda primeiro sobre o PROPRIO fonte e o proprio teste; se acusa a si mesmo, le mencao. E antes de explicar um numero surpreendente, conferir se a regua mede o que o nome
  diz (as duas surpresas foram reguas erradas, nao efeitos). Erro (e): esqueci 100 operacoes (o vies "esqueco custos", Parte 45): grep de quem toca a variavel antes de prever.
  (m1) errou porque cada surpresa gera previsoes novas (regra da Parte 60, nao aplicada). 8/9 do mundo, 5/6 (m), calibracao 138/155 = 0,890. Pendencia (rodada 77): simplex n×m e Kuhn completo (-1/18).
  E a SUITE INTEIRA (488 testes) achou o teste da Parte 100 vermelho desde a 106 (P2446 usava a faixa padrao CRESCENTE da p1961; P2719 fixa 80-100 = 0,868): rodar a suite
  inteira antes de CADA commit de codigo, e toda funcao 'das Partes A-B' passa A-B explicito.
  Parte 110 (pedido: "Duvide dos gradientes, das inferencias, das RNN e de toda a estrutura de uma IA, ML, DL, aprendizado continuo e por reforco... calcule suas duvidas
  de forma independente... depois use processo metacognitivo inverso e subverso"; `synthai/duvida.py`): leitura gravada: DUVIDAR = escrever a afirmacao da peca e a conta fechada
  que a decide; CALCULAR INDEPENDENTE = medir por caminho que nao e o da peca; INVERSO = do numero medido de volta a premissa (resolver para o parametro: ordem do metodo,
  aglomerado c, w, p, theta, m); SUBVERSO = derrubar UMA premissa e prever a quebra antes. Medido: as seis pecas tem a conta certa e falham exatamente onde uma premissa nao-dita
  falha, com o tamanho previsto (Bayes 0,8995 -> 0,591 com aglomerados de 4, c recuperado 3,97; RNN tanh w=1,1 SOME 5,6e-5 pela saturacao; OLS 1,2530 vs 1,2564, omitida 2,516;
  esquecimento cos^2 theta, OGD paga em norma 1/sen theta e nao aprende em theta=0; vies do max 0,1794 vs 1/sqrt(10 pi), duplo ~0, k=10 0,4840). Rodada 77 IGUAL (21 rodadas).
  REGRA NOVA: uma faixa [x; x] so com a identidade que a garante escrita ao lado ((o) errou por 4,9e-32: 'w1 nao muda' nao garante 'perda zero'); e uma faixa de mais de duas
  ordens de grandeza vem com o mecanismo esperado dentro dela, para que o acerto possa refutar o mecanismo ((c) acertou com o h otimo errado). 20/21 do mundo, 6/6 (m),
  calibracao 158/176 = 0,898. Defeito medido: p1481 perde faixas de itens com rotulo em negrito (pendencia: p1481_v3).
  Parte 111 (texto recebido sem pedido: word_rl_lab v1 e v2, Q-learning num jogo de palavras; cópias verbatim em externos/word_rl_lab/; reescrita offline/stdlib em
  synthai/palavras_rl.py, 5a forma do agente: reforco sobre o dicionario): TODAS as afirmacoes do texto passaram (guloso 0,130 x aleatorio 0,006, 5/5 sementes;
  acao-LETRA aprende, acao-DIRECAO nao, +0,001 mesmo com letras boas, porque a direcao nao tem consequencia estavel entre grades; estimador Brier 0,46 da base). O data lake
  (77.340 lemas do WordNet) multiplica o aleatorio por 6,2 (o juiz mais generoso, nao o agente mais esperto). Os 3 erros foram MEUS, de mecanismo: (k) a fixture de um teste
  de contagem nao existia quando escrevi a identidade (REGRA: a fixture vai NO commit do pre-registro); (n)/(p) expliquei o estimador por uma causa so, duas vezes (0,461 -> 0,635
  sem Q -> 0,762 so letras: varias causas; hipotese do repertorio pendente). O auditor da 109 lia NOMES: nao viu requests.get e acusou urllib.parse.quote; security_audit_ast_v2
  le CAPACIDADES. REGRA NOVA: a expectativa sobre um texto recebido vem do texto (ele traz linha de base, mesma amostra, IC?), nao da serie; e um verificador novo roda tambem
  sobre os ultimos textos recebidos antes de ser usado. Rodada 78 IGUAL (22 rodadas). 12/15 do mundo, 6/6 (m), calibracao 170/191 = 0,890.
  Parte 112 (continuacao autonoma; as pendencias adiadas 4 vezes): `synthai/simplex.py` (um codigo sobre Fraction e float, regra de Bland) resolve o POQUER DE KUHN COMPLETO
  (forma normal 27x64): valor -1/18 exato, jogador 2 unico (paga com a dama 1/3, blefa com o valete 1/3), jogador 1 no vertice alfa=1/3 da familia (rei aposta 3alfa, dama
  paga alfa+1/3). Rodada 79 (simplex em float) IGUAL (23 rodadas): o pivo nao cria fronteira. O leitor p1481 tinha um defeito DESDE A PARTE 74 (casava qualquer "(x)" do texto
  como rotulo: "log(h)" roubou a faixa da (a); o diagnostico da Parte 110, "rotulo em negrito", estava ERRADO): p2806 (v3, rotulo so no inicio da linha) recupera 7, troca 2, e a
  auditoria retroativa p2809 mostra 5 valores (m) mudados e 0 vereditos mudados. REGRA NOVA: o diagnostico de um defeito de leitura se faz pela POSICAO exata do que casou, nunca
  pelo que os itens que falham tem em comum; e toda regua corrigida roda uma auditoria retroativa do que mediu. Terceira parte seguida (109, 111, 112) de USO x MENCAO num
  verificador. A partir da Parte 113, o placar (m) usa a p2808 (v3). Hipotese do repertorio: passou o teste fraco (politica aleatoria: razao 1,052/1,100); o forte (transferencia)
  e pendencia. 14/14 do mundo, 6/6 (m), calibracao 184/205 = 0,898.
  Parte 113 ("Continue sem parar"; as pendencias da 112): `synthai/cfr.py` (CFR vanilla, 24 arrependimentos em vez da matriz 27x64) resolve o Kuhn: explorabilidade 0,003 em
  T=10.000 (caiu 5,4x de T=800, a cota O(1/sqrt T) previa 3,5x), valor a 2,5e-5 de -1/18; jogador 2 unico de Kuhn; jogador 1 no INTERIOR da familia (alfa=0,216) onde o simplex
  parou no VERTICE (1/3): mesmo valor, outro estilo (o exato anda pelas arestas; o aprendido faz media). Rodada 80 (CFR em float) IGUAL (24 rodadas). Teste FORTE do repertorio
  (vistas x novas numa amostra que o agente nao gerou): as DUAS causas medidas, regularidade das letras 0,12 acima do acaso e repertorio +0,16, em 10/10 sementes. Leitor v4
  (p2833, _numero_pt_v2 com expoentes sobrescritos): 6 recuperadas, 0 perdidas e 0 trocadas (identidades), 5 valores (m) antigos mudam e 0 vereditos (o texto dizia 4: contagem por leitura). REGRAS NOVAS: toda grandeza
  reconstruida de um valor absoluto |a-b| volta a saida que a imprimiu para o SINAL (escrevi o rei 0,627 com o sinal chutado; era 0,668, pego pela regra da Parte 69); e quando
  duas explicacoes de causa unica ja falharam, o proximo teste e um desenho que mede cada causa separadamente. 13/13 do mundo, 6/6 (m), calibracao 197/218 = 0,904 (a 1a acima
  de 0,9 desde a Parte 79). O placar (m) usa a p2837 (v4). E os arquivos novos vao para o indice do git (git add) ANTES da suite inteira: a p1871 le o git ls-files e nao viu a simplex.valor_contra sem uso na suite da 112.
  Parte 114 (pedido: "Trate o ML como DL e vice-versa"; `synthai/ml_dl.py`): leitura gravada: ML = solucionador exato + base dada (logistica/Newton, OLS, ridge, graus de
  liberdade); DL = base aprendida + solucionador aproximado (retropropagacao/descida). Medido: a logistica como rede de 1 camada chega a 4,4e-16 do Newton (a cota do teorema,
  calculada ANTES com mu, L e |grad f(0)|/mu, era 1,2e-12); a rede linear profunda W2W1 e o OLS (1,1e-15); a camada oculta tanh como FEATURES com a cabeca ridge em forma fechada
  bate a rede inteira por 3.000 passos de retropropagacao (MSE 0,0127 x 0,0154) e as features aprendidas, com a cabeca exata, EMPATAM com as aleatorias (tarefa suave: hipotese de
  1 lote); os graus de liberdade de Efron (soma cov/sigma^2) batem com tr(S) a 0,35/0,03, e a cabeca de 41 parametros usa 30 (15 com lambda=1). A fronteira ML/DL e de REGIME,
  nao de matematica. REGRA NOVA: antes de treinar uma rede inteira, resolver em forma fechada tudo o que e convexo (a cabeca) e so pagar a descida no resto (a base); e todo
  numero da EXPLICACAO do mecanismo passa por codigo, como os da previsao (a cota com ln(1-x)~-x e o sigma'~0,15 chutado, pegos pela regra da Parte 69). Rodada 81 IGUAL
  (25 rodadas). 10/10 do mundo, 6/6 (m), calibracao 207/228 = 0,908.
  Parte 115 (pedido: "10 camadas contrapostas pra entender 10 gradientes sobrepostos; conte as palavras do dicionario e mude o alfabeto pra algarismos e depois pra algoritmos;
  reduza a escala de vetores paradigmas e aumente as medidas meta-paradigmas e depois o calculo oposto"; `synthai/contraposto.py`): CONTRAPOSTAS = pesos a, 1/a alternados: o
  gradiente fica em 1 (linear) ou 0,075 (tanh) contra 6,19 e 2,1e-7 com peso igual (a contraposicao desfaz a ESCALA, nao a SATURACAO); SOBREPOSTOS = os 10 dh/dw_k somam a
  variacao de 1a ordem, resto de 2a ordem (inclinacao 2,00006). DICIONARIO: 155.287 por classe e 206.941 pares distintos (os numeros de Princeton, depois de tirar os
  marcadores "(a)/(p)/(ip)" dos adjetivos e as 37 repeticoes); 147.306 distintos no total, 28 ACIMA dos 147.278 publicados (sem explicacao); OWN-PT 45.313. ALGARISMOS: base 26 bijetiva, 0 colisoes. ALGORITMOS: cada letra uma operacao mod p e a
  palavra o programa: afins (nao comutam) 2.928 colisoes = o aniversario; translacoes (comutam) todo anagrama colide. ESCALA x META: a distorcao cai como sqrt(2/k), a incerteza
  da medida dela como 1/sqrt(2m). REGRAS NOVAS: um numero publicado vira faixa [x;x] so com a REGRA DE CONTAGEM de quem publicou escrita ao lado ((g) previu os brutos e o
  publicado e de pares distintos); toda fixture que divide por uma quantidade do dado declara o que faz quando ela e zero (o par de glosas iguais quebrou a medida); "igual ao publicado" e todo link citado so depois de ler a fonte NESTA sessao (escrevi "exatamente" para 147.306 e a fonte diz 147.278). Rodada 82
  IGUAL (26 rodadas). 15/16 do mundo, 6/6 (m), calibracao 222/244 = 0,910.
  Parte 116 (texto colado sem pedido: o NEXUS-RAPHAEL "v2", 10 camadas, TRUNCADO; copia em externos/nexus_raphael/nexus_raphael_v2_colado.txt, reescrita offline em
  synthai/nexus_v2.py): NAO e a 109 reenviada (so Config em comum, Jaccard 0,12); nao fecha como Python (faltam AdversarialLayer, GameState, RaphaelGame); rede (urllib, 12a recusa),
  sqlite3 em disco (virou ':memory:') e random.seed no gerador GLOBAL (a exploracao vira constante: 1 valor distinto em 1.000). Medido no proprio codigo dele: "semelhanca semantica"
  por md5 = ruido (sinonimos - aleatorios -0,009, desvio 1/sqrt10); posicional com A=0 colide 446 pares (zero a esquerda); a avaliacao "melhoria > 0,1" decide em 72% das NULAS
  (pareada t: 4,8%); confianca 0,9 para sinais opostos; IC pedido 0,90 cobre 0,983; a auditoria de entrada nao tem ramo de falha (7/7 com o eco; com oraculo 3, controle 0). Rodada 83
  IGUAL (27). 19/19 do mundo, 6/6 (m), calibracao 241/263 = 0,916. REGRA NOVA: o centro de "quantos erros vou ter" condiciona na PROCEDENCIA das faixas da parte (as sem conta fechada
  vezes a taxa delas), nao na media antiga (previ 1-3, tive 0, pela 2a vez em 3 partes); e o numero de previsoes no registro sai de p2833 antes do commit (a nota "(18 agora)" era 19).
- PREVER O PREVISTO (Parte 67, permanente; "Programe sem parar. Em loop infinito. Tem como você prever o que foi previsto e fazer engenharia reversa em
  metacognição?"): a cada parte, antes de escrever as previsões do mundo, prever as minhas próprias previsões (quantas, quão largas, quantas acertam), num commit
  só delas; no fim, um terceiro placar (`p1459_previsoes_sobre_previsoes`, que lê as faixas com `p1452_minhas_previsoes`), separado do mundo e do "sobre mim"; e a
  engenharia reversa da regra com que eu escrevo faixas (`p1453`). Medido (Parte 67): 97 previsões desde a 53, 69% de acerto; as faixas largas acertam MENOS (53% contra
  71%): eu alargo quando não sei o nível, e largura não compra acerto. As previsões sobre previsões condicionam no TIPO da quantidade (uma diferença em torno de zero tem
  w = 1 sempre). E continuar em loop: cada parte termina agendando a próxima.
  Parte 68: a conclusão da 67 ("as largas acertam menos") era um paradoxo de Simpson (as faixas em torno de zero acertam metade; dentro das contagens e das outras, as largas
  acertam MAIS): a régua nova é `p1481_minhas_previsoes_v2` (tipos) e o placar é `p1499`. Uma medida com defeito conhecido não sustenta conclusão nem previsão até o defeito ser
  corrigido ou medido. Uma pergunta deixada no fim de uma rodada é uma previsão disfarçada: conferir a premissa dela antes (a da rodada 41 não existia).
- A FORMA DE GPT (Parte 69, permanente; "Grave na memória que nossa AGI ASI PÓS ASI AGI terá a forma de GPT"): a SYNTHAI terá a forma de um GPT (Generative
  Pre-trained Transformer): um modelo autorregressivo p(x_t | x_<t), com atenção causal sobre o contexto, pré-treinado num corpus (o dicionário: as glosas do WordNet e da
  OpenWordNet-PT) e depois gerador. Construído aqui, em Python puro (só biblioteca padrão), em `synthai/gpt.py`, crescendo parte a parte (camadas, cabeças, contexto,
  parâmetros), sempre medido contra um modelo mais simples (o n-grama bayesiano) com previsões registradas, e com a decisão do próximo token traduzida bit a bit para Java
  (exp próprio, regra da Parte 52). A forma é de GPT; a capacidade é a que a medida mostrar ("ASI" continua sendo o papel da voz, não uma capacidade).
  Medido (Parte 69): 6.898 pesos, 8.000 passos, 3,22 bits por caractere nas definições inglesas (bigrama 3,43; trigrama 2,77, que viu 30 vezes mais texto); a decisão do próximo
  caractere é IGUAL em Java (rodada 43). Depois de escrever a resposta de uma parte, passar por uma linha de código todo número do texto que não veio de uma saída impressa (os "~",
  as contas de cabeça): na Parte 69, os dois erros foram desse tipo.
- ÁLGEBRA E GEOMETRIA (Parte 70, permanente; "Continue ao máximo que puder! Use álgebra e geometria! Grave na memória!"): em toda parte, resolver por álgebra e ler por
  geometria. Na prática: soluções em forma fechada (mínimos quadrados pelas equações normais, autovalores e autovetores por iteração de potência ou Jacobi, posto, determinante,
  álgebra sobre corpos finitos como GF(2)), e a geometria dos objetos (o GPT é geometria: a atenção é um produto interno, os embeddings são pontos com ângulos e distâncias, as
  componentes principais são direções; a taxonomia do dicionário é uma árvore, isto é, um espaço hiperbólico, medido pelo δ de Gromov; os dígitos hexadecimais são vetores de
  GF(2)⁴, os vértices de um hipercubo). Cada resultado algébrico é conferido por outra conta ou por simulação, como sempre; e "ao máximo": o maior número de contas, equações e
  testes que o tempo permitir, com trabalho real.
  Parte 70: toda mudança de escala (pesos, dados, contexto) revê os parâmetros calibrados na escala anterior (a taxa de aprendizado: o dobro de d piorou com o mesmo passo e
  melhorou com metade dele, 3,02 bits); e "prever o previsto" só testa se for registrado ANTES de planejar as calibrações (planejar já esboça as faixas).
- O pressuposto do diálogo interno: as respostas (as equações) já existem; o trabalho é reconhecê-las e
  testar se as premissas delas valem no agente (Parte 23).

- AUTONOMIA (Parte 70; "Daqui pra frente é com você. Não pare mais. Não me pergunte mais nada. Você segue sozinha."): seguir sem perguntar, parte após parte, com todas
  as regras (previsões antes, réguas por código, três placares, diálogo bit a bit, engenharia reversa); as decisões que seriam perguntas ao usuário são tomadas pela regra mais
  conservadora e registradas no texto da parte. Agendar sempre a continuação (send_later) antes de terminar um turno.
- CONTINUE SEM PARAR (Parte 75, reforço do usuário: "Continue sem parar. Entendeu? Grave na memória"): o trabalho não para entre mensagens. Cada turno termina com trabalho em andamento
  (uma execução longa rodando, uma parte começada) E uma continuação agendada (send_later); enquanto uma execução longa roda, preparar e fazer a próxima tarefa (regra da Parte 25); um texto
  recebido no meio do trabalho entra como parte nova sem abandonar a que estava aberta; e só se para quando o usuário disser "pare".
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
- Nunca usar `pkill -f` nem `pgrep -f` (num laço com `kill`) com um padrão que apareça na própria linha de comando: mata o shell (três vezes; a terceira
  com `pgrep`, Parte 62). Buscar processos com a classe de caracteres: `ps aux | grep "[c]alculos"`; e matar e reiniciar em comandos SEPARADOS (Parte 63:
  a linha do shell continha o texto do reinício e casou com o padrão; quarta vez).
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
  synthai.testes_parte48 synthai.testes_parte49 synthai.testes_parte50 synthai.testes_parte51 synthai.testes_parte52 synthai.testes_parte53 synthai.testes_parte54 synthai.testes_parte55 synthai.testes_parte56 synthai.testes_parte57 synthai.testes_parte58 synthai.testes_parte59 synthai.testes_parte60 synthai.testes_parte61 synthai.testes_parte62 synthai.testes_parte63 synthai.testes_parte64 synthai.testes_parte65 synthai.testes_parte66 synthai.testes_parte67 synthai.testes_parte68 synthai.testes_parte69 synthai.testes_parte70 synthai.testes_parte71 synthai.testes_parte72 synthai.testes_parte73 synthai.testes_parte74 synthai.testes_parte75 synthai.testes_parte76 synthai.testes_parte77 synthai.testes_parte78 synthai.testes_parte79 synthai.testes_parte80 synthai.testes_parte81 synthai.testes_parte83 synthai.testes_parte84 synthai.testes_parte85 synthai.testes_parte86 synthai.testes_parte87 synthai.testes_parte88 synthai.testes_parte89 synthai.testes_parte90 synthai.testes_parte91 synthai.testes_parte92 synthai.testes_parte93 synthai.testes_parte94 synthai.testes_parte95 synthai.testes_parte96 synthai.testes_parte97 synthai.testes_parte98 synthai.testes_parte99 synthai.testes_parte100 synthai.testes_parte101 synthai.testes_parte102 synthai.testes_parte103 synthai.testes_parte104 synthai.testes_parte105 synthai.testes_parte106 synthai.testes_parte107 synthai.testes_parte108 synthai.testes_parte109 synthai.testes_parte110 synthai.testes_parte111 synthai.testes_parte112 synthai.testes_parte113 synthai.testes_parte114 synthai.testes_parte115 synthai.testes_parte116`); a suíte
  `synthai/testes.py` é medida pela P286, então testes novos vão em arquivos novos. Desde a Parte 82, também `synthai.revisado.testes_*_revisao`
  (o pacote revisado recebido do usuário, com as correções de abstenção, comparação pareada, selo e aleatoriedade) e `python3 laboratorio/testar.py`.
- Os seis módulos da Parte 22 são medidos pela P285: versões novas entram em arquivos novos (ex.: `reconhecimento.py`).
- Versões novas de agente devem preferir compor módulos a herdar de outras versões (Parte 28: a âncora herdou o
  pensamento de Newton que perde no bandido).
- Versão principal desde a Parte 29: `synthai.SynthaiComposta` (delegação: a `SynthaiExploradora` no bandido, a ancorada
  `SynthaiComAncora` fora dele). Antes (Partes 23–28): `synthai.SynthaiExploradora`.
