"""Rodada 55 do diálogo Python <-> Java (Parte 88, pendência da Parte 87): o passo do GRPO com corte (clipping), bit a bit. surrogate = min(r*A, clip(r, 1-eps,
1+eps)*A). Só comparações, × e a função clip (min/max) — nada da libm, então o risco é só a ordem. Vários pares (razão r, vantagem A); imprime o surrogate em
hexadecimal. Rodar da raiz: python3 dialogo/rodada55.py"""

EPS = 0.2
CASOS = [(1.0, 1.0), (1.5, 1.0), (0.5, 1.0), (1.3, -1.0), (0.7, -1.0), (2.0, 0.5), (0.1, -0.5), (1.25, 1.0)]


def clip(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def surrogate(r, a):
    nao_cortado = r * a
    cortado = clip(r, 1.0 - EPS, 1.0 + EPS) * a
    return nao_cortado if nao_cortado < cortado else cortado


def main():
    for i, (r, a) in enumerate(CASOS):
        print(f"caso {i} s {surrogate(r, a).hex()}")
    print("fim")


if __name__ == "__main__":
    main()
