# Previsão registrada antes do treino dos pesos distribuídos (2026-10-20)

Configuração: tokenizador de caracteres (mínimo 100 ocorrências), contexto 32, d = 32, 2 camadas, 4 cabeças
(~28 mil parâmetros), AdamW lr 3e-3 com aquecimento de 100 e cosseno, 3.000 passos de 16 janelas,
corpus = glosas do WordNet 3.0 (8,96 milhões de caracteres), 10% das glosas reservadas para teste.

- Bits por caractere no teste: entre 2,6 e 3,1 (centro 2,85). Âncoras: trigrama Witten-Bell 2,78 (Parte 100),
  GPT de 6,9 mil pesos 3,22 (Parte 69). Mecanismo: 4x mais pesos e mais camadas puxam para baixo; só 1,5 milhão
  de caracteres vistos (3.000 × 16 × 32) puxa para cima.
- O trigrama treinado no mesmo texto fica entre 2,70 e 2,85.
- Ganhar do trigrama: probabilidade ~35% (não é o esperado neste tamanho).
