"""Rodada 101 do diálogo Python <-> Java (Parte 153): o braço aleatório EXATO de synthai.tabuleiro.aleatorio_exato bit a bit, na grade 3 × 3. Todas as
atribuições de letras (ordem do itertools.product: a última casa varia mais depressa), peso Π p na ordem das casas, e em cada uma a recursão sobre os
caminhos com a regra do valid_actions (ações por letra na ordem de inserção das vizinhas; PARAR com 3 ou mais letras; só PARAR com 5). Casos A' ({a, b} =
(0,7; 0,3), palavras de 'a' a 'b') e B ({a, b, c} = (0,5; 0,3; 0,2), sem letras iguais seguidas). Somas em laço. Confere contra o módulo (1e-12) antes de
imprimir. Da raiz: python3 dialogo/rodada101.py"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai import tabuleiro  # noqa: E402


def exato(palavras, letras, pesos, tamanho=3, minimo=3, maximo=5):
    t = 0.0
    for w in pesos:
        t += w
    p = [w / t for w in pesos]
    dic = set(palavras)
    casas = [(r, c) for r in range(tamanho) for c in range(tamanho)]
    vz = {}
    for (r, c) in casas:
        lst = []
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                if (a or b) and 0 <= r + a < tamanho and 0 <= c + b < tamanho:
                    lst.append((r + a, c + b))
        vz[(r, c)] = lst
    total = 0.0
    for idx in itertools.product(range(len(letras)), repeat=len(casas)):
        grade = {u: letras[i] for u, i in zip(casas, idx)}
        peso = 1.0
        for i in idx:
            peso = peso * p[i]

        def anda(caminho, prefixo):
            acoes = {}
            if len(caminho) < maximo:
                for v in vz[caminho[-1]]:
                    if v not in caminho and grade[v] not in acoes:
                        acoes[grade[v]] = v
            parar = len(caminho) >= minimo
            n = len(acoes) + (1 if parar else 0)
            if n == 0:
                return 0.0
            s = (1.0 if prefixo in dic else 0.0) if parar else 0.0
            for letra, v in acoes.items():
                s += anda(caminho + [v], prefixo + letra)
            return s / n
        acerto = 0.0
        for u in casas:
            acerto += anda([u], grade[u])
        total += peso * acerto / len(casas)
    return total


def main():
    duas = ["".join(x) for L in (3, 4, 5) for x in itertools.product("ab", repeat=L)]
    A = [w for w in duas if w[0] == "a" and w[-1] == "b"]
    tres = ["".join(x) for L in (3, 4, 5) for x in itertools.product("abc", repeat=L)]
    B = [w for w in tres if all(a != b for a, b in zip(w, w[1:]))]
    ea = exato(A, "ab", [0.7, 0.3])
    eb = exato(B, "abc", [0.5, 0.3, 0.2])
    assert abs(ea - tabuleiro.aleatorio_exato(A, {"A": 0.7, "B": 0.3}, 3)) < 1e-12
    assert abs(eb - tabuleiro.aleatorio_exato(B, {"A": 0.5, "B": 0.3, "C": 0.2}, 3)) < 1e-12
    print("A' " + ea.hex())
    print("B " + eb.hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
