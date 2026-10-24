"""Rodada 98 do diálogo Python <-> Java (Parte 150): a densidade de palavras de synthai.tabuleiro bit a bit. Uma lista fixa de 40 palavras
portuguesas; as frequências das letras A a Z contadas nela (em %, piso 0,01, total em laço na ordem do alfabeto) e a densidade
D = Σ_w Π_c p(c) das palavras de 3 a 5 letras, com essas frequências e com as do inglês (LETTER_FREQ). Só + × ÷ em laço (o sum() do Python 3.12 é
compensado, Parte 34). Antes de imprimir, confere que as duas D ficam a menos de 1e-15 (relativo) das do módulo. Da raiz: python3 dialogo/rodada98.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai import palavras_rl, tabuleiro  # noqa: E402

PALAVRAS = ("casa mesa rio mar sol lua dia noite agua terra fogo vento pedra arvore flor fruta pao leite vinho sal "
            "amor medo raiva paz guerra vida morte tempo hora ano mes semana boca olho mao pe dedo nariz cabelo dente").split()
ALFA = [chr(65 + i) for i in range(26)]


def frequencias(palavras):
    cont = {c: 0 for c in ALFA}
    for w in palavras:
        for ch in w.upper():
            if ch in cont:
                cont[ch] += 1
    total = 0
    for c in ALFA:
        total += cont[c]
    out = {}
    for c in ALFA:
        v = 100.0 * cont[c] / total
        out[c] = v if v > 0.01 else 0.01
    return out


def densidade(palavras, freq):
    t = 0.0
    for c in ALFA:
        t += freq[c]
    d = 0.0
    for w in palavras:
        if 3 <= len(w) <= 5:
            x = 1.0
            for ch in w.upper():
                x *= freq[ch] / t
            d += x
    return d


def main():
    f = frequencias(PALAVRAS)
    en = {c: palavras_rl.LETTER_FREQ[c] for c in ALFA}
    dpt, den = densidade(PALAVRAS, f), densidade(PALAVRAS, en)
    assert abs(dpt - tabuleiro.densidade(PALAVRAS, tabuleiro.frequencias_de(PALAVRAS))) < 1e-15 * dpt
    assert abs(den - tabuleiro.densidade(PALAVRAS, palavras_rl.LETTER_FREQ)) < 1e-15 * den
    for c in ALFA:
        print(c + " " + f[c].hex())
    print("D_pt " + dpt.hex())
    print("D_en " + den.hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
