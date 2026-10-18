"""Rodada 83 do diálogo Python <-> Java (Parte 116): a AVALIAÇÃO PAREADA que substitui a avaliação metacognitiva do NEXUS-RAPHAEL v2 recebido.
d = valor − linha de base; t = média(d)/(s_d/√n); 'confirmed' se t > t crítico (2,131847: unilateral 95%, 4 graus de liberdade), 'rejected' se
t < −t crítico. Três hipóteses de 5 experimentos. Só +, −, ×, ÷ e √, somas em laço na mesma ordem. Bit a bit.
Da raiz: python3 dialogo/rodada83.py"""
import math

T_CRITICO = 2.131847
HIPOTESES = [
    ([10.4, 11.2, 9.8, 12.1, 10.9], [10.0, 10.1, 9.9, 10.3, 10.2]),
    ([9.1, 10.7, 8.8, 11.9, 10.2], [10.0, 10.1, 9.9, 10.3, 10.2]),
    ([8.2, 9.0, 8.7, 9.4, 8.1], [10.0, 10.1, 9.9, 10.3, 10.2]),
]


def avaliar(valores, bases):
    n = len(valores)
    d = [v - b for v, b in zip(valores, bases)]
    soma = 0.0
    for x in d:
        soma += x
    media = soma / n
    q = 0.0
    for x in d:
        q += (x - media) * (x - media)
    s = math.sqrt(q / (n - 1))
    t = media / (s / math.sqrt(n))
    if t > T_CRITICO:
        return "confirmed", t
    if t < -T_CRITICO:
        return "rejected", t
    return "inconclusive", t


def main():
    for i, (v, b) in enumerate(HIPOTESES):
        st, t = avaliar(v, b)
        print(f"H{i} t {t.hex()} {st}")
    print("fim")


if __name__ == "__main__":
    main()
