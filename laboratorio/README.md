# Dois mecanismos de laboratório

Este código pertence a uma cópia de laboratório independente. Não foi integrado ao SYNTHAI. Os módulos textuais descrevem propostas; os resultados aqui dizem respeito somente aos contratos delimitados destes arquivos.

## Evidência sequencial

Em evidencia.py, cada resultado é um inteiro X_t em {0,1}. A hipótese nula exige **E[X_t | F_(t−1)] ≤ p0** em cada etapa. Uma aposta λ_t, escolhida com base somente no passado, deve pertencer a [0,1/p0]. O fator é 1+λ_t(X_t−p0), e E_0=1.

Os fatores são não negativos e têm esperança condicional ≤1. Seu produto forma uma supermartingal de teste. Sob essas premissas, a desigualdade de Ville dá P(sup_t E_t ≥1/α)≤α. Frações exatas permitem conferir trajetórias sem erro de arredondamento neste laboratório pequeno. O custo dessa representação cresce com o tamanho dos numeradores e denominadores.

OrcamentoErro exige Σα_j≤α entre suas alocações. Para obter uma garantia global, cada teste precisa ser válido para a seleção realizada, todas as tentativas devem ser contabilizadas e a alocação não pode ser reutilizada indevidamente. A classe não vincula automaticamente uma alocação a uma única instância do processo, nem impede alterações diretas por um chamador confiável. A API exige apostar antes de chamar observar; ela não impede acesso antecipado ao resultado, seleção favorável das observações, reinícios ocultos ou vazamento no gerador. A garantia se perde quando essas premissas falham.

Este mecanismo testa uma hipótese Bernoulli condicional. Não é uma implementação pronta de comparação de retorno contínuo, promoção geral do SYNTHAI ou identificação causal.

## Feedback persistente

Em feedback.py, o efeito protegido é **somar uma recompensa inteira limitada a um acumulador local e incrementar um contador**. O identificador da decisão, sua tentativa, versão, época de ativação, estado, recompensa aplicada e recibo são verificados no ledger. BEGIN IMMEDIATE serializa escritores; atualização, estado aplicado e recibo ficam na mesma transação.

Uma repetição válida do mesmo feedback não soma novamente. Conteúdo diferente para uma decisão aplicada é um conflito. Cancelamento confirmado impede aplicação posterior, sem apagar aplicações anteriores. Uma decisão criada em uma época antiga não volta a ser válida após v1→v2→v1. Reativar a versão já vigente é um no-op, não uma nova encarnação. Uma auditoria lê modelos, decisões e recibos sob uma única transação de leitura; isso impede misturar estados de commits distintos.

A propriedade é **no máximo uma atualização local por decisão lógica**. Uma atualização eventual depende de entrega válida e compatibilidade. Criar novamente uma decisão ou tentativa pode produzir erro de unicidade; a API inteira não é idempotente. Tentativas de transporte representam o mesmo efeito lógico, não novas ações independentes. Versões e origem são metadados de participantes confiáveis, sem autenticação externa.

O laboratório não garante uma execução externa exatamente uma vez, atomicidade de parâmetros arbitrários de aprendizagem, resistência a alterações diretas no banco ou segurança após restauração de um backup que apague decisões aplicadas. Durabilidade pressupõe SQLite e armazenamento que cumpram seus contratos. Usar WAL e synchronous=FULL não torna infalível o hardware.

## Verificações executadas

Foram executados **27 testes**, com resultado em resultado_testes.json e rastreio em testes.log. Incluem esperança exata em horizontes finitos sob a nula, parada adaptativa, parâmetros inválidos, recompensa duplicada ou conflitante, época ABA, conexões concorrentes, cancelamento concorrente, rollback após falha, encerramento de processo antes do commit e snapshot de auditoria durante commit concorrente.

Um teste mostra por conta explícita que selecionar a aposta após ver o resultado pode produzir esperança de fator maior que um. Essa demonstração ilustra uma premissa necessária; não demonstra que a API impeça vazamento.

A revisão independente de implementação encontrou a leitura de auditoria sem snapshot e verificou a correção, com relatório em revisao.json. Enumeração finita e testes de software não substituem a demonstração das premissas matemáticas ou a validação de implantação.

Para repetir no ambiente local:

```sh
python laboratorio/testar.py
```

Esses 27 testes são verificações de dois artefatos. Não são 27 módulos novos e não completam a meta de um milhão.
