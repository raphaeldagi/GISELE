"""Rodada 58 do diálogo Python <-> Java (Parte 91, pendência da Parte 90): o CORAÇÃO de um passo de treino de GPT — o gradiente da softmax com entropia
cruzada, um passo de SGD e a decisão nova — bit a bit. p = softmax(logits) (exp próprio); perda = −ln p[alvo] (log próprio); gradiente = p − onehot(alvo);
passo: logits -= lr·gradiente; decisão = argmax. Mostra que o treino muda a escolha, e que é idêntico nas duas línguas. Só +, −, ×, ÷ e o exp/log próprios
(a fronteira da Parte 52). Rodar da raiz: python3 dialogo/rodada58.py"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import exp_, log_  # noqa: E402

LR = 0.5
# alguns vetores de logits e o alvo de cada um
CASOS = [([2.0, 1.0, 0.5, 0.0], 2),
         ([0.1, 0.2, 0.3, 0.25], 0),
         ([-1.0, 3.0, 2.0, 2.9], 3),
         ([1.0, 1.0, 1.0, 1.0], 1),
         ([5.0, -2.0, 0.0, 1.0], 1)]


def softmax(logits):
    m = logits[0]
    for x in logits:
        if x > m:
            m = x
    e = [exp_(x - m) for x in logits]
    s = 0.0
    for x in e:
        s = s + x
    return [x / s for x in e]


def passo(logits, alvo):
    p = softmax(logits)
    perda = -log_(p[alvo])
    grad = [p[i] - (1.0 if i == alvo else 0.0) for i in range(len(logits))]
    novo = [logits[i] - LR * grad[i] for i in range(len(logits))]
    p2 = softmax(novo)
    perda2 = -log_(p2[alvo])
    arg = 0
    for i in range(len(novo)):
        if novo[i] > novo[arg]:
            arg = i
    return perda, perda2, arg, novo


def main():
    for c, (logits, alvo) in enumerate(CASOS):
        perda, perda2, arg, novo = passo(logits, alvo)
        print(f"caso {c} perda {perda.hex()} perda2 {perda2.hex()} arg {arg}")
        for i in range(len(novo)):
            print(f"caso {c} w {i} {novo[i].hex()}")
    print("fim")


if __name__ == "__main__":
    main()
