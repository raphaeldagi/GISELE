"""Rodada 16 do diálogo Python <-> Java: a decisão pela hipótese mais pesada no nível do mundo (synthai/decisao.py,
ThompsonBOCPDGlobalMAP, P791). O mesmo teste da rodada 15 (três braços em rodízio, gerador da rodada 5 com semente 1616,
troca no passo 600 de 1200, H = 1/50): o passo da virada (a primeira vez, depois da troca, em que a hipótese mais pesada
nasceu depois dela) e as três hipóteses mais pesadas no fim. Rodar da raiz do repositório: python3 dialogo/rodada16.py"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402
from synthai.decisao import ThompsonBOCPDGlobalMAP  # noqa: E402


def main():
    g = LCG(1616)
    t = ThompsonBOCPDGlobalMAP(3, random.Random(0), risco=1 / 50, hipoteses=16)
    virada = None
    for passo in range(1200):
        ps = (0.2, 0.5, 0.8) if passo < 600 else (0.8, 0.5, 0.2)
        braco = passo % 3
        t.atualizar(braco, 1 if g.uniforme() < ps[braco] else 0)
        top = max(t.hs, key=lambda h: h[0])
        obs = int(sum(top[1]) + sum(top[2]) - 6)
        if virada is None and passo >= 600 and obs <= passo - 599:
            virada = passo
    print(f"virada no passo {virada}")
    for h in t.hs[:3]:
        print(h[0].hex() + " | " + " ".join(x.hex() for x in h[1]) + " | " + " ".join(x.hex() for x in h[2]))


if __name__ == "__main__":
    main()
