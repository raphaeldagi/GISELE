"""Rodada 14 do diálogo Python <-> Java (Parte 77: os pesos com o log_ próprio, nas duas línguas; a original em dialogo/registro/): os trigramas de letras que mais carregam significado (P732): o log da razão de
chances (Laplace) de cada trigrama do lema entre 4017 animais e 4017 outros substantivos. Com `--preparar PASTA`, escreve
PASTA/formas14.txt (rótulo TAB lema), que o Java lê. Rodar da raiz do repositório: python3 dialogo/rodada14.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calculos  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import log_  # noqa: E402


def trigramas(minimo=10, topo=12):
    """A conta da calculos.p732_trigramas (que fica intacta, porque é medida), aqui com o log_ próprio (Parte 77: a fronteira da Parte 52)."""
    from synthai.semiotica import trigramas_de_forma
    ca, co = {}, {}
    for lema, y in calculos._formas_732():
        for t in trigramas_de_forma(lema):
            (ca if y else co)[t] = (ca if y else co).get(t, 0) + 1
    voc = set(ca) | set(co)
    na, no = sum(ca.values()), sum(co.values())
    v = len(voc)
    peso = {t: log_((ca.get(t, 0) + 1) / (na + v)) - log_((co.get(t, 0) + 1) / (no + v)) for t in voc}
    ok = [t for t in voc if ca.get(t, 0) + co.get(t, 0) >= minimo]
    ok.sort(key=lambda t: (-peso[t], t))
    return ok[:topo], ok[::-1][:topo], peso.get("dae"), peso.get("ae$"), len(voc)


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "formas14.txt"), "w", encoding="utf-8") as f:
            for lema, y in calculos._formas_732():
                f.write(f"{y}\t{lema}\n")
        return
    animais, outros, dae, ae, v = trigramas()
    print(f"trigramas distintos = {v}; dae = {dae.hex()}; ae$ = {ae.hex()}")
    print("mais animais: " + " ".join(animais))
    print("menos animais: " + " ".join(outros))


if __name__ == "__main__":
    main()
