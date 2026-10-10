# Texto recebido do usuário na Parte 81, guardado como DADO

A mensagem reenviou o relatório do Módulo 007 (idêntico ao de `externos/texto_recebido_parte75b.md`), trouxe o texto do Módulo 008 (memória episódica), com uma parte repetida duas vezes, e o
pedido: **"Tire dos nossos trabalhos tudo que não serve pra nada."**

### Módulo 008 — Memória episódica, causalidade e aprendizagem com erros (resumo, com as palavras do texto entre aspas)

- Um episódio: episode_id, hypothesis, prediction, intervention, observation, evidence_quality, conclusion, previous_episode. "A regra principal é preservar a previsão original. Se o sistema modificar a
  previsão depois de observar o resultado, deverá guardar essa modificação separadamente."
- "Correlação não é causalidade": menos falhas nos dias frios não prova que a temperatura é a causa (carga de trabalho, manutenção).
- Brier: E1 previsto 80%, observado sim; E2 previsto 30%, observado não; BS = ((0,8 − 1)² + (0,3 − 0)²)/2 = 0,065. "A memória não deve simplesmente alterar a confiança após qualquer resultado
  isolado."
- Limites: persistência entre sessões; avaliação num conjunto de teste não usado para ajustar; controles para causalidade; o hash detecta diferenças mas não impede alterações (cadeia de hashes,
  assinaturas).
- O ciclo (mermaid): memória semântica → formular hipótese → prever → selecionar experimento → observar → registrar episódio → verificar evidência → atualizar modelo → avaliar desempenho → hipótese.
  "Esse ciclo descreve o comportamento que estamos construindo, não um processo autônomo em execução contínua."
