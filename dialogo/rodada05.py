"""Rodada 5 do diálogo Python <-> Java: a regra de aceitação sem a maldição do vencedor (synthai/rsi.py, _t_pareado: pai e
filho reavaliados JUNTOS nas mesmas sementes novas; aceita se t > 3), alimentada por um gerador congruencial de 64 bits
(constantes do MMIX de Knuth) que as duas linguagens implementam igual. Em Python o inteiro não tem limite e a conta é
mascarada com & (2^64 - 1); em Java o long transborda sozinho, com o mesmo resultado módulo 2^64.
Desde o Python 3.12, sum() de floats usa soma compensada (Neumaier); a contagem de quantos t mudariam com a soma
ingênua sai nas duas linguagens. Rodar da raiz do repositório: python3 dialogo/rodada05.py"""

import hashlib
import os
import sys
from math import sqrt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthai.rsi import _t_pareado  # noqa: E402

MASCARA = (1 << 64) - 1
A, C = 6364136223846793005, 1442695040888963407


class LCG:
    def __init__(self, semente):
        self.x = semente & MASCARA

    def uniforme(self):
        self.x = (A * self.x + C) & MASCARA
        return (self.x >> 11) * 2.0 ** -53

    def normal(self):  # soma de 12 uniformes menos 6, na ordem
        s = 0.0
        for _ in range(12):
            s += self.uniforme()
        return s - 6.0


def t_ingenuo(a, b):
    d = [x - y for x, y in zip(a, b)]
    s = 0.0
    for x in d:
        s += x
    m = s / len(d)
    v = 0.0
    for x in d:
        v += (x - m) * (x - m)  # não (x - m) ** 2: o pow da libm erra o último bit em ~0,08% dos casos (Rodada 5)
    v /= len(d) - 1
    return m / sqrt(v / len(d))


g = LCG(2026)
aceites, ts, mudam = [], [], 0
for ensaio in range(200):
    efeito = (ensaio % 5 - 2) * 10.0
    filho = [efeito + 50.0 * g.normal() for _ in range(10)]
    pai = [50.0 * g.normal() for _ in range(10)]
    t = _t_pareado(filho, pai)
    mudam += t != t_ingenuo(filho, pai)
    ts.append(t)
    aceites.append("1" if t > 3 else "0")
print(f"aceites = {aceites.count('1')} de 200; sha = {hashlib.sha256(''.join(aceites).encode()).hexdigest()}")
print("t[0..4] = " + " ".join(x.hex() for x in ts[:5]))
print(f"maior t = {max(ts).hex()}; menor t = {min(ts).hex()}")
print(f"t que mudariam com a soma ingenua = {mudam}")
