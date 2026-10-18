"""Rodada 76 do diálogo Python <-> Java (Parte 109): o valor EXATO do Kuhn simplificado do NEXUS-RAPHAEL, bit a bit.
Enumeração das 6 distribuições equiprováveis (p0, p1 distintos de {1,2,3}) para a probabilidade de apostar com Q em 0, 0,1, ..., 1,
e o melhor valor da grade (argmax). Só +, −, ×, ÷ e comparações, numa ordem fixa de somas — nenhuma transcendental (Parte 52).
Da raiz: python3 dialogo/rodada76.py"""


def valor_kuhn(pa_q):
    tot = 0.0
    for p0 in (1, 2, 3):
        for p1 in (1, 2, 3):
            if p0 == p1:
                continue
            if p0 == 3:
                pa = 1.0
            elif p0 == 2:
                pa = pa_q
            else:
                pa = 0.0
            if p1 >= 2:
                apostou = 2.0 if p0 > p1 else -2.0
            else:
                apostou = 1.0
            tot = tot + (pa * apostou + (1.0 - pa) * (-1.0)) / 6.0
    return tot


def main():
    melhor_k, melhor_v = 0, valor_kuhn(0.0)
    for k in range(11):
        v = valor_kuhn(k / 10.0)
        print("pa " + str(k) + " " + v.hex())
        if v > melhor_v:
            melhor_k, melhor_v = k, v
    print("melhor " + str(melhor_k) + " " + melhor_v.hex())
    print("fim")


if __name__ == "__main__":
    main()
