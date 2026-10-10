# Como eu construiria uma AGI/ASI — Parte 81 (0x51): o que não serve

> Continuação da [Parte 80](ASI_AGI_parte80_o_valor_de_um_conjunto.md). Pedido do usuário: **"Tire dos nossos trabalhos tudo que não serve pra nada."** Ele contraria a regra antiga "o `calculos.py`
> só cresce; nunca apagar funções antigas", e, por ser o pedido mais recente, vale. O critério, escolhido pela regra mais conservadora (a regra de autonomia) e escrito antes de medir: **sai só o que
> nada usa**, isto é, uma função, classe ou arquivo que nenhum código, teste, rodada ou documento do repositório referencia. **Ficam:** as funções `pNN` (cada número citado nos documentos sai de uma
> delas), os documentos das partes (o registro histórico) e o que for referenciado. Tudo num commit só, reversível pelo git. A mesma mensagem trouxe de novo o relatório do Módulo 007 e o texto do
> Módulo 008 (memória episódica e escore de Brier).

## Previsões sobre as minhas previsões desta parte (num commit só delas)

- **(m1)** o número de previsões do mundo em **[3; 7]**
- **(m2)** o número de faixas que cruzam ou tocam o zero em **[1; 4]** (contagens de código morto podem ser zero)
- **(m3)** a mediana de w das faixas que não cruzam o zero em **[0,10; 0,90]**, ou indefinida
- **(m4)** a fração de acertos do mundo em **[0,40; 1,00]**
- **(m5)** o número de faixas que não cruzam o zero com w > 0,6 em **[0; 4]**
- **(m6)** o número de surpresas em **[0; 3]**

## Previsões sobre mim, antes de escrever

| medida | **eu** | por quê |
|---|---|---|
| caracteres | **[13.039; 22.082]** | o estatístico (até a 71) |
| compressão | **[0,397; 0,422]** | o estatístico |
| testes de unidade | **[1 + S; 4 + S]** | 1 ou 2 funções novas de auditoria |
| testes do placar | **4 + E ± 1** | as letras, mais uma por erro de mecanismo |
| erros do placar | **[0; 3,33]** | o estatístico |
| redundância P821 | **[0,563; 0,651]** | o estatístico |
| previsões unilaterais | **0** | `p974` |
| pNN novas sem teste | **0** | `p1092` |

## Previsões do mundo (antes de medir; sem calibração possível, por isso largas, e com o fator 1,36 já aplicado)

"Referenciado" = o nome aparece, como palavra inteira, em algum outro lugar do repositório (código, testes, rodadas, documentos, `CLAUDE.md`), fora da própria definição.
- **(a)** funções e classes de primeiro nível do `calculos.py` que não são `pNN` e não são referenciadas em lugar nenhum: **[0; 40]**
- **(b)** funções e classes de primeiro nível dos módulos de `synthai/` (fora os testes) não referenciadas fora do próprio arquivo nem dentro dele: **[0; 30]**
- **(c)** arquivos versionados cujo nome não aparece em nenhum outro arquivo versionado: **[0; 8]**
- **(d)** depois de tirar o que (a), (b) e (c) acharem, a suíte inteira de testes e a regressão completa passam como antes (categórica)

**Medido:** (a) **0** ✅; (b) **0** ✅; (c) **83** ❌ pela letra (o nome literal), mas **0** depois de olhar cada um (`p1872`): 34 rodadas que o `verificar.py` acha por `glob`, 24 saídas que a `rodada29.py` abre por
um nome montado, 24 originais em `dialogo/registro/` citadas pela pasta e este documento (ainda não ligado). (d) **não se aplica**: não havia nada a tirar. **Pelo critério escrito antes, nada no
repositório deixa de servir.** O erro da previsão (c) é o terceiro verificador meu, seguido, que acusa defeitos que não existem (o auditor da Parte 72, a `p1638`, e agora a `p1871`): procurar o
nome escrito não acha o uso por padrão.
