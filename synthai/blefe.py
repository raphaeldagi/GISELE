"""O blefe: o equilíbrio de indiferença (Parte 105, P2591-P2593). Teoria dos jogos mínima, offline, só biblioteca padrão.

Jogo polarizado meia-rua: pote P (cada um já apostou P/2), aposta B. O apostador tem os nuts (ganha sempre, prob ½) ou ar
(perde sempre, prob ½); o pagador tem um pega-blefe. O apostador sempre aposta os nuts e blefa o ar com frequência b; o
pagador paga com frequência c. O equilíbrio é um ponto de INDIFERENÇA: cada lado joga a mistura que deixa o outro sem poder
melhorar — a forma mais pura da decisão sob informação oculta (Partes 83/84)."""

import random


def alpha_blefe(P=2.0, B=2.0):
    """A fração de BLEFE entre as apostas que deixa o pagador indiferente: α = B/(P+2B) (α(P+B) = (1−α)B)."""
    return B / (P + 2 * B)


def freq_pagar(P=2.0, B=2.0):
    """A frequência de PAGAR (defesa mínima) que deixa o blefe sem lucro: c = P/(P+B) ((1−c)P = cB)."""
    return P / (P + B)


def freq_blefar_o_ar(P=2.0, B=2.0):
    """A frequência com que blefar o ar: de α = b/(1+b) (metade nuts, metade ar), b = α/(1−α)."""
    a = alpha_blefe(P, B)
    return a / (1 - a)


def ev_pagar(alpha, P=2.0, B=2.0):
    """EV de PAGAR uma aposta (relativo a desistir=0): ganha P+B se era blefe, perde B se era valor."""
    return alpha * (P + B) - (1 - alpha) * B


def ev_blefar(c, P=2.0, B=2.0):
    """EV de BLEFAR o ar (relativo a desistir=0): ganha P se o pagador desiste, perde B se paga."""
    return (1 - c) * P - c * B


def indiferenca(P=2.0, B=2.0):
    """No equilíbrio, os dois ficam indiferentes: devolve (|EV(pagar) no α*|, |EV(blefar) no c*|) — ambos ~0."""
    return abs(ev_pagar(alpha_blefe(P, B), P, B)), abs(ev_blefar(freq_pagar(P, B), P, B))


def melhor_resposta_plana(P=2.0, B=2.0, passos=11):
    """No c* do equilíbrio, o EV do ar do apostador é o mesmo para QUALQUER frequência de blefe (reta plana): devolve a
    maior diferença de EV entre blefar sempre e nunca — ~0 (ninguém melhora desviando)."""
    c = freq_pagar(P, B)
    evs = [ (1 - c) * P - c * B for _ in range(passos) ]  # independe de b: o EV do ar é (1-c)P - cB
    return max(evs) - min(evs)


def simular_equilibrio(n=40000, semente=105, P=2.0, B=2.0):
    """Joga o equilíbrio (apostador: nuts sempre aposta, ar blefa com b*; pagador paga com c*) e mede a fração realizada de
    BLEFES entre as apostas (deve ~ α* = 1/3) e a fração de pagamentos (deve ~ c* = 1/2). Devolve (α empírico, c empírico)."""
    r = random.Random(semente)
    b, c = freq_blefar_o_ar(P, B), freq_pagar(P, B)
    apostas, blefes, pagou = 0, 0, 0
    for _ in range(n):
        nuts = r.random() < 0.5
        if nuts:
            apostas += 1
        elif r.random() < b:        # ar: blefa com freq b
            apostas += 1
            blefes += 1
        else:
            continue                # ar desiste: não há aposta
        if r.random() < c:
            pagou += 1
    return (blefes / apostas, pagou / apostas)
