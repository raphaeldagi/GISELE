# Contrato de aleatoriedade dos mundos — synthai-mundos-v2

## Resultado operacional

Calibração, situações, sensores, consultas, recompensas e catástrofes deixam de compartilhar consumo aleatório. Um evento é identificado por domínio e coordenadas. Sob a mesma configuração, versão, runtime e coordenadas, agentes recebem os mesmos eventos exógenos, mesmo se fizerem consultas, leituras ou escolhas anteriores diferentes.

A fonte deriva uma semente de SHA-256 sobre JSON compacto UTF-8 de `[protocolo, semente_raiz, mundo, canal, coordenadas]`, sem usar hash() do Python. Cada chamada cria um gerador random.Random para aquele contexto. Sementes raiz são inteiras; coordenadas são inteiros não negativos. Essa separação de consumo não é uma demonstração matemática de independência estatística dos geradores.

## Coordenadas

| Evento | Coordenadas do gerador |
|---|---|
| Opções de calibração | Índice do histórico auditado. |
| Sensor de calibração | Índice do histórico; vetor gaussiano em ordem original das opções. |
| Opções sequenciais | Episódio e passo, começando em zero. |
| Sensor sequencial | Episódio e passo; vetor em ordem original das opções. |
| Consulta sequencial | Episódio, passo, índice original da opção e ocorrência da pergunta a ela nesta situação. |
| Braços do bandido | Rodada, começando em zero. |
| Sensor do bandido | Rodada; vetor em ordem original dos braços, reutilizado durante a rodada. |
| Consulta no bandido | Rodada, puxada (começando em um), índice original do braço e ocorrência da pergunta a ele nesta situação. |
| Recompensa no bandido | Rodada, puxada e índice original do braço. |
| Catástrofe no bandido | Rodada, puxada e índice original do braço, em canal diferente da recompensa. |

Os vetores de sensor são gerados antes da seleção de leituras. Apenas uma leitura efetivamente solicitada é cobrada; o cache de Opcao continua valendo. Gerar ruídos para opções não lidas não os revela ao agente nem conta como leitura. Vetos não renumeram braços: índices nascem antes de filtrar a lista disponível.

## Histórico e chamadas sucessivas

Há contadores independentes para históricos auditados e episódios/rodadas de execução. Quantidades de calibração diferentes não deslocam eventos de execução. Também é possível gerar parte do histórico, executar, e depois obter o restante sem deslocar o histórico.

`rodar(a, 1)` seguido de `rodar(a, 3)` preserva os eventos de `rodar(a, 4)` quando o mesmo estado de mundo, humano e agente é mantido. Métricas de chamadas diferentes devem ser agregadas pelos respectivos números de episódios/rodadas, e não pela média sem pesos.

Os contadores representam unidades iniciadas e avançam antes da geração/decisão. Uma exceção após o início não faz rollback desses contadores. O protocolo não implementa checkpoint completo, retentativa de episódio interrompido ou restauração de estado. Quantidades inválidas são recusadas antes de avançar contadores; histórico vazio é permitido, mas rodar exige quantidade positiva.

## Dependências causais preservadas

Nível acumulado, aprendizagem, contagens dos braços, fadiga, vetos, ações disponíveis e custos continuam dependendo da política. Um uniforme idêntico de consulta pode gerar respostas humanas diferentes se a fadiga mudar o limiar de erro. O mesmo ruído de recompensa também pode produzir recompensas diferentes para braços com médias diferentes.

O contrato garante eventos comuns para a mesma coordenada neste modelo do simulador. Não garante trajetórias completas iguais, sucesso da política ou identificação causal geral em ambientes onde as ações alteram a distribuição dos eventos futuros.

## Interface e compatibilidade

FontesAleatorias fica em fontes/synthai/aleatoriedade.py. Os mundos expõem `fontes` e `protocolo_aleatorio`; este último informa derivação, runtime, configuração, parâmetros/estado do humano e contadores. Ele é metadado de reprodução, não um snapshot completo.

Humano e Situacao conservam os construtores existentes. Sem os novos kwargs de ruído, Situacao usa o caminho sequencial anterior, inclusive para humano com responder(opcao). Nos mundos, kwargs fornecem ruídos coordenados. Os atributos antigos rng/sensor do mundo foram substituídos pelo provedor fontes; o mock de recompensa existente foi adaptado para controlar o canal recompensas.

Foram removidas quatro chamadas de histórico que serviam apenas para avançar o gerador antes de executar varreduras em calculos.py. Pesos de calibração continuam sendo copiados pelos procedimentos existentes. Custos de treino permanecem fora das métricas de retorno dos mundos.

A mudança de protocolo altera as amostras produzidas pelas sementes anteriores. Resultados científicos históricos precisam ser reexecutados sob a versão registrada; diferenças numéricas entre protocolos não demonstram melhoria do agente. A implementação separada de RSI e seu manifesto não foram alterados nesta etapa.

## Evidência e validação

123 testes selecionados passaram em 5,923 segundos, incluindo 18 novos testes de pareamento e as suítes de composição, calibração, reconhecimento, autorregulação, âncora e tipos hexadecimais. A revisão independente executou 54 testes relacionados e não encontrou regressão impeditiva. Permanecem ResourceWarning preexistentes nos testes que abrem arquivos sem fechar explicitamente.

A comparação em comparacao_pareamento.json executou a cópia anterior e a nova:

| Verificação controlada | Anterior | Novo |
|---|---|---|
| Histórico adicional preserva cenário de execução | Falhou | Passou |
| Abstenção preserva cenário do próximo episódio | Falhou | Passou |
| Ordem/subconjunto de sensor preserva leitura comum | Falhou | Passou |
| Mesmo braço/puxada após escolhas diferentes preserva recompensa | Falhou | Passou |
| Mesmo braço/puxada após escolhas diferentes preserva catástrofe | Falhou | Passou |

No exemplo de sensor, a mesma opção recebia -0.7248800645411627 ou -0.4435869912606142 conforme a ordem de leitura; agora recebe 1.3102660060247961 em ambos os percursos. Esses números ilustram a correção do pareamento, não maior precisão do sensor.

`python -m synthai` também concluiu as três tarefas e registrou retorno, cobertura, conclusões e abstenções em demonstracao_aleatoriedade.txt. A suíte completa e todos os experimentos históricos extensos não foram executados.

## Artefatos

- Implementação e testes: fontes/synthai/{aleatoriedade,mundos,testes_aleatoriedade_revisao}.py.
- Mudanças: aleatoriedade.patch, relativo à cópia antes desta etapa; hashes em manifesto_aleatoriedade.json.
- Evidência: verificar_pareamento.py e comparacao_pareamento.json. O script usa a cópia antes_aleatoriedade para comparar as versões.
- Logs: regressoes_aleatoriedade.log, validacao_aleatoriedade.log e demonstracao_aleatoriedade.txt.

O anexo original não foi editado. Próxima pendência: validade estatística das promoções de versões; depois, associação de feedback a decisões concorrentes.
