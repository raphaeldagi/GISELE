"""Rodada 15 do diálogo Python <-> Java: a detecção de mudança no nível do mundo (synthai/decisao.py,
ThompsonBOCPDGlobal, P761). Três braços em rodízio, recompensas do gerador da rodada 5 (semente 1515), médias trocadas no
passo 600 de 1200, risco H = 1/50. Imprime as hipóteses finais (peso, contagens), em hexadecimal, e as observações da mais
pesada. Rodar da raiz do repositório: python3 dialogo/rodada15.py"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402
from synthai.decisao import ThompsonBOCPDGlobal  # noqa: E402


def main():
    g = LCG(1515)
    t = ThompsonBOCPDGlobal(3, random.Random(0), risco=1 / 50, hipoteses=16)
    for passo in range(1200):
        ps = (0.2, 0.5, 0.8) if passo < 600 else (0.8, 0.5, 0.2)
        braco = passo % 3
        t.atualizar(braco, 1 if g.uniforme() < ps[braco] else 0)
    print(f"{len(t.hs)} hipoteses")
    for h in t.hs:
        print(h[0].hex() + " | " + " ".join(x.hex() for x in h[1]) + " | " + " ".join(x.hex() for x in h[2]))
    top = t.hs[0]
    print(f"observacoes da mais pesada = {int(sum(top[1]) + sum(top[2]) - 2 * len(top[1]))}")


if __name__ == "__main__":
    main()
