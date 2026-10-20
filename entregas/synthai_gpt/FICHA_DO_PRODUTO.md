# SYNTHAI-GPT 1.0.0 — ficha do produto

**Um transformer do tipo GPT, de ponta a ponta, num arquivo Python só, sem nenhuma dependência.**

## Em uma frase
O SYNTHAI-GPT é a arquitetura de um GPT (transformer decodificador autorregressivo, a família do GPT-2) escrita do zero em
Python puro: treino, geração, avaliação e pesos. Vem com um modelo pré-treinado no dicionário WordNet e com um laboratório
de 3.950 linhas de métodos numéricos e de teoria dos jogos. Cada peça é verificável: são 72 testes, incluindo a conferência do
gradiente por diferenças finitas.

## O que vai no pacote
| Arquivo | O que é |
|---|---|
| `SYNTHAI_GPT.py` | O produto inteiro: motor GPT, tokenizadores, treino, geração, avaliação, laboratório NEXUS-RAPHAEL 3.0.0, testes e linha de comando |
| `synthai_gpt_pesos.json` | Pesos pré-treinados nas glosas do WordNet 3.0, com selo SHA-256 |
| `FICHA_DO_PRODUTO.md` | Este documento |
| `LICENCAS_DOS_DADOS.txt` | Avisos do WordNet 3.0 e da OpenWordNet-PT, que precisam acompanhar os pesos |

## Especificação técnica
- **Arquitetura**: embeddings de ficha e de posição aprendidos → N blocos pré-LayerNorm [atenção causal de H cabeças + resíduo;
  MLP d→4d→d com GELU + resíduo] → LayerNorm final → projeção para o vocabulário → softmax. A inicialização segue a do
  GPT-2 (σ = 0,02, com as saídas dos resíduos reduzidas por 1/√(2N)).
- **Treino**:
  - entropia cruzada com gradiente escrito à mão;
  - otimizador AdamW: decaimento de peso desacoplado, recorte da norma do gradiente em 1, aquecimento linear e decaimento em cosseno;
  - lote repartido entre processos locais, com o mesmo gradiente médio do treino serial (testado);
  - checkpoint com o estado do otimizador; a retomada dá os mesmos pesos do treino contínuo (testado).
- **Tokenização**: por caractere, ou BPE (byte-pair encoding) treinável, com ida e volta exata.
- **Geração**: gulosa, temperatura, top-k, top-p (núcleo), penalidade de repetição e semente reprodutível.
- **Avaliação**: bits por caractere em glosas que o modelo nunca viu, sempre ao lado de duas linhas de base: um n-grama
  (Witten-Bell, ordem 3) treinado no mesmo texto e a distribuição uniforme.
- **Pesos**: JSON com selo SHA-256. Carregar pesos nunca executa código (não há pickle), e um peso adulterado é recusado (testado).
- **Segurança**: o código não acessa a rede, não roda subprocessos de si mesmo e não usa eval/exec. Um teste confere isso
  na árvore sintática do próprio arquivo.
- **Requisitos**: Python 3.10 ou mais novo, em qualquer sistema operacional. Não precisa de GPU.

## Números medidos dos pesos distribuídos
| Medida | Valor |
|---|---|
| Parâmetros | 31.501 (vocabulário 77, contexto 32, d = 32, 2 camadas, 4 cabeças) |
| Treino | 3.000 passos × 16 janelas de 32 caracteres; 41 min em 4 núcleos de CPU |
| Corpus | glosas do WordNet 3.0, 8.963.290 caracteres; 10% das glosas reservadas para teste |
| **Bits por caractere no teste** | **2,880** |
| Trigrama Witten-Bell treinado no mesmo texto | 3,190 |
| Uniforme sobre o vocabulário | 6,539 |
| Trigrama bayesiano da série SYNTHAI (Parte 100) | 2,78 (ainda melhor que este modelo) |
| Previsão registrada antes do treino | GPT em [2,6; 3,1]: acertou. Trigrama em [2,70; 2,85]: errou (3,19) |
| Selo SHA-256 dos pesos | conferido ao carregar |

Exemplo gerado (temperatura 0,7, semente 1): *"the act of a shapose somaning a pup in in a mactiontic revermanning"*. São palavras plausíveis
no formato de uma definição, sem significado garantido. É o que um modelo deste tamanho faz, e a ficha deve dizer isso.

## Para quem serve (e como vender)
1. **Ensino de IA e de LLMs**: cursos, bootcamps e universidades. É o único lugar em que o aluno lê *toda* a conta de um GPT
   (ida, volta, otimizador) num arquivo, sem caixa-preta de framework, e confere cada gradiente.
   Produto possível: licença por turma, com o roteiro de aulas como extra.
2. **Ambientes sem dependências**: sistemas embarcados, servidores fechados, ambientes regulados e auditorias de código.
   Roda onde só há a biblioteca padrão do Python.
3. **Auditoria e reprodutibilidade**: sementes fixas, pesos com selo e testes que conferem a matemática. Serve como referência
   ("oráculo") para verificar implementações aceleradas em PyTorch ou JAX.
4. **Treino em corpus próprio**: `gpt treinar --corpus seu_texto.txt` treina um modelo pequeno de domínio (estilo de documentos,
   nomes, códigos), com a comparação honesta contra o n-grama.

Uma estrutura de oferta possível:
- **Básico**: o arquivo e os pesos.
- **Profissional**: Básico + treino num corpus do cliente + relatório de avaliação contra as linhas de base.
- **Ensino**: Básico + material didático.

## O que se pode afirmar, e o que não se pode
- **Pode**:
  - "arquitetura do tipo GPT (transformer decodificador) implementada do zero em Python puro";
  - "gradiente verificado numericamente";
  - "sem dependências";
  - "pesos com selo de integridade";
  - os números da tabela acima, com a linha de base ao lado.
- **Não pode**:
  - comparar com o ChatGPT ou com modelos de bilhões de parâmetros: este modelo tem dezenas de milhares;
  - dizer que "conversa" ou que "sabe fatos": ele gera texto no estilo de definições de dicionário;
  - insinuar relação com a OpenAI. "GPT" aqui nomeia a arquitetura, não um produto de terceiros;
  - chamar o modelo de AGI ou ASI.
- **Antes de vender**: escolha e anexe uma licença para o código. Se você é o titular, uma licença comercial própria ou uma
  dupla (open source + comercial) são as opções usuais. Para nome e marca, consulte um advogado da sua jurisdição.

## Obrigações de licença dos dados (acompanham os pesos)
- **WordNet 3.0**: "WordNet 3.0 Copyright 2006 by Princeton University. All rights reserved." O uso, a cópia, a modificação e a
  distribuição são permitidos sem taxa, desde que o aviso e o termo de isenção acompanhem todas as cópias. O nome de
  Princeton não pode ser usado em publicidade.
- **OpenWordNet-PT** (se você treinar com `--corpus ownpt`): CC BY 4.0, que exige atribuição.
