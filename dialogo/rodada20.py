"""Rodada 20 do diálogo Python <-> Java: o Naive Bayes da Parte 34 (synthai.dicionario.NaiveBayesContagens) reconhece a
época de cada seção do resultados.txt (Partes 1-20 = 1; 21-41 = 2), deixando uma de fora? As palavras são as da Rodada 19,
com repetição. Com `--preparar PASTA`, escreve PASTA/secoes20.txt (parte TAB época TAB palavras separadas por espaço), que
o Java lê. Rodar da raiz do repositório: python3 dialogo/rodada20.py"""

import importlib.util
import os
import sys
import unicodedata
from math import log

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
from synthai.dicionario import NaiveBayesContagens  # noqa: E402

_spec = importlib.util.spec_from_file_location("rodada19", os.path.join(AQUI, "rodada19.py"))
r19 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r19)


def palavras(texto):
    t = unicodedata.normalize("NFD", r19.ROTULO.sub(" ", texto))
    t = "".join(c for c in t if not unicodedata.category(c).startswith("M")).lower()
    return r19.PALAVRA.findall(t)


def dados():
    docs, sec = r19.documentos(), r19.secoes()
    return [(n, 1 if n <= 20 else 2, palavras(sec[n])) for n in sorted(k for k in docs if k in sec)]


def escore(nb, cl, ps):
    """O escore de uma classe, como em NaiveBayesContagens.prever."""
    n = sum(nb.ncls.values())
    v = len(nb.vocab) or 1
    sc = log(nb.ncls[cl] / n)
    c, t = nb.cont[cl], nb.total[cl]
    for w in ps:
        sc += log((c.get(w, 0) + nb.alfa) / (t + nb.alfa * v))
    return sc


def deixar_um_de_fora(ds):
    res = []
    for i, (n, ep, ps) in enumerate(ds):
        nb = NaiveBayesContagens()
        for j, (_, ep2, ps2) in enumerate(ds):
            if j != i:
                nb.aprender(ps2, ep2)
        res.append((n, ep, nb.prever(ps), escore(nb, 1, ps) - escore(nb, 2, ps)))
    return res


def main():
    ds = dados()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "secoes20.txt"), "w", encoding="ascii") as f:
            for n, ep, ps in ds:
                f.write(f"{n}\t{ep}\t{' '.join(ps)}\n")
        return
    acertos = 0
    for n, ep, prev, dif in deixar_um_de_fora(ds):
        acertos += ep == prev
        print(f"parte {n}: epoca {ep}; prevista {prev}; escore(1) - escore(2) = {dif.hex()}")
    print(f"acertos: {acertos}")


if __name__ == "__main__":
    main()
