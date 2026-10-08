# SYNTHAI — convenções do projeto

(O agente se chamava GISELE até a Parte 14; foi renomeado para SYNTHAI na Parte 15. O repositório
continua se chamando GISELE, e os nomes antigos das classes continuam no código como apelidos.)

Série de perguntas e respostas sobre como construir uma AGI/ASI, em português.

## Quando o usuário disser "Continue"
Repetir o processo inteiro: nova parte com novas perguntas mais fundas, respostas nas quatro
camadas, novos cálculos e simulações em `calculos.py`, auditoria de afirmações antigas,
evolução do agente `Synthai`, seção de unificação, `resultados.txt`, link a partir da parte
anterior, commit e push.

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
- Cada parte do `__main__` é uma função `_parte_N`; para desenvolver, `python3 calculos.py N` roda só a parte N
  (mais a unificação). Depois de mudar o código: `python3 calculos.py > resultados.txt` (todas as partes,
  leva vários minutos: rodar em segundo plano) e commitar os dois.
- Se a simulação discordar do texto, corrigir o texto e registrar a correção.
- Registrar as previsões antes de **qualquer** execução que mostre os números medidos, inclusive um teste de fumaça (Parte 22).

## O protótipo em módulos (`synthai/`, desde a Parte 22)
- A versão principal é `synthai.Synthai`: um módulo por função de Jung (`percepcao`, `pensamento`, `intuicao`, `sentimento`,
  `relacao`), integrados pelo `agente`. Módulos novos entram no pacote; os experimentos continuam em `calculos.py` (`pNN_...`).
- O pacote reusa `calculos.py` (importa, não copia). Só biblioteca padrão.
- Os módulos do agente nunca leem atributos `_` de outros objetos (o escondido do mundo); `synthai/testes.py` verifica.
  Cada módulo novo ganha testes de unidade em `synthai/testes.py` (`python3 -m unittest synthai.testes`).
