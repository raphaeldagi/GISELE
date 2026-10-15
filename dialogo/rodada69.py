"""Rodada 69 do diálogo Python <-> Java (Parte 102): o beam search (busca em feixe), bit a bit.
A cada um de T passos, cada hipótese do feixe é estendida por cada token; o escore é a SOMA das log-probabilidades (log próprio) dos
tokens; mantêm-se os k melhores por comparação. Ao fim, imprime a melhor sequência e o seu escore. O exp (softmax) e o log são a única
fronteira (Parte 52); somar e ordenar é exato. Logits fixos por passo (determinístico). Rodar da raiz: python3 dialogo/rodada69.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_, log_  # noqa: E402

K = 3
# logits por passo (T=4 passos, V=4 tokens)
PASSOS = [
    [2.0, 1.0, 0.5, 0.0],
    [0.2, 1.5, 0.3, 0.9],
    [1.1, 0.4, 2.2, 0.1],
    [0.7, 0.6, 0.5, 1.9],
]


def logprobs(logits):
    m = logits[0]
    for x in logits:
        if x > m:
            m = x
    e = [exp_(x - m) for x in logits]
    s = 0.0
    for x in e:
        s = s + x
    ls = log_(s)
    return [(logits[i] - m) - ls for i in range(len(logits))]   # log softmax = (z-m) - log(sum e)


def beam():
    """Devolve (melhor sequencia, escore). Feixe de largura K sobre T passos."""
    feixe = [([], 0.0)]   # (sequencia, escore acumulado)
    for passo in PASSOS:
        lp = logprobs(passo)
        cand = []
        for seq, sc in feixe:
            for tok in range(len(passo)):
                cand.append((seq + [tok], sc + lp[tok]))
        # ordena por escore decrescente (desempate estavel pela ordem de geracao)
        cand.sort(key=lambda t: -t[1])
        feixe = cand[:K]
    return feixe[0]


def main():
    seq, sc = beam()
    print(f"melhor {' '.join(str(t) for t in seq)}")
    print(f"escore {sc.hex()}")
    print("fim")


if __name__ == "__main__":
    main()
