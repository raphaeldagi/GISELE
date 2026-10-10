"""Rodada 33 do diálogo Python <-> Java: o nome próprio e a palavra comum. Dos lemas portugueses de uma palavra só que começam
com maiúscula, quantos têm uma irmã com a mesma grafia em minúsculas (a cadeia inteira em minúsculas igual a outro lema)?
Com `--preparar PASTA` escreve PASTA/lemas33.txt, que o Java lê. Rodar da raiz do repositório: python3 dialogo/rodada33.py"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)


def lemas():
    from synthai.dicionario import DicionarioPT
    pt = DicionarioPT()
    return sorted({w for ls in pt.lemas.values() for w in ls if w.isalpha()})


def irmas(ws):
    """(com maiúscula, com irmã minúscula, exemplos ordenados)."""
    conj = set(ws)
    mai = [w for w in ws if w[0].isupper()]
    com = [w for w in mai if w.lower() in conj and w.lower() != w]
    return len(mai), len(com), com[:12]


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "lemas33.txt"), "w", encoding="utf-8") as f:
            for w in lemas():
                f.write(w + "\n")
        return
    if len(sys.argv) == 2:
        ws = [l for l in open(os.path.join(sys.argv[1], "lemas33.txt"), encoding="utf-8").read().split("\n") if l]
    else:
        ws = lemas()
    n, k, ex = irmas(ws)
    print(f"com maiuscula: {n}; com irma minuscula: {k}; fracao = {(k / n).hex()}")
    print("exemplos: " + " ".join(ex))


if __name__ == "__main__":
    main()
