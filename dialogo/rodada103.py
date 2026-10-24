"""Rodada 103 do diálogo Python <-> Java (Parte 155): as estatísticas exatas do fim do episódio de synthai.tabuleiro.estatisticas_exatas com a ORDEM REVERSA
das vizinhas ((1, 1), …, (−1, −1)), bit a bit, na grade 3 × 3, caso B ({a, b, c} = (0,5; 0,3; 0,2), sem letras iguais seguidas), de 3 a 4 letras. Por
caminho, o vetor (acerto, dr, dc, distância à borda, comprimento); a soma dos filhos na ordem das ações e a divisão por n; o total ponderado por atribuição
(ordem do itertools.product). Confere contra o módulo (1e-12) antes de imprimir. Da raiz: python3 dialogo/rodada103.py"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai import tabuleiro  # noqa: E402


def estat(palavras, letras, pesos, tamanho=3, minimo=3, maximo=4):
    t = 0.0
    for w in pesos:
        t += w
    p = [w / t for w in pesos]
    dic = set(palavras)
    casas = [(r, c) for r in range(tamanho) for c in range(tamanho)]
    deltas = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b][::-1]
    vz = {}
    for (r, c) in casas:
        vz[(r, c)] = [(r + a, c + b) for a, b in deltas if 0 <= r + a < tamanho and 0 <= c + b < tamanho]
    tot = [0.0] * 5
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
                return [0.0] * 5
            s = [0.0] * 5
            if parar:
                (r0, c0), (r1, c1) = caminho[0], caminho[-1]
                s = [1.0 if prefixo in dic else 0.0, float(r1 - r0), float(c1 - c0),
                     float(min(r1, c1, tamanho - 1 - r1, tamanho - 1 - c1)), float(len(caminho))]
            for letra, v in acoes.items():
                f = anda(caminho + [v], prefixo + letra)
                for k in range(5):
                    s[k] = s[k] + f[k]
            return [x / n for x in s]
        for u in casas:
            f = anda([u], grade[u])
            for k in range(5):
                tot[k] += peso * f[k] / len(casas)
    return tot


def main():
    tres = ["".join(x) for L in (3, 4, 5) for x in itertools.product("abc", repeat=L)]
    B = [w for w in tres if all(a != b for a, b in zip(w, w[1:]))]
    e = estat(B, "abc", [0.5, 0.3, 0.2])
    m = tabuleiro.estatisticas_exatas(B, {"A": 0.5, "B": 0.3, "C": 0.2}, 3, 3, 4, ordem="reversa")
    for k, nome in enumerate(("acerto", "dr", "dc", "borda", "comprimento")):
        assert abs(e[k] - m[nome]) < 1e-12
        print(nome + " " + e[k].hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
