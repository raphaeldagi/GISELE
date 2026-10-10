"""Rodada 32 do diálogo Python <-> Java: a primeira diferença no dicionário português. Os lemas portugueses de uma palavra só
(OpenWordNet-PT), em ordem de pontos de código: a posição média (1 = a primeira letra) da primeira letra diferente entre vizinhos
(se um é prefixo do outro, a posição é o tamanho do menor + 1), e quantos pares de vizinhos ficam invertidos pela chave portuguesa
(sem acentos pela NFD e minúscula; depois a original). Com `--preparar PASTA` escreve PASTA/lemas32.txt, que o Java lê.
Rodar da raiz do repositório: python3 dialogo/rodada32.py"""

import os
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)


def lemas():
    from synthai.dicionario import DicionarioPT
    pt = DicionarioPT()
    return sorted({w for ls in pt.lemas.values() for w in ls if w.isalpha()})


def chave_pt(w):
    t = unicodedata.normalize("NFD", w)
    return "".join(c for c in t if not unicodedata.category(c).startswith("M")).lower()


def medir(ws):
    """(soma das posições da primeira diferença, pares de vizinhos, inversões pela chave portuguesa)."""
    soma, inv = 0, 0
    for a, b in zip(ws, ws[1:]):
        k = 0
        while k < len(a) and k < len(b) and a[k] == b[k]:
            k += 1
        soma += k + 1
        if (chave_pt(a), a) > (chave_pt(b), b):
            inv += 1
    return soma, len(ws) - 1, inv


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "lemas32.txt"), "w", encoding="utf-8") as f:
            for w in lemas():
                f.write(w + "\n")
        return
    if len(sys.argv) == 2:
        ws = [l for l in open(os.path.join(sys.argv[1], "lemas32.txt"), encoding="utf-8").read().split("\n") if l]
    else:
        ws = lemas()
    soma, pares, inv = medir(ws)
    print(f"lemas: {len(ws)}; pares de vizinhos: {pares}")
    print(f"posicao media da primeira diferenca = {(soma / pares).hex()} (soma {soma})")
    print(f"pares invertidos pela ordem portuguesa: {inv}")


if __name__ == "__main__":
    main()
