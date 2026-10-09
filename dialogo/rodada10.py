"""Rodada 10 do diálogo Python <-> Java: as três lógicas difusas da lógica real diferenciável (synthai/neurossimbolico.py,
P551): Łukasiewicz, Gödel e produto. Para 1000 pares (a, b) do gerador da rodada 5 (semente 1010): a t-norma, a t-conorma,
a implicação e o gradiente da implicação; imprime as somas (com o sum() do Python) e a satisfação média de cada lógica, e
os valores no primeiro par, em hexadecimal. Rodar da raiz do repositório: python3 dialogo/rodada10.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402
from synthai.neurossimbolico import LOGICAS, gradiente_implicacao, satisfacao  # noqa: E402

g = LCG(1010)
pares = [(g.uniforme(), g.uniforme()) for _ in range(1000)]
for nome in ("lukasiewicz", "godel", "produto"):
    T, S, I = LOGICAS[nome]
    a, b = pares[0]
    ga, gb = gradiente_implicacao(nome, a, b)
    print(f"{nome} par 0: T = {T(a, b).hex()} S = {S(a, b).hex()} I = {I(a, b).hex()} dI = {ga.hex()} {gb.hex()}")
    somaT = sum(T(x, y) for x, y in pares)
    somaS = sum(S(x, y) for x, y in pares)
    grads = [gradiente_implicacao(nome, x, y) for x, y in pares]
    print(f"{nome} somas: T = {somaT.hex()} S = {somaS.hex()} dIa = {sum(x for x, _ in grads).hex()} dIb = {sum(y for _, y in grads).hex()}")
    print(f"{nome} satisfacao = {satisfacao(nome, pares).hex()}")
