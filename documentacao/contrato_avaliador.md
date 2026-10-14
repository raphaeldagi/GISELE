# Contrato de integridade e avaliação reproduzível

## Comportamento

`AvaliadorSelado(k=10, t=2000)` calcula a nota externa como menos arrependimento médio de QEpsilon em bandidos de Bernoulli. A configuração exige inteiros positivos. `nota(genoma, sementes)` preserva o uso anterior e agora aceita iteradores de sementes, materializando-os antes do cálculo.

As sementes devem ser inteiras e a coleção não pode ser vazia. alfa, eps e q0 devem respeitar os limites do espaço de mutação e ter valores finitos; demais dados do genoma precisam ser representáveis em JSON finito. A nota aceita deve ser finita e estar entre -t e 0. O relato do agente não participa da nota.

## Manifesto

O manifesto inclui:

- SHA-256 dos arquivos rsi.py, decisao.py e random.py.
- Identificação e hashes de código Python carregado, defaults e kwdefaults do catálogo de dependências da nota.
- Métodos do aprendiz QEpsilon e métodos relevantes de random.Random, globals/builtins encontrados nessas funções, conteúdo das células de fechamento e atributos das classes.
- Configuração k/t, limites do genoma, identificação do protocolo, derivação das sementes e versão/implementação/cache tag do Python e versão de marshal.

O snapshot privado compara também identidades dos bindings. IDs de objetos e caminhos absolutos não entram no selo exportado. O catálogo é explícito e deve ser revisado se o benchmark passar a chamar novas dependências. A checagem é conservadora: mudanças em partes não usadas dos arquivos selados também invalidam o avaliador existente.

A assinatura pública agora é um método da instância, pois inclui sua configuração. Os consumidores examinados usam o construtor, nota e selo; seus testes continuaram aprovados.

## Ordem de avaliação

1. Verificar integridade.
2. Materializar sementes, copiar o genoma e validar entradas.
3. Verificar novamente: iteradores de entrada podem ter alterado dependências durante a leitura.
4. Calcular com k/t explícitos, mantendo as derivações de RNG existentes.
5. Verificar integridade depois do cálculo e validar o domínio da nota.
6. Registrar e devolver somente a nota aceita.

Divergências e arquivos ausentes produzem RuntimeError. Entradas ou notas inválidas produzem ValueError. Recusas não incrementam chamadas nem entram no histórico de notas aceitas. Reatribuir a tag pública selo não altera a referência inicial privada.

## Registro e reprodução

`manifesto` retorna uma cópia; `registros` retorna cópias dos registros aceitos. Cada registro contém número, selo, configuração, genoma, sementes efetivamente usadas, nota e checksum SHA-256 de sua representação JSON canônica. O checksum permite conferir consistência; não é assinatura de autoria. Dados retornados podem ser alterados sem modificar o histórico interno.

Exemplo reproduzível em avaliacao_exemplo.json: genoma inicial, sementes [1,2], k=10, t=2000, nota -223.06173584559386. O manifesto e o registro devem ser conservados juntos. Para reproduzir, conferir o selo/artefatos e avaliar o genoma nas sementes/configuração registradas. Comparações entre configurações ou artefatos diferentes exigem análise própria.

## Validação

95 testes selecionados passaram em 9,035 segundos, incluindo 22 novos testes de integridade/reprodução e os 6 testes existentes da Parte 33. Os testes cobrem bindings, métodos do aprendiz, substituição de __code__, defaults/kwdefaults, métodos do RNG, substituição de builtins via globals, alterações de arquivo, configuração, limites do genoma, mudança durante cálculo/consumo de sementes, cópias públicas, domínio da nota e reprodução. O selo foi igual em dois processos com o mesmo ambiente/artefato/configuração.

reproducao_selo.json registra as três adulterações reproduzidas separadamente: trocar rodar_bandido, alterar QEpsilon.atualizar e mudar defaults de regret_do_genoma. Todas foram recusadas; só a nota de base entrou no histórico.

Os logs são regressoes_selo.log e validacao_selo.log. Permanecem avisos preexistentes de arquivos não fechados em testes e auditoria estática. A suíte completa e os experimentos históricos extensos não foram executados.

## Limites

O selo detecta divergências após sua criação em um processo cooperativo. Ele não autentica a base inicial, protege o próprio auditor contra adulteração, bloqueia mudanças transitórias que sejam restauradas entre checagens ou isola código hostil. A implementação não oferece transação contra modificações simultâneas, nem execução concorrente do mesmo avaliador. A versão do runtime é registrada, mas não se calcula o hash de todos os binários e bibliotecas nativas do ambiente.

Integridade e reprodução não demonstram que o benchmark mede inteligência geral, que o genoma melhorou em novas tarefas ou que a regra de seleção é uma prova matemática. Múltiplas comparações, ruído de seleção e generalização continuam sendo questões de avaliação distintas.

## Continuidade

Esta etapa modifica somente rsi.py e adiciona os testes. O anexo original não foi editado. selo.patch corresponde à cópia de trabalho antes desta etapa; manifesto_selo.json registra hashes de antes/depois. Próximos problemas operacionais identificados: fontes aleatórias compartilhadas nos mundos, validação estatística das promoções e associação de feedback a decisões concorrentes.

A revisão independente executou os testes de integridade e da Parte 33 e não encontrou reparos obrigatórios. Também confirmou selo e nota iguais em subprocessos com diferentes PYTHONHASHSEED. Uma verificação posterior adicionou os limites do genoma ao manifesto e confirmou sua recusa quando alterados.

Atualização da etapa seguinte: os mundos agora usam fontes coordenadas por domínio, conforme contrato_aleatoriedade.md. O protocolo de RSI descrito neste arquivo e seu exemplo não foram alterados.
