"""Rodada 100 do diálogo Python <-> Java (Parte 152; a centésima): a tabela do colapso de synthai.tabuleiro.tabela_colapso bit a bit. Para n = 1..8
vizinhas com letras iid (frequências do inglês, LETTER_FREQ, em ordem alfabética), a distribuição do número K de letras distintas e de (K, c presente) por
programação dinâmica sobre as letras, numa matriz [t][k] percorrida em ordem fixa, com p^m por multiplicação repetida e m! exato; daí P(parar | n) =
E[1/(K+1)], P(c | n) = E[1{c}/(K+1)] e, sem PARAR, E[1{c}/K]. Antes de imprimir, confere contra o módulo a menos de 1e-12. Da raiz: python3 dialogo/rodada100.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai import palavras_rl, tabuleiro  # noqa: E402

LETRAS = sorted(palavras_rl.LETTER_FREQ)


def potencia(x, m):
    r = 1.0
    for _ in range(m):
        r = r * x
    return r


def dp(p, n, forcar, fat):
    est = [[0.0] * (n + 1) for _ in range(n + 1)]
    est[0][0] = 1.0
    for i in range(len(p)):
        novo = [[0.0] * (n + 1) for _ in range(n + 1)]
        for t in range(n + 1):
            for k in range(n + 1):
                w = est[t][k]
                if w == 0.0:
                    continue
                inicio = 1 if i == forcar else 0
                for m in range(inicio, n - t + 1):
                    novo[t + m][k + (1 if m else 0)] += w * potencia(p[i], m) / fat[m]
        est = novo
    return [fat[n] * est[n][k] for k in range(n + 1)]


def main():
    tot = 0.0
    for c in LETRAS:
        tot += palavras_rl.LETTER_FREQ[c]
    p = [palavras_rl.LETTER_FREQ[c] / tot for c in LETRAS]
    fat = [1.0]
    for m in range(1, 9):
        fat.append(fat[-1] * m)
    mod = tabuleiro.tabela_colapso(palavras_rl.LETTER_FREQ)
    for n in range(1, 9):
        dist = dp(p, n, -1, fat)
        parar = 0.0
        for k in range(1, n + 1):
            parar += dist[k] / (k + 1)
        assert abs(parar - mod[n][0]) < 1e-12
        linha = ["n" + str(n), parar.hex()]
        for i, c in enumerate(LETRAS):
            cc = dp(p, n, i, fat)
            com, sem = 0.0, 0.0
            for k in range(1, n + 1):
                com += cc[k] / (k + 1)
                sem += cc[k] / k
            assert abs(com - mod[n][1][c]) < 1e-12 and abs(sem - mod[n][2][c]) < 1e-12
            linha.append(com.hex())
            linha.append(sem.hex())
        print(" ".join(linha))
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
