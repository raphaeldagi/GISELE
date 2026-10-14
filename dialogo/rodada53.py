"""Rodada 53 do diálogo Python <-> Java (Parte 86): o passo do neurônio de Izhikevich, bit a bit. Só +, −, × e ÷ — nada da libm (Parte 52) —, mas a ORDEM
das operações decide o último bit (Parte 34/85): os dois meios-passos em v e a mesma ordem de somas nas duas línguas. Um neurônio RS (a=0,02, b=0,2,
c=−65, d=8) sob corrente I=10, dt=0,5 ms, 400 passos. Imprime v, u (hex) a cada passo e o total de disparos. Rodar da raiz: python3 dialogo/rodada53.py"""

A, B, C, D, DT, I = 0.02, 0.2, -65.0, 8.0, 0.5, 10.0
PASSOS = 400


def passo(v, u):
    disparo = 0
    v = v + (DT / 2.0) * (0.04 * v * v + 5.0 * v + 140.0 - u + I)
    v = v + (DT / 2.0) * (0.04 * v * v + 5.0 * v + 140.0 - u + I)
    u = u + DT * A * (B * v - u)
    if v >= 30.0:
        v = C
        u = u + D
        disparo = 1
    return v, u, disparo


def main():
    v, u, disparos = C, B * C, 0
    for k in range(PASSOS):
        v, u, d = passo(v, u)
        disparos += d
        print(f"passo {k} v {v.hex()} u {u.hex()}")
    print(f"disparos: {disparos}")


if __name__ == "__main__":
    main()
