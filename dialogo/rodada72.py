"""Rodada 72 do diálogo Python <-> Java (Parte 105): a decisão de equilíbrio do blefe, bit a bit.
O equilíbrio (α = B/(P+2B), c = P/(P+B), b = α/(1−α)) e os EVs de indiferença usam só +, −, ×, ÷ e comparações — nenhuma
transcendental, logo portável por construção (Parte 52). A decisão de agir (apostar/pagar) é sortear contra a frequência com o
acaso DADO DE FORA (uma comparação). Da raiz: python3 dialogo/rodada72.py"""

P = 2.0
B = 2.0
ACASO = [0.10, 0.33, 0.50, 0.67, 0.90]   # o acaso dado de fora (insumo portável)


def equilibrio():
    alpha = B / (P + 2.0 * B)
    c = P / (P + B)
    b = alpha / (1.0 - alpha)
    ev_pagar = alpha * (P + B) - (1.0 - alpha) * B
    ev_blefar = (1.0 - c) * P - c * B
    return alpha, c, b, ev_pagar, ev_blefar


def decisoes(c):
    """Para cada acaso u, pagar sse u < c (1.0 ou 0.0)."""
    return [1.0 if u < c else 0.0 for u in ACASO]


def main():
    alpha, c, b, evp, evb = equilibrio()
    print("alpha " + alpha.hex())
    print("c " + c.hex())
    print("b " + b.hex())
    print("evpagar " + evp.hex())
    print("evblefar " + evb.hex())
    print("decisoes " + " ".join(x.hex() for x in decisoes(c)))
    print("fim")


if __name__ == "__main__":
    main()
