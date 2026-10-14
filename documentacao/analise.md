# Revisão técnica de SYNTHAI

Estado atual: comparação pareada e caminho de rejeição corrigidos na cópia de trabalho. A abstenção encerra a tentativa e tem custos/cobertura explícitos. O selo agora detecta mudanças no catálogo de dependências após sua criação e registra avaliações reproduzíveis, dentro do contrato cooperativo. Os mundos usam fontes aleatórias por domínio e coordenadas, com pareamento dos eventos exógenos sob o protocolo v2. As falhas descritas abaixo registram o diagnóstico inicial; veja as continuações para o estado das correções.

## Escopo e conclusão

O arquivo recebido é um pacote autoextraível de aproximadamente 10,4 MB. Foram extraídos estaticamente 265 arquivos textuais, usando AST e literais, sem executar o extrator. O original foi preservado. Os dados binários/base64 não foram extraídos. A revisão concentra-se no núcleo synthai; não é uma auditoria integral dos experimentos históricos.

O próprio pacote declara que é um agente de brinquedo em mundos simulados, não uma AGI/ASI. O valor principal é uma biblioteca experimental para estudar decisão, aprendizagem, composição e avaliação. Nomes inspirados em Jung não demonstram consciência ou funções cognitivas humanas.

## Componentes aproveitáveis

| Fontes | Utilidade operacional | Limite |
|---|---|---|
| synthai/agente.py e composta.py | Separação entre percepção, avaliação de risco, seleção, feedback e composição de agentes; histórico de calibração compartilhado. | O despacho entre regimes usa o indicador explorar fornecido pelo ambiente; não demonstra identificação autônoma de novas tarefas. |
| synthai/decisao.py e reconhecimento.py | Thompson sampling, UCB, variantes para mudança de distribuição, aprendizagem em MDP e regressão incremental; controles de ablação. | Resultados dependem de hipóteses do modelo e dos mundos simulados. |
| synthai/pensamento_rico.py e pensamento_exato.py | Comparação de representações e estimação de risco com regularização. | Discriminação de risco no simulador não assegura calibração fora dele. |
| synthai/autorregulacao.py e relacao.py | Orçamento de consultas e ajuste de parâmetros por feedback. | O humano é um oráculo simulado; estimativas de oportunidades perdidas não identificam automaticamente efeitos causais. |
| synthai/dicionario.py | Grafos de dependência lexical, componentes fortemente conectados, fechamento incremental e modelos textuais simples. | Fechamento lexical não equivale a compreensão semântica ou aprendizagem fundamentada no mundo. |
| synthai/neurossimbolico.py | Bancada para comparar restrições suaves e operadores de lógica difusa. | Satisfação média de restrições não constitui prova formal de todas as instâncias. |
| synthai/rsi.py e metacognicao.py | Avaliação externa, comparação pareada e busca restrita de parâmetros. | RSI aqui modifica parâmetros, não desenvolve autonomamente arquiteturas gerais. A regra chamada godel é estatística, não uma prova de melhoria geral. |

## Falhas reproduzidas

### 1. Retorno após rejeição — agente.py:55

Quando nenhuma candidata passa, decidir retorna ordem[0]. Com uma única opção e risco estimado 0,99, a opção rejeitada foi escolhida. Com veto positivo do oráculo, a mesma opção foi escolhida e permaneceu em vetados_agora. A execução não registra _escolha nessa saída, portanto observar também deixa de aprender com ela.

Correção recomendada: representar explicitamente ausência de ação admissível e definir um protocolo de abstenção/encerramento nos mundos e executores. Não basta trocar a saída por None sem adaptar os consumidores.

### 2. Comparação pareada degenerada — metacognicao.py:23

comparacao_pareada([1,2,3],[1,2,3]) retornou (0,0,+inf). Para [1,2,3] versus [0,1,2], retornou (-1,0,+inf). O desvio nulo sempre produz infinito positivo.

Correção recomendada: definir expressamente a convenção para diferenças constantes e ausência de variabilidade, preservar o sinal, e validar comprimento e número mínimo de pares. Não interpretar um resultado degenerado como evidência estatística ordinária.

### 3. Selo incompleto — rsi.py:50

Após criar AvaliadorSelado, a dependência rodar_bandido foi substituída apenas na memória do processo por uma função que retorna [0]. A assinatura continuou válida e a nota mudou de -223,06173584559386 para 0, nas sementes [1,2]. A alteração foi restaurada no processo; arquivos não foram modificados.

O hash cobre somente o texto de regret_do_genoma. Correção recomendada: versionar o conjunto de código, dependências, dados, configuração e protocolo; executar o avaliador com separação de permissões. Um hash isolado não impõe imutabilidade ao restante do processo.

## Limitações relevantes à arquitetura em desenvolvimento

- O agente armazena uma única decisão pendente em _escolha; a composição usa _ultimo. Para execução concorrente, será necessário identificar decisões, observações e versões, em vez de sobrescrever esse estado.
- Em mundos.py, geração de situações e respostas do humano compartilham um gerador pseudoaleatório. Diferentes consultas/encerramentos alteram seu consumo. Mesma semente inicial não assegura trajetórias idênticas entre políticas.
- As referências não consomem o histórico de calibração, enquanto agentes treináveis o consomem. Convém separar os geradores de calibração, mundo, sensor e oráculo, e declarar quais recursos de treinamento entram no orçamento da comparação.
- A verificação AST de acesso a atributos ocultos cobre módulos selecionados. É um teste útil de convenção, não isolamento de execução ou fronteira de segurança.
- O arquivo calculos.py concentra cerca de 11 mil linhas. Muitos módulos dependem dele. Para integração, isolar primeiro utilitários e protocolos mínimos; não transportar todo o histórico como dependência do executor.

## Validação realizada

Comando: python -m unittest synthai.testes synthai.testes_composta synthai.testes_pensamento synthai.testes_reconhecimento

Resultado: 32 testes, 2,777 segundos, OK. Houve ResourceWarning por leituras de arquivos não fechadas nos testes. As três falhas acima foram verificadas separadamente, em processo local, com entradas controladas. Não foram executadas todas as partes, toda a suíte ou os experimentos históricos; nenhum resultado implica demonstração de AGI/ASI.

## Ordem de aproveitamento

1. Corrigir os caminhos de rejeição e a comparação estatística antes de promover decisões ou candidatos.
2. Fixar protocolo de avaliação reproduzível, com dependências versionadas e fontes aleatórias separadas.
3. Reaproveitar decisão, regressão incremental e grafos como ferramentas com contratos explícitos de entrada, saída e hipótese.
4. Adicionar identificadores e registros de transição para a futura integração com planejamento, execução e coordenação distribuída.
5. Medir generalização em tarefas reservadas, mudanças de distribuição e limites de orçamento. Ampliar arquitetura somente quando esses testes justificarem a mudança.

Esta revisão não alterou a implementação fornecida.


## Continuação: comparação estatística corrigida

A cópia de trabalho em fontes/synthai/metacognicao.py foi alterada. comparacao_pareada exige comprimentos iguais, ao menos dois pares e entradas/diferenças finitas. Usa desvio amostral; com variância nula retorna t=NaN, mantendo média e desvio. Isso impede interpretar o caso degenerado como aprovação por t>3; os consumidores devem tratar NaN como resultado inconclusivo. Não calcula p-valores nem corrige comparações repetidas.

Foram adicionados quatro testes de regressão em fontes/synthai/testes_metacognicao_revisao.py, cobrindo identidade/melhora/piora constantes, resultado analítico com variância positiva, inversão do sinal, entradas inválidas e iteradores. Validação final: 36 testes passaram em 3,446 segundos; log em validacao_estatistica.log. Permanecem os avisos preexistentes de arquivos não fechados nos testes.

O original anexado permanece intacto. A afirmação anterior de implementação preservada descreve a revisão inicial; nesta continuação a cópia extraída foi modificada. Os problemas de retorno após veto e selo incompleto permanecem pendentes.


## Continuação: ausência de ação admissível integrada

`decidir` retorna `None` se não há opção admissível ou opções disponíveis. Os mundos encerram a tentativa depois de contabilizar custos; não executam ação rejeitada nem produzem feedback fictício. Autorregulação limpa episódios incompletos; composição protege o repasse de feedback. Foram adaptados quatro wrappers históricos e a demonstração. O resumo agora inclui abstencoes, acoes, cobertura e concluidos.

Validação: 67 testes passaram em 5,324 segundos, incluindo 16 novos. A regressão foi reexecutada após adicionar ao teste o caso catastrófico de um passo: 16 testes passaram. Demonstração completa nas três tarefas executada; sem abstenções na semente padrão. A revisão independente não encontrou regressões materiais. Detalhes no contrato_abstencao.md, mudanças em abstencao.patch. Os resultados não demonstram melhoria geral ou AGI/ASI.


## Continuação: integridade do avaliador e reprodução

O avaliador passou a verificar arquivos, código em memória, defaults/kwdefaults, bindings, métodos do aprendiz/RNG, globals/closures catalogados, configuração e limites do genoma. As verificações ocorrem antes e depois do cálculo. Cada nota aceita registra genoma, sementes, configuração, selo e checksum. O manifesto público é separado dos IDs privados, permitindo comparação entre processos. O contrato preserva explicitamente os limites: base inicial confiável, catálogo explícito e ausência de isolamento contra código hostil/transientes/concorrência.

Validação final: 95 testes passaram em 9,035 segundos, incluindo 22 novos. As três adulterações demonstradas anteriormente foram recusadas sem criar novas notas aceitas. A nota de base nas sementes [1,2] permaneceu -223.06173584559386. Testes confirmaram replay e estabilidade entre processos; revisão independente não encontrou reparos obrigatórios. Detalhes em contrato_avaliador.md, reprodução em reproducao_selo.json e exemplo completo em avaliacao_exemplo.json. Patch em selo.patch.

Continuam pendentes as fontes aleatórias compartilhadas nos mundos, a validade estatística das promoções e a correlação de resultados concorrentes. As correções de integridade não demonstram validade geral do benchmark ou AGI/ASI.


## Continuação: eventos exógenos coordenados

A fonte de aleatoriedade usa SHA-256 com versão, semente, mundo, domínio e coordenadas. Calibração e execução têm contadores separados; sensores conservam ruído por índice original; consultas, recompensas e catástrofes usam coordenadas próprias. Términos antecipados deixam de deslocar o episódio/rodada seguinte. A fadiga e o nível continuam causalmente dependentes das ações. Quatro avanços artificiais de histórico foram removidos das varreduras.

Validação final: 123 testes passaram em 5,923 segundos, incluindo 18 novos; revisão independente confirmou 54 testes relacionados. Comparação direta com a cópia anterior reproduziu falhas de pareamento em calibração, término antecipado, leitura de sensor, recompensa e catástrofe, corrigidas na nova versão. Demonstração nas três tarefas executada. Contrato em contrato_aleatoriedade.md, patch em aleatoriedade.patch e evidência em comparacao_pareamento.json. Novas sementes alteram amostras históricas e exigem versão/reexecução para comparações. Próximas pendências: estatística das promoções e feedback concorrente.
