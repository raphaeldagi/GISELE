"""Rodada 14 do diálogo Python <-> Java: os trigramas de letras que mais carregam significado (P732): o log da razão de
chances (Laplace) de cada trigrama do lema entre 4017 animais e 4017 outros substantivos. Com `--preparar PASTA`, escreve
PASTA/formas14.txt (rótulo TAB lema), que o Java lê. Rodar da raiz do repositório: python3 dialogo/rodada14.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calculos  # noqa: E402


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "formas14.txt"), "w", encoding="utf-8") as f:
            for lema, y in calculos._formas_732():
                f.write(f"{y}\t{lema}\n")
        return
    animais, outros, dae, ae, v = calculos.p732_trigramas()
    from math import log  # noqa: F401  (os pesos vêm de calculos.p732_trigramas)
    print(f"trigramas distintos = {v}; dae = {dae.hex()}; ae$ = {ae.hex()}")
    print("mais animais: " + " ".join(animais))
    print("menos animais: " + " ".join(outros))


if __name__ == "__main__":
    main()
