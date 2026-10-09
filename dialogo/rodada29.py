"""Rodada 29 do diálogo Python <-> Java: o ulp que chega à saída. Para cada rodada antiga que chama exp ou log, a saída normal
e a saída com cada exp e log deslocado de um ulp (dialogo/perturbar_libm.py, semente 29) estão em dialogo/saidas29/. Para cada
par: quantos números hexadecimais, a maior mudança relativa |u − v|/|u| e se o texto fora dos números mudou.
Rodar da raiz do repositório: python3 dialogo/rodada29.py"""

import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
HEX = re.compile(r"-?0x[0-9a-fA-F]+(?:\.[0-9a-fA-F]*)?p[+-]?[0-9]+")
RODADAS = ["06", "09", "14", "18", "19", "20", "21", "22", "23", "24", "25", "26"]


def comparar(a, b):
    la, lb = a.split("\n"), b.split("\n")
    texto = len(la) != len(lb)
    n, m = 0, 0.0
    for x, y in zip(la, lb):
        if HEX.sub("#", x) != HEX.sub("#", y):
            texto = True
        for u, v in zip(HEX.findall(x), HEX.findall(y)):
            u, v = float.fromhex(u), float.fromhex(v)
            n += 1
            if u != v:
                r = abs(u - v) / abs(u)
                if r > m:
                    m = r
    return n, m, texto


def main():
    for r in RODADAS:
        a = open(os.path.join(AQUI, "saidas29", f"normal{r}.txt"), encoding="utf-8").read()
        b = open(os.path.join(AQUI, "saidas29", f"perturbada{r}.txt"), encoding="utf-8").read()
        n, m, t = comparar(a, b)
        print(f"rodada{r}: {n} numeros; maior mudanca relativa = {m.hex()}; texto {'mudou' if t else 'igual'}")


if __name__ == "__main__":
    main()
