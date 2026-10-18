"""Rodada 78 do diálogo Python <-> Java (Parte 111): o passo de Q-learning tabular (o coração do word_rl_lab), bit a bit.
Tabela 5 estados × 3 ações; 2.000 transições (s, a, r, s', fim) geradas por um LCG inteiro (sem o random de cada língua);
Q ← Q + α(r + γ·max Q(s′, ·) − Q), com o max por comparação. Só +, −, × e comparação. Da raiz: python3 dialogo/rodada78.py"""

S, A, N = 5, 3, 2000
ALFA, GAMA = 0.2, 0.95


def lcg(x):
    return (x * 1103515245 + 12345) % 2147483648


def treinar():
    q = [[0.0] * A for _ in range(S)]
    x = 78
    for _ in range(N):
        x = lcg(x)
        s = x % S
        x = lcg(x)
        a = x % A
        x = lcg(x)
        r = float(x % 7) - 3.0
        x = lcg(x)
        s2 = x % S
        x = lcg(x)
        fim = (x % 10) == 0
        futuro = 0.0
        if not fim:
            futuro = q[s2][0]
            for b in range(1, A):
                if q[s2][b] > futuro:
                    futuro = q[s2][b]
        q[s][a] = q[s][a] + ALFA * (r + GAMA * futuro - q[s][a])
    return q


def main():
    q = treinar()
    for s in range(S):
        print("q " + str(s) + " " + " ".join(v.hex() for v in q[s]))
    print("fim")


if __name__ == "__main__":
    main()
