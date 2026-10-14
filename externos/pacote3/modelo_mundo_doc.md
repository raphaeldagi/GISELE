# Modelo de mundo e planejamento latente

O experimento local usa um estado observado de duas coordenadas e uma ação em [-1,1]. O simulador gera transições de uma dinâmica linear determinística. Um encoder linear projeta estados em três coordenadas latentes, um encoder alvo acompanha o encoder online por média móvel, e um preditor recebe o estado latente atual junto da ação.

A perda inclui erro de previsão contra a representação alvo com stop-gradient e penalidades de variância/covariância nos embeddings online. Os gradientes foram conferidos por diferenças finitas. Essas penalidades não excluem matematicamente colapso: o encoder exatamente zero pode permanecer estacionário. O relatório mede posto e dispersão para detectar esse caso, em vez de contar erro latente zero como sucesso.

Após o treino, congela-se o encoder, alinha-se explicitamente o alvo e ajusta-se o preditor por mínimos quadrados no mesmo conjunto de treino. Essa reconciliação torna consistentes as bases de entrada e saída nos rollouts. No mundo linear, esse ajuste explica o erro muito pequeno. O desempenho não demonstra aprendizado geral de dinâmica física nem reprodução de JEPA em vídeo.

O MPC avalia sequências amostradas em horizonte e orçamento limitados, incluindo a sequência nula. Escolhe a primeira ação da melhor sequência prevista, observa o próximo estado e replaneja. O planejador não consulta a dinâmica real do simulador; essa dinâmica é usada para executar e avaliar as ações. A métrica latente determina os compromissos entre erro e custo da ação. Alterar escala do encoder sem revisar pesos do custo pode alterar a política.

Quatro condições iniciais compõem a avaliação de controle. Custos médios são descritivos desse conjunto pequeno, sem garantia estatística de vantagem geral. A avaliação de transições usa gerador separado do treino. Tarefas concorrentes recebem um snapshot somente para leitura.

## Continuidade explícita e encerramento

O checkpoint contém parâmetros, estado observado, versão de formato e flags de autorização/encerramento. A gravação é local e atômica por substituição de arquivo, com checksum SHA-256. O checksum detecta divergência do conteúdo; não autentica o autor nem impede um operador de reescrever conteúdo e checksum.

Restaurar verifica formato, shapes, finitude e consistência de bases declaradas alinhadas. Apenas carrega os dados. Não inicia processos, não adquire credenciais ou recursos, não conecta réplicas e não restaura autorização revogada. Um checkpoint encerrado continua encerrado. O proprietário pode explicitamente criar um novo controle numa nova execução; o programa não faz isso por conta própria.

Parada e efetivação de ações compartilham um lock local. Uma parada durante o planejamento impede a ação ainda não efetivada; uma ação que já ganhou o ponto de efetivação pode terminar antes de a parada retornar. Custos e efeitos anteriores não desaparecem. Isso é um protocolo cooperativo local, não contenção de código hostil.

Para executar:

```sh
python SYNTHAI_consolidado.py modelo-mundo --saida mundo.json --checkpoint estado.json
```

O checkpoint produzido pelo comando de demonstração é marcado como encerrado. As funções salvar_checkpoint/restaurar_checkpoint estão disponíveis no código editável. Nenhuma infraestrutura Meta, modelo LLaMA, serviço financeiro ou nuvem participa desse experimento.
