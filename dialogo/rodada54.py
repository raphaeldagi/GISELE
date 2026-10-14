"""Rodada 54 do diálogo Python <-> Java (Parte 87): a vantagem normalizada do GRPO, bit a bit. Â_i = (r_i − média)/(desvio populacional). Só +, −, ×, ÷ e
√ — e √ o IEEE 754 arredonda corretamente (Parte 52), então o risco é só a ordem das somas (Partes 34/85): a média e a variância somadas na mesma ordem nas
duas línguas. Vários grupos de recompensas; imprime cada vantagem em hexadecimal. Rodar da raiz: python3 dialogo/rodada54.py"""

import math

GRUPOS = [[5.0, 2.0], [1.0, 2.0, 3.0, 4.0], [0.5, 0.5, 0.5], [10.0, -3.0, 7.0, 0.0, 2.5], [1.0, 1.0, 1.0, 9.0]]


def vantagens(rs):
    g = len(rs)
    soma = 0.0
    for r in rs:
        soma = soma + r
    media = soma / g
    sq = 0.0
    for r in rs:
        sq = sq + (r - media) * (r - media)
    desvio = math.sqrt(sq / g)
    return [(r - media) / (desvio + 1e-8) for r in rs]


def main():
    for gi, rs in enumerate(GRUPOS):
        for vi, a in enumerate(vantagens(rs)):
            print(f"grupo {gi} i {vi} A {a.hex()}")
    print("fim")


if __name__ == "__main__":
    main()
