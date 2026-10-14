# Como eu construiria uma AGI/ASI — Parte 88 (0x58): a arquitetura autopoiética recebida

> Continuação da [Parte 87](ASI_AGI_parte87_compressao_plasticidade_grpo.md). Pedido do usuário: um relatório "Arquitetura Cognitiva Autopoiética Recursiva" com um código (`asi_autopoietic_core.py`: LFI1
> paraconsistente, cosseno duplicado, dez camadas verso/reverso, pilha adversarial de 7, delírio controlado, metacognição e probabilidade aninhadas). É o QUARTO relatório desta família (as Partes 83, 85 e
> este pedido repetem cosseno duplicado, sete camadas adversariais, delírio, lógica dual). Parte de auditoria: o código é dado, não executado; reimplemento e meço só o que é NOVO em relação às Partes 83/85/87,
> e aponto o que já foi medido.
>
> **O que já está medido (não repito):** o "cosseno duplicado" é a identidade do ângulo duplo (Parte 85, P1991); a "pilha adversarial de 7/N camadas" não treina (Parte 85, P1992; Parte 83); o "vetor recursivo"
> normalizado não diverge (Parte 85, P1994); o delírio (recozimento/ruído) não dá ASI sozinho (Parte 84, quatro falhas) e o próprio usuário já concordou com isso (Parte 85). **O que é novo aqui:** a LFI1 (lógica
> de inconsistência formal), a "probabilidade dentro da probabilidade" implementada como uma conta concreta, e o descompasso entre o que o texto do delírio promete e o que o código faz.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**
