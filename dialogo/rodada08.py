"""Rodada 8 do diálogo Python <-> Java: a atualização da ThompsonBOCPD (synthai/decisao.py, P531): mistura de hipóteses
[peso, a, b] por braço, risco H = 1/50 por passo, preditiva Beta, as 16 hipóteses de maior peso. Três braços em rodízio,
recompensas do gerador da rodada 5 (semente 808), médias trocadas no passo 600. Imprime, no fim, as hipóteses de cada
braço (peso, a, b) em hexadecimal. Rodar da raiz do repositório: python3 dialogo/rodada08.py"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402
from synthai.decisao import ThompsonBOCPD  # noqa: E402

g = LCG(808)
t = ThompsonBOCPD(3, random.Random(0), risco=1 / 50, hipoteses=16)
for passo in range(1200):
    ps = (0.2, 0.5, 0.8) if passo < 600 else (0.8, 0.5, 0.2)
    braco = passo % 3
    t.atualizar(braco, 1 if g.uniforme() < ps[braco] else 0)
for i, hs in enumerate(t.mist):
    print(f"braco {i}: {len(hs)} hipoteses")
    for h in hs:
        print("  " + " ".join(x.hex() for x in h))
