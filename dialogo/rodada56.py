"""Rodada 56 do diálogo Python <-> Java (Parte 89, pendência das Partes 86/88): uma POPULAÇÃO de neurônios de Izhikevich acoplados, bit a bit. 6 neurônios RS,
acoplados por uma matriz de pesos fixa; a corrente de cada um é a externa mais a soma dos pesos vezes 1 quando o vizinho disparou no passo anterior. Só +, −, ×
(a ordem fixa das somas, Partes 34/85); sem libm. 300 passos de 0,5 ms. Imprime v de cada neurônio por passo e o total de disparos. Rodar da raiz: python3
dialogo/rodada56.py"""

N, PASSOS, DT, I_EXT = 6, 300, 0.5, 5.0
# matriz de acoplamento fixa (pesos pequenos), em ordem de linha
W = [[0.0, 0.3, 0.0, 0.0, 0.2, 0.0],
     [0.0, 0.0, 0.4, 0.0, 0.0, 0.0],
     [0.2, 0.0, 0.0, 0.3, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.5, 0.0],
     [0.0, 0.0, 0.0, 0.0, 0.0, 0.3],
     [0.4, 0.0, 0.0, 0.0, 0.0, 0.0]]


def simular(imprimir=False):
    v = [-65.0] * N
    u = [0.2 * -65.0] * N
    disparou = [0] * N
    total = 0
    for k in range(PASSOS):
        novo_disp = [0] * N
        correntes = []
        for i in range(N):
            acopl = 0.0
            for j in range(N):
                acopl = acopl + W[i][j] * disparou[j]
            correntes.append(I_EXT + acopl)
        for i in range(N):
            ii = correntes[i]
            v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii)
            v[i] = v[i] + (DT / 2.0) * (0.04 * v[i] * v[i] + 5.0 * v[i] + 140.0 - u[i] + ii)
            u[i] = u[i] + DT * 0.02 * (0.2 * v[i] - u[i])
            if v[i] >= 30.0:
                v[i] = -65.0
                u[i] = u[i] + 8.0
                novo_disp[i] = 1
                total = total + 1
        disparou = novo_disp
        if imprimir:
            for i in range(N):
                print(f"passo {k} n {i} v {v[i].hex()}")
    return total


def main():
    total = simular(imprimir=True)
    print(f"disparos: {total}")


if __name__ == "__main__":
    main()
