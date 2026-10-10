"""Rodada 9 do diálogo Python <-> Java: a média bayesiana de modelos (synthai/decisao.py, ThompsonMistura, P541): quatro
ThompsonBOCPD com H em {0, 1/2000, 1/500, 1/100}, pesos pela soma dos logs das preditivas. Três braços em rodízio,
recompensas do gerador da rodada 5 (semente 909), médias trocadas no passo 600. Imprime os log-pesos, as perdas de cada
modelo e a da mistura, e os pesos normalizados, em hexadecimal. Rodar da raiz: python3 dialogo/rodada09.py"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402
from synthai.decisao import ThompsonMistura  # noqa: E402

g = LCG(909)
t = ThompsonMistura(3, random.Random(0))
for passo in range(1200):
    ps = (0.2, 0.5, 0.8) if passo < 600 else (0.8, 0.5, 0.2)
    braco = passo % 3
    t.atualizar(braco, 1 if g.uniforme() < ps[braco] else 0)
print("logw = " + " ".join(x.hex() for x in t.logw))
print("perda = " + " ".join(x.hex() for x in t.perda))
print("perda da mistura = " + t.perda_mistura.hex())
print("pesos = " + " ".join(x.hex() for x in t.pesos()))
