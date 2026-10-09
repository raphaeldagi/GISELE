"""Rodada 28 do diálogo Python <-> Java: exatidão ou sorte? A partir das contagens de chamadas de exp, log e pow de cada
rodada antiga (dialogo/contagens28.tsv, medidas por dialogo/contar_libm.py), a chance de passar por sorte com outra libm,
P = exp(n_exp ln(1 - 0,0029) + n_log ln(1 - 0,0007)), com o exp e o log próprios da Rodada 26 (só + - x / e escalas exatas).
Rodar da raiz do repositório: python3 dialogo/rodada28.py"""

import importlib.util
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("rodada26", os.path.join(AQUI, "rodada26.py"))
r26 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r26)
TAXA_EXP, TAXA_LOG = 0.0029, 0.0007


def contagens():
    res = []
    for l in open(os.path.join(AQUI, "contagens28.tsv"), encoding="ascii").read().split("\n")[1:]:
        if l:
            r, e, g, p = l.split("\t")
            res.append((r, int(e), int(g), int(p)))
    return res


def chance(n_exp, n_log):
    return r26.exp_(n_exp * r26.log_(1.0 - TAXA_EXP) + n_log * r26.log_(1.0 - TAXA_LOG))


def main():
    sorte = 0
    for r, e, g, p in contagens():
        c = chance(e, g)
        sorte += c < 0.5
        print(f"{r}: exp {e}, log {g}, pow {p}; chance de passar por sorte = {c.hex()}")
    print(f"rodadas com chance < 0,5: {sorte}")


if __name__ == "__main__":
    main()
