"""Rodada 99 do diálogo Python <-> Java (Parte 151): a geometria exata do braço aleatório de synthai.tabuleiro.paradas_por_comprimento bit a bit.
Recursão em profundidade sobre os caminhos sem repetir casa (vizinhança de rei), PARAR só com `minimo` letras, com `maximo` só PARAR; parcelas p/n
somadas na mesma ordem nos dois lados. Grades 4, 5, 6 e comprimentos (3, 5), (3, 4), (4, 5). Confere contra o módulo (igualdade exata) antes de
imprimir. Da raiz: python3 dialogo/rodada99.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai import tabuleiro  # noqa: E402

CASOS = ((4, 3, 5), (5, 3, 5), (6, 3, 5), (5, 3, 4), (5, 4, 5))


def paradas(tamanho, minimo, maximo):
    out = [0.0] * (maximo + 1)

    def anda(caminho, p):
        L = len(caminho)
        if L >= maximo:
            out[L] += p
            return
        r, c = caminho[-1]
        livres = []
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                if (a or b) and 0 <= r + a < tamanho and 0 <= c + b < tamanho and (r + a, c + b) not in caminho:
                    livres.append((r + a, c + b))
        n = len(livres) + (1 if L >= minimo else 0)
        if n == 0:
            return
        if L >= minimo:
            out[L] += p / n
        for v in livres:
            anda(caminho + [v], p / n)
    for r in range(tamanho):
        for c in range(tamanho):
            anda([(r, c)], 1.0 / (tamanho * tamanho))
    return out


def main():
    for tam, mi, ma in CASOS:
        s = paradas(tam, mi, ma)
        m = tabuleiro.paradas_por_comprimento(tam, mi, ma)
        assert all(s[L] == m[L] for L in m)
        print("g" + str(tam) + "_" + str(mi) + "_" + str(ma) + " " + " ".join(s[L].hex() for L in range(mi, ma + 1)))
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
