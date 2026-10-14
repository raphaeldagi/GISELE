# Sete camadas e dez níveis recursivos

A arquitetura executável aplica uma interpretação operacional dos termos solicitados. Não assume que auto-observação ou recursão produzam consciência, AGI ou ASI.

| Camada operacional | Mecanismo |
|---|---|
| 1. Axiomas | Objetivos e orçamentos fixos, com configuração validada |
| 2. Geometria | Vetores normalizados, referência recursiva e cosseno de ângulo duplo |
| 3. Diálogo | Alternância entre lógica criativa e criatividade lógica; pergunta de melhoria e pergunta de refutação |
| 4. Aprendizagem | Rede com sete mapas afins: entrada, cinco blocos residuais tanh e saída binária |
| 5. Adversário | Treino adversarial e ataque PGD, com orçamento de norma infinito e pior caso encontrado por amostra |
| 6. Metacognição | Avaliação da previsão e da recomendação; probabilidades condicionadas e revisão recursiva |
| 7. Integração | Snapshots versionados, seleção operacional e confirmação reservada |

## Geometria e gradientes

Para r e x não nulos, c=(x·r)/(||x||||r||). O sistema preserva x, c e cos(2θ)=2c²−1. Preservar c evita perder orientação ao incluir uma transformação com simetria antipodal. O gradiente de c em relação a x é r/(||x||||r||)−c x/||x||²; o do cosseno duplicado é 4c vezes esse gradiente. Na origem ou com referência nula, o código define c=0 como convenção e não afirma que exista ângulo.

A referência evolui por r_(t+1)=normalizar((1−η)normalizar(r_t)+η normalizar(m_t)), com m_t obtido apenas dos dados de treino. Cada artefato inclui a própria referência. A candidata não altera a geometria da versão anterior; a avaliação compara seus snapshots sobre os mesmos casos originais, com ataques próprios de cada modelo.

Isso utiliza álgebra vetorial euclidiana e uma identidade algébrica trigonométrica. Não implementa a área matemática inteira denominada geometria algébrica.

## Dez níveis dentro da metacognição

1. Inferência de evento pela rede.
2. Probabilidade de acerto condicionada à faixa de confiança.
3. Erro da previsão e da confiabilidade prevista.
4. Frequência suavizada de recomendações úteis.
5. Dissonância operacional entre acerto nominal e adversarial.
6. Julgamento metacognitivo da recomendação anterior.
7. Mistura de confiança revisada na previsão de acerto.
8. Dilema entre ganho adversarial e regressão nominal.
9. Auditoria das premissas e do orçamento.
10. Observação integrada do próprio registro.

Cada nível recebe o registro anterior, verifica recursivamente a finitude das medidas, o domínio das probabilidades e a ordem de dependências, e produz um juízo metacognitivo com hash da entrada. Dez níveis não produzem dez rótulos externos: a evidência do ciclo é contada uma vez. A ordem de auditoria alterna versa/reversa sem inverter as dependências matemáticas.

“Metacognição dentro da probabilidade” significa usar a confiança estimada no controlador para formar uma mistura explícita da probabilidade de acerto calibrada e uma referência 0,5. “Probabilidade dentro da metacognição” significa julgar o controlador com frequências suavizadas de ganhos observados. Essas médias Beta e a mistura são heurísticas sob seleção adaptativa; não há garantia de calibração fora do benchmark. Uma expressão P(P(A)) sem especificar eventos não define, por si só, um novo mecanismo probabilístico.

“Autopoiese” corresponde aqui à manutenção de artefatos, estratégias e logs sob contratos fixos. “Dissonância” é um erro ou conflito mensurável, não uma alegação de experiência psicológica. “Auto-observável” significa que entradas, resultados e juízos podem ser inspecionados no rastreio, não que exista cognição plena.

## Síncrono, assíncrono e confirmação

O modo síncrono executa treino e avaliações em sequência. O assíncrono despacha o treino para uma thread e avalia os dois snapshots em tarefas concorrentes. Os pesos, referências e estatísticas dos snapshots são cópias somente para leitura. Dados de avaliação também são copiados. Nenhuma tarefa atualiza parâmetros compartilhados; o código não implementa SGD distribuído assíncrono.

Os conjuntos de treino, calibração e desenvolvimento usam geradores separados. Desenvolvimento é consultado repetidamente para seleção, com limiares operacionais, sem alegar significância estatística. A confirmação só é gerada e avaliada depois de congelar a seleção, uma vez, sem retorno ao treino. A semente e o gerador são públicos: esse isolamento de fluxo não é uma barreira contra um operador que ajuste o código após ler a reserva.

O ciclo para ao atingir o critério em desenvolvimento após pelo menos duas iterações, ou ao acabar o orçamento. A confirmação pode falhar, e isso é reportado. Acerto acima de um limiar em uma tarefa sintética não demonstra generalidade. O adversário guarda a entrada original e o estado de maior perda encontrado, mas PGD finito não certifica o pior ataque possível.
