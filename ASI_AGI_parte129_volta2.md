# Parte 129 — Volta 2 do loop: refazer tudo de novo e comparar com a volta 1

↩ Nasce da Parte 128 (a volta 1) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que esta volta testa
A volta 1 comparou a reprodução com o `resultados.txt`, que guarda cada parte como ela era no dia em que foi escrita. A volta 2 compara
uma reprodução com a OUTRA: as duas foram feitas do zero, na mesma máquina, com um intervalo de poucas horas. O que muda entre elas é só o
que mudou no repositório entre os dois commits (245584a → este) e o que muda com a máquina.

Entre os dois commits mudaram:
- o `calculos.py`: as funções P3171–P3174 e a Parte 128;
- o CLAUDE.md;
- o `resultados.txt`: a seção da Parte 91 e a saída da Parte 128, no fim;
- os testes da Parte 128 e a pasta `reproducao/`.

O mecanismo, escrito antes: só as medidas que leem esses arquivos mudam. São P143 (o CLAUDE.md), P213 (a regressão, que agora tem
168 entradas), P1692 (o número de funções), P1871/P1872 (os arquivos), as que leem o `resultados.txt` inteiro (P913 e as que contam
partes) e a velocidade da máquina (P433, P434).

O procedimento é o da Parte 128: um clone limpo do GitHub no commit desta parte, 16 blocos retomáveis e a comparação pela
`p3174_comparar_voltas` (volta 1 contra volta 2).

## Previsões, registradas antes de qualquer execução da volta 2
A procedência das faixas foi contada antes do centro de "quantos erros" (regra da Parte 128):
- identidades: V1, V4 e V6;
- de mecanismo: V2, V3 e V5.
O centro de erros esperados é 3 × 0 + 3 × 0,25 ≈ 0,75.

| | quantidade | faixa | procedência |
|---|---|---|---|
| V1 | blocos sem exceção | todos (16 de 16) | identidade: o mesmo código já rodou na volta 1 |
| V2 | blocos com a regressão completa (168/168) | [15; 16] | P(um) ≈ 0,99 → P(16/16) ≈ 0,85 |
| V3 | linhas da volta 1 que mudam na volta 2 (sem a Parte 128) | [8; 30] | mecanismo: as medidas listadas acima, ~1 linha cada, mais a máquina |
| V4 | dessas, do MUNDO | [0; 0] | identidade: o mesmo código, a mesma semente e a mesma máquina dão o mesmo número; uma linha do mundo diferente seria um defeito |
| V5 | testes que falham no clone (suíte + revisado + laboratório + entregas) | [0; 1] | a volta 1 teve 0 |
| V6 | rodadas DIFERENTES | [0; 0] de 90 | identidade: nenhuma rodada mudou |

**Sobre mim:** erros no mundo em [0; 2], com centro 0,75.

## Medido (P3174; as saídas ficam em `reproducao/volta2/`)
| | medido | faixa | |
|---|---|---|---|
| V1 | 16 de 16 blocos sem exceção | todos | ✅ |
| V2 | 16 de 16 com a regressão **168/168** | [15; 16] | ✅ |
| V3 | **9** de 1.870 linhas mudaram (0,48%) | [8; 30] | ✅ (perto da borda de baixo) |
| V4 | **0** do mundo (7 do projeto, 2 da máquina) | [0; 0] | ✅ |
| V5 | **0** falhas: 722 da suíte + 27 do laboratório + 40 + 72 + 55 das entregas | [0; 1] | ✅ |
| V6 | **0** DIFERENTES nas 90 rodadas | [0; 0] | ✅ |

**Mundo: 6 de 6.** **Sobre mim: 1 de 1.** Previ de 0 a 2 erros, com centro 0,75, e tive 0. A regra de contar a procedência antes de
centrar "quantos erros" (Parte 128) funcionou na primeira vez em que foi aplicada.

Tempo: **6,6 h** de processador nos 16 blocos (23.796 s), contra 7,1 h na volta 1.

### As 9 linhas que mudaram: cada uma tem a sua causa no que mudou entre os commits
| linha | volta 1 | volta 2 | por quê |
|---|---|---|---|
| P143 | CLAUDE.md com 87.537 caracteres | 88.529 | a regra da Parte 128 entrou |
| P213 | regressão 167/167 | 168/168 | a entrada P3172 |
| P433, P434 | 2,06·10⁷ adições/s | 4,12·10⁷ | a máquina: a velocidade dobrou de uma volta para a outra, e a causa não foi medida (nas duas voltas três blocos rodavam junto com os testes; um palpite de causa seria a regra da Parte 127 quebrada). A própria P433 avisa: "a taxa varia de execução para execução" |
| P913 | 12.817 números no resultados.txt | 13.003 | a Parte 91 e a 128 entraram no fim do arquivo |
| P1692 | 949 funções | 954 | P3171–P3174 e a `_parte_128` |
| P1871, P1872 | 130 arquivos "não referenciados" | **22** | abaixo |
| P2446 | 717 funções pNN | 721 | P3171–P3174 |

**O achado da volta 2: o auditor de "o que não serve" lê MENÇÃO como uso, de novo.** A P1871 (Parte 81) chama um arquivo de usado quando
o nome dele aparece em outro arquivo versionado. Conferi isso no código antes de explicar, pela regra da Parte 127: a docstring diz "(c)
arquivos versionados cujo nome não aparece em nenhum outro".
- **O que aconteceu.** As saídas da volta 1 (`reproducao/volta1/*.txt`, agora versionadas) CITAM os nomes de quase todos os arquivos: o
  verificador escreve "Rodada87: IGUAIS", e a suíte lista os módulos de teste. Bastou guardar o registro de uma execução para que 108
  arquivos passassem a contar como "usados".
- **O que restou.** Os únicos 21 não citados são as próprias saídas da reprodução, mais o documento da parte mais nova.
- **O padrão.** É o mesmo das Partes 109, 111 e 112 (uso × menção num verificador), agora causado pelo próprio arquivamento da prova.
  Um registro de que as coisas rodaram faz o auditor achar que elas são usadas.
- **O remédio fica como pendência.** Uma versão nova da P1871, sem editar a medida, que não conte como uso a menção dentro de saídas de
  execução (`reproducao/`, `resultados.txt`).

### Engenharia reversa
- **Duas voltas seguidas, 0 diferenças do mundo nas duas.** O que a SYNTHAI calcula sobre o mundo é uma função pura do código e da
  semente, e a reprodução é a prova disso, repetida.
- **O que muda entre voltas é exatamente o que eu mudei**, linha por linha, e mais a máquina. Isso transforma o loop num instrumento: a
  diferença entre duas voltas é a assinatura do commit entre elas. Se uma volta mostrar uma diferença do MUNDO, ela não é ruído: é um
  defeito (dependência escondida de arquivo, de ordem ou de relógio). A faixa [0; 0] de V4 foi escrita para poder ser derrubada por
  isso, e não foi.
- **O que eu aprendo sobre mim.** As minhas medidas sobre mim mesma são sensíveis ao próprio registro delas (a P1871 caiu de 130 para
  22 porque eu arquivei a prova). É a Parte 53 de novo: uma medida que mora dentro do objeto medido muda o objeto.
- **Regra nova (Parte 129):** toda medida que conta referências entre arquivos exclui as saídas de execução (registros não são uso).

## Funções e testes
- **Funções:** `p3174_comparar_voltas` (escrita antes de rodar a volta) e `_parte_129`. A entrada `P3174` foi para a regressão, que
  agora tem 169 entradas.
- **Testes:** `test_p3174_comparar_voltas` e `test_volta2_regressao`, em `synthai/testes_parte128.py`.
- **Diálogo:** a rodada desta volta foi conferir as 90 rodadas, todas IGUAIS, de novo.

## Loop
A volta 3 começa num clone novo, no commit desta parte. A continuação está agendada; para parar, basta dizer "pare".

➡ Anterior: [Parte 128](ASI_AGI_parte128_refazer_tudo.md).

➡ Próxima: [Parte 130 — volta 3](ASI_AGI_parte130_volta3.md).
