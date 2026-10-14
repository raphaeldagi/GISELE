"""Rodada 60 do diálogo Python <-> Java (Parte 93): a decisão do MPC — rollout no modelo de mundo aprendido e argmin do custo
sobre um conjunto FIXO de sequências de ação — bit a bit. O ponto: planejar/controlar NÃO cria fronteira entre as línguas
(Parte 52); a dinâmica (s' = A s + B a), o custo (distância² + velocidade² + λ·a²) e o argmin usam só + − × e comparações, todos
exatos no IEEE 754. Sem exp/log/pow, sem sorteio (o conjunto de candidatos é determinístico, para a tradução ser bit a bit).
Rodar da raiz: python3 dialogo/rodada60.py"""

# Modelo (num mundo linear, os minimos quadrados recuperam A, B exatamente: uso os coeficientes verdadeiros).
A = [[1.0, 0.15], [0.0, 0.9]]
B = [[0.0], [0.15]]
ALVO = 1.0
PESO_ACAO = 0.05
S0 = (-1.5, 0.3)

# Conjunto determinista de sequencias de acao (horizonte 4): a nula e 8 rampas/degraus fixos.
CANDIDATOS = [
    [0.0, 0.0, 0.0, 0.0],
    [1.0, 1.0, 1.0, 1.0],
    [0.5, 0.5, 0.5, 0.5],
    [1.0, 0.5, 0.25, 0.0],
    [0.25, 0.5, 0.75, 1.0],
    [-1.0, -1.0, -1.0, -1.0],
    [0.75, 0.25, -0.25, -0.75],
    [1.0, 0.0, -1.0, 0.0],
    [0.3, 0.6, 0.3, 0.6],
]


def transicao(s, a):
    s0, s1 = s
    n0 = A[0][0] * s0 + A[0][1] * s1 + B[0][0] * a
    n1 = A[1][0] * s0 + A[1][1] * s1 + B[1][0] * a
    return (n0, n1)


def custo(s0, acoes):
    s = s0
    c = 0.0
    for a in acoes:
        s = transicao(s, a)
        c = c + (s[0] - ALVO) * (s[0] - ALVO) + s[1] * s[1]
    for a in acoes:
        c = c + PESO_ACAO * a * a
    return c


def mpc():
    melhor = 0
    melhor_c = custo(S0, CANDIDATOS[0])
    custos = [melhor_c]
    for k in range(1, len(CANDIDATOS)):
        ck = custo(S0, CANDIDATOS[k])
        custos.append(ck)
        if ck < melhor_c:
            melhor_c = ck
            melhor = k
    return melhor, melhor_c, custos


def main():
    melhor, melhor_c, custos = mpc()
    for k in range(len(custos)):
        print(f"candidato {k} custo {custos[k].hex()}")
    print(f"melhor {melhor} primeira_acao {CANDIDATOS[melhor][0].hex()}")
    print(f"custo_otimo {melhor_c.hex()}")
    print("fim")


if __name__ == "__main__":
    main()
