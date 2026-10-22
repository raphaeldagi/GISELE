# Parte 130 — Volta 3 do loop

↩ Nasce da Parte 129 (a volta 2) e do pedido "Repita sempre tudo que fizemos. Loop infinito."

## O que esta volta testa
É a terceira repetição de tudo: um clone limpo, as 125 partes, todos os testes e as 90 rodadas. Ela é lançada por um script só,
`reproducao/nova_volta.sh`, para que cada volta seja feita do mesmo jeito. A comparação é volta 2 contra volta 3 (`p3174_comparar_voltas`).

Entre os commits 1c15dda (volta 2) e o desta parte mudaram:
- o `calculos.py`: a `_parte_129` e a entrada de regressão P3174;
- o CLAUDE.md, o `resultados.txt` (com a saída da Parte 129) e os testes;
- `reproducao/volta2/` (22 arquivos) e `reproducao/nova_volta.sh`.

O mecanismo vem da tabela da Parte 129. Cada mudança acima mexe numa medida conhecida:
- **P143:** o CLAUDE.md cresceu;
- **P213:** a regressão passa de 168/168 para 169/169;
- **P913:** o `resultados.txt` cresceu;
- **P1692:** uma função a mais, a `_parte_129`;
- **P1871 e P1872:** os arquivos não citados. Pela leitura de menção da Parte 129, eram 22 na volta 2. Agora entram os 22 arquivos da
  volta 2, dos quais se espera que 21 fiquem sem citação, como aconteceu com os da volta 1, mais o `nova_volta.sh`, que nenhum arquivo
  versionado cita. A conta: 22 + 21 + 1 = 44;
- **P433 e P434:** a máquina;
- **P2446:** não deve mudar, porque não há pNN nova (a `_parte_129` não é pNN).

## Previsões, registradas antes de lançar a volta
Antes do centro de "quantos erros", contei a procedência das faixas (regra da Parte 128):
- identidades: W1, W4, W6;
- conta: W7, com uma cauda de ±2 para os arquivos que eu não li um a um;
- mecanismo: W2, W3, W5.

O centro de erros esperado é 0,10 + 3 × 0,25 ≈ 0,85.

| | quantidade | faixa | procedência |
|---|---|---|---|
| W1 | blocos sem exceção | todos | identidade |
| W2 | blocos com a regressão 169/169 | [15; 16] de 16 | P(16/16) ≈ 0,85 |
| W3 | linhas da volta 2 que mudam na volta 3 (sem as Partes 128 e 129) | [5; 12] | mecanismo: as 6 a 8 medidas listadas acima |
| W4 | dessas, do mundo | [0; 0] | identidade |
| W5 | testes que falham | [0; 1] | as voltas 1 e 2 tiveram 0 |
| W6 | rodadas DIFERENTES | [0; 0] de 90 | identidade |
| W7 | P1871: arquivos "não referenciados" | [42; 46] | conta 22 + 21 + 1 = 44 |

**Sobre mim:** erros no mundo em [0; 2], com centro 0,85.
