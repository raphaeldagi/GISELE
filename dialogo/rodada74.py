"""Rodada 74 do diálogo Python <-> Java (Parte 107): a indução reversa (iteração de valor, horizonte 2), bit a bit.
V[0]=0; V[h][s] = maxₐ (r(s,a) + V[h-1][T(s,a)]). Só +, max e comparações — nenhuma transcendental, portável por construção
(a recursão entre as ruas NÃO cria fronteira, como o MPC da Parte 93). Da raiz: python3 dialogo/rodada74.py"""

ESTADOS = ("A", "B")
ACOES = (0, 1)
R = {("A", 0): 1.0, ("A", 1): 0.0, ("B", 0): 0.0, ("B", 1): 3.0}
T = {("A", 0): "A", ("A", 1): "B", ("B", 0): "A", ("B", 1): "B"}


def iteracao(horizonte=2):
    V = [{s: 0.0 for s in ESTADOS}]
    for _ in range(horizonte):
        Va = V[-1]
        novo = {}
        for s in ESTADOS:
            melhor = R[(s, 0)] + Va[T[(s, 0)]]
            for a in ACOES[1:]:
                cand = R[(s, a)] + Va[T[(s, a)]]
                if cand > melhor:
                    melhor = cand
            novo[s] = melhor
        V.append(novo)
    return V


def main():
    V = iteracao(2)
    print("V1 " + V[1]["A"].hex() + " " + V[1]["B"].hex())
    print("V2 " + V[2]["A"].hex() + " " + V[2]["B"].hex())
    print("fim")


if __name__ == "__main__":
    main()
