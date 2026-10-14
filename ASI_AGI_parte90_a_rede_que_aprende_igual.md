# Como eu construiria uma AGI/ASI — Parte 90 (0x5A): a rede que aprende igual

> Continuação da [Parte 89](ASI_AGI_parte89_o_substrato_que_aprende.md). Sem texto novo do usuário: sigo o ciclo. A Parte 89 mostrou que a STDP tem deriva de forma fechada e que uma população de Izhikevich
> acoplada é IGUAL bit a bit (rodada 56). A pergunta mais funda desta parte (↩ P2115): quando os PESOS do acoplamento MUDAM pela STDP — isto é, a rede aprende enquanto roda, e a mudança de peso depende de
> tempos de disparo medidos —, a trajetória ainda sai idêntica bit a bit em Python e Java? É o teste mais duro da independência de linguagem: um laço de realimentação onde o erro de um bit num peso se
> propagaria para todos os disparos seguintes.
>
> **A âncora algébrica (Parte 70):** a STDP num par é só +, −, × e exp. Se eu usar o exp próprio (regra da Parte 52) e a mesma ordem de somas (Partes 34/85), a atualização de peso é determinística e idêntica;
> a pergunta é se algum passo esconde uma fronteira (uma divisão, um pow, uma ordem diferente) que só aparece quando os pesos realimentam.

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**
