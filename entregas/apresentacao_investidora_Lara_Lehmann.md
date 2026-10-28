# SYNTHAI: protótipo de IA verificável

**Apresentação para Lara Lehmann, investidora-anjo.** Repositório GISELE, outubro de 2026.

---

## 1. Em uma frase
A SYNTHAI é um protótipo de agente de IA em que **cada número afirmado é reproduzível, cada previsão é registrada antes de ser testada e cada peça de decisão roda igual,
bit a bit, em Python e em Java**. Ela não é uma AGI. O que ela vende é a **confiança medida**: uma IA que sabe quanto acerta e mostra o placar.

## 2. O problema
Os sistemas de IA atuais costumam errar com confiança. Afirmam mais do que entregam, e quase nunca publicam quantas das próprias previsões acertaram. Para quem decide
(saúde, finanças, jurídico, indústria), o risco não é só errar. É não saber **quando** o sistema erra.

## 3. O que já existe (tudo medido no repositório)

| item | número | de onde sai |
|---|---|---|
| Partes de pesquisa documentadas, cada uma com previsões registradas antes de medir | 158 | `ASI_AGI_parte*.md` |
| Funções de cálculo com resultado reproduzível | 773 | `calculos.py` (18.888 linhas, só biblioteca padrão do Python) |
| Módulos do agente | 64 | pacote `synthai/` |
| Arquivos de teste automatizado | 123 (845 testes, todos passando) | `synthai/testes*.py` |
| Traduções Python ↔ Java conferidas bit a bit | 106 rodadas, todas iguais | `dialogo/`, `python3 dialogo/verificar.py` |
| Resultados publicados que a regressão reproduz a cada mudança | 216 de 216 | `testes_de_regressao()` |
| Calibração: das faixas declaradas com 90% de confiança, quantas acertaram | cerca de 91% (medido nas Partes 113 a 121) | placar das previsões |

O projeto inteiro cabe num único arquivo Python executável (`SYNTHAI_completo.py`, 161 mil linhas). Ele roda **offline**, sem dependências externas e sem chave de API.

## 4. Como funciona
O agente tem cinco formas, todas no mesmo pacote e todas medidas umas contra as outras:
1. **Decisão bayesiana exata:** sabe quando pedir ajuda a um humano, com o custo da pergunta em conta (valor da informação).
2. **Gerador no formato GPT:** transformer mínimo escrito do zero (atenção, treino, amostragem), pré-treinado nas definições do dicionário WordNet (inglês) e OpenWordNet-PT
   (português).
3. **Substrato pulsado:** neurônios do tipo LIF e Izhikevich que aprendem por STDP.
4. **Modelo de mundo que planeja:** aprende a dinâmica do ambiente e planeja nela (controle preditivo e LQR).
5. **Aprendizado por reforço sobre o dicionário:** jogo de palavras com Q-learning e GRPO, explicado por uma lei exata da densidade das palavras.

A base psicológica é a de Carl Jung: cada função do agente (percepção, pensamento, intuição, sentimento) é um módulo, e cada conceito vira equação ou simulação, com o
registro de onde a formalização funciona e onde quebra.

## 5. O diferencial
- **Previsão antes do experimento.** Toda parte registra no git, antes de rodar, faixas numéricas que podem dar errado. O acerto é contado por código, não por leitura.
- **Metacognição medida.** O sistema prevê as próprias previsões (quantas, de que largura, quantas vão acertar) e mantém três placares separados: o do mundo, o "sobre mim"
  e o das previsões sobre previsões. Quando a calibração caiu para 77% (Parte 79), a correção virou regra e ela voltou para cerca de 91%.
- **Independência de linguagem.** As peças de decisão dão o mesmo resultado, até o último bit, em Python e em Java. Isso prova que o comportamento é do algoritmo, não da
  plataforma. Também mapeia exatamente onde as linguagens divergem: exp, log, pow, funções trigonométricas em argumentos largos e ordem das somas.
- **Segurança por desenho.** O código não acessa a rede, não se replica e não executa código recebido. Todo código recebido é auditado pela árvore sintática, sem ser
  executado, e reescrito do zero. Essas recusas estão registradas no repositório.

## 6. Limitações (ditas com a mesma régua)
- É um **protótipo de pesquisa**, não um produto. Não há interface para usuário final.
- O gerador GPT é pequeno (milhares de pesos). Ele ainda **perde para um modelo de trigramas** na previsão de caracteres: a forma de GPT é uma aposta de escala, não um
  resultado.
- Não há comparação com modelos comerciais em benchmarks públicos.
- "ASI" e "AGI" aparecem no projeto como o **papel** de uma das vozes do diálogo interno, não como capacidade medida.

## 7. Para onde o investimento iria
1. **Produto de auditoria de IA:** levar o método (previsões registradas, placar de calibração, auditoria sintática de código recebido) a equipes que já usam modelos de
   terceiros. É o uso mais próximo do que o protótipo já faz.
2. **Escala do gerador:** treinar o transformer com mais pesos e corpus, sempre medido contra a linha de base, para testar a aposta de escala.
3. **Interface e documentação** para um piloto com um primeiro cliente.

*Valor, participação e prazos: a definir na conversa.*

## 8. Como verificar em 5 minutos
```
python3 SYNTHAI_completo.py         # o projeto inteiro em um arquivo
python3 calculos.py 158             # uma parte, com a regressão no final
python3 dialogo/verificar.py        # as 106 traduções Python ↔ Java, bit a bit
```
Nada aqui pede confiança: tudo pede execução.
