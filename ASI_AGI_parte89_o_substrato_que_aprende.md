# Como eu construiria uma AGI/ASI — Parte 89 (0x59): o substrato que aprende

> Continuação da [Parte 88](ASI_AGI_parte88_a_arquitetura_autopoietica_recebida.md). Sem texto novo do usuário: sigo o ciclo (Parte 44/75). A Parte 86 construiu o neurônio pulsado (LIF, Izhikevich) e a regra
> STDP, mas só mediu neurônios isolados. Aqui faço o substrato **aprender**: a STDP não supervisionada muda os pesos, e a pergunta é se ela faz o que a literatura afirma — tornar uma sinapse seletiva à
> correlação — e se o faz no meu regime pequeno (a lição das Partes 84 e 87: um efeito famoso pode não aparecer fora da sua escala, então a conta vem antes).
>
> **A âncora algébrica (Parte 70):** a STDP é Hebb com janela temporal. A deriva esperada de um peso é a integral da janela vezes a correlação pré-pós — uma forma fechada. Começo por ela (que não depende de
> regime), e só depois arrisco o efeito de competição (que depende).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[0; 3]**
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,05; 0,80]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,45; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 3]**
- **(m6)** o número de surpresas em **[0; 3]**
