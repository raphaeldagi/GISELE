"""Rodada 90 do diálogo Python <-> Java (Parte 123): o rastreador do erro humano com esquecimento, nas duas formas (encolher para a
priori Beta(2, 18), a da SynthaiLenta; e encolher para zero, a da auditoria recebida), γ = 0,995 e 0,93. Observações de um LCG
(erro quando x/2³¹ < ε), ε = 0,15 por 2.000 observações e depois 0,6; imprime a média a cada 500 e o atraso até cruzar 0,375.
Só +, −, ×, ÷ e comparações. Da raiz: python3 dialogo/rodada90.py"""

SEMENTE = 1231


def rodar(gama, forma):
    x = SEMENTE
    a, b = 2.0, 18.0
    medias = []
    atraso = -1
    for t in range(4000):
        eps = 0.15 if t < 2000 else 0.6
        x = (1103515245 * x + 12345) % 2147483648
        e = 1.0 if x / 2147483648.0 < eps else 0.0
        if forma == 0:
            a = 2.0 + gama * (a + e - 2.0)
            b = 18.0 + gama * (b + (1.0 - e) - 18.0)
        else:
            a = gama * a + e
            b = gama * b + (1.0 - e)
        m = a / (a + b)
        if t >= 2000 and atraso < 0 and m >= 0.375:
            atraso = t - 1999
        if t % 500 == 499:
            medias.append(m)
    return medias, atraso


def main():
    for gama in (0.995, 0.93):
        for forma in (0, 1):
            medias, atraso = rodar(gama, forma)
            print("gama " + str(gama) + " forma " + str(forma) + " atraso " + str(atraso) + " " + " ".join(v.hex() for v in medias))
    print("fim")


if __name__ == "__main__":
    main()
