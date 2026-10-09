"""Rodada 7 do diálogo Python <-> Java: o detector de surpresa (synthai/decisao.py, ThompsonSurpresa.atualizar, P491).
Três braços em rodízio (sem amostragem, para que o acaso seja só o das recompensas), recompensas do gerador congruencial
da rodada 5; no passo 600 as médias trocam: (0,2; 0,5; 0,8) -> (0,8; 0,5; 0,2). Imprime os passos e os braços renovados
e as crenças finais em hexadecimal. Rodar da raiz do repositório: python3 dialogo/rodada07.py"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rodada05 import LCG  # noqa: E402  (o mesmo gerador da rodada 5)
from synthai.decisao import ThompsonSurpresa  # noqa: E402

g = LCG(707)
t = ThompsonSurpresa(3, random.Random(0), janela=20, z=3.0)
eventos = []
for passo in range(1200):
    ps = (0.2, 0.5, 0.8) if passo < 600 else (0.8, 0.5, 0.2)
    braco = passo % 3
    antes = t.renovacoes
    t.atualizar(braco, 1 if g.uniforme() < ps[braco] else 0)
    if t.renovacoes > antes:
        eventos.append(f"{passo}:{braco}")
print(f"renovacoes = {t.renovacoes}")
print("eventos = " + " ".join(eventos))
print("a = " + " ".join(x.hex() for x in t.a))
print("b = " + " ".join(x.hex() for x in t.b))
