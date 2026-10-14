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

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,392; 0,420]** | o estatístico |
| testes de unidade | **[3 + S; 7 + S]** | a rodada e as medidas da rede |
| testes do placar | **6 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir)

As (b) e (c) foram calibradas num teste de fumaça (semente única do próprio problema determinístico) e PREVEEM a execução canônica; contas de sinal e categóricas não levam o fator 1,36.

- **(a)** a rodada 57 — a rede de Izhikevich acoplada que APRENDE por STDP (pesos mudando pela ordem dos disparos, com o exp próprio) — dá a MESMA trajetória E a mesma matriz de pesos final, bit a bit, em Python e
  Java (categórico: IGUAL). É o teste mais duro: um erro de um bit num peso realimentaria todos os disparos seguintes
- **(b)** a STDP está ativa e é de depressão dominante: a soma dos pesos CAI da inicial (2,6); a variação ΔW_total em **[−0,03; −0,005]** (calibrada na fumaça: −0,018; negativa porque A₋ > A₊)
- **(c)** mesmo com a STDP ativa, em 300 passos o aprendizado é lento demais para mudar o PADRÃO de disparos: a rede que aprende dá o MESMO número de disparos que a rede de pesos fixos da rodada 56 (**12**) (categórico:
  igual, porque ΔW ≈ 0,02 é pequeno demais para cruzar um limiar de disparo)
- **(d)** [o teste da calibração, continuando] o acerto das minhas previsões do mundo das Partes 80–90 em **[0,74; 0,88]**
