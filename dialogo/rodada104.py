"""Rodada 104 do diálogo Python <-> Java (Parte 156): as esperanças exatas das DECISÕES do episódio de synthai.tabuleiro.ramificacao_exata, bit a bit, na
grade 3 × 3, caso B ({a, b, c} = (0,5; 0,3; 0,2), sem letras iguais seguidas), de 3 a 4 letras, primeira casa de cada letra. Por caminho, o vetor (acerto,
falha, decisões, opções, livres, ações): a soma dos filhos na ordem das ações, a divisão por n e, depois, a decisão do próprio nó (1, n, livres, ações). O
total ponderado por atribuição (ordem do itertools.product). Confere contra o módulo (1e-12) antes de imprimir. Da raiz: python3 dialogo/rodada104.py"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai import tabuleiro  # noqa: E402


def ramif(palavras, letras, pesos, tamanho=3, minimo=3, maximo=4):
    t = 0.0
    for w in pesos:
        t += w
    p = [w / t for w in pesos]
    dic = set(palavras)
    casas = [(r, c) for r in range(tamanho) for c in range(tamanho)]
    deltas = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
    vz = {}
    for (r, c) in casas:
        vz[(r, c)] = [(r + a, c + b) for a, b in deltas if 0 <= r + a < tamanho and 0 <= c + b < tamanho]
    tot = [0.0] * 6
    for idx in itertools.product(range(len(letras)), repeat=len(casas)):
        grade = {u: letras[i] for u, i in zip(casas, idx)}
        peso = 1.0
        for i in idx:
            peso = peso * p[i]

        def anda(caminho, prefixo):
            acoes = {}
            livres = 0
            if len(caminho) < maximo:
                for v in vz[caminho[-1]]:
                    if v not in caminho:
                        livres += 1
                        if grade[v] not in acoes:
                            acoes[grade[v]] = v
            parar = len(caminho) >= minimo
            n = len(acoes) + (1 if parar else 0)
            if n == 0:
                return [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
            s = [0.0] * 6
            if parar:
                s[0] = 1.0 if prefixo in dic else 0.0
            for letra, v in acoes.items():
                f = anda(caminho + [v], prefixo + letra)
                for k in range(6):
                    s[k] = s[k] + f[k]
            s = [x / n for x in s]
            s[2] += 1.0
            s[3] += n
            s[4] += livres
            s[5] += len(acoes)
            return s
        for u in casas:
            f = anda([u], grade[u])
            for k in range(6):
                tot[k] += peso * f[k] / len(casas)
    return tot


def main():
    tres = ["".join(x) for L in (3, 4, 5) for x in itertools.product("abc", repeat=L)]
    B = [w for w in tres if all(a != b for a, b in zip(w, w[1:]))]
    e = ramif(B, "abc", [0.5, 0.3, 0.2])
    m = tabuleiro.ramificacao_exata(B, {"A": 0.5, "B": 0.3, "C": 0.2}, 3, 3, 4)
    for k, nome in enumerate(("acerto", "falha", "decisoes", "opcoes", "livres", "acoes")):
        assert abs(e[k] - m[nome]) < 1e-12
        print(nome + " " + e[k].hex())
    print("conferido True")
    print("fim")


if __name__ == "__main__":
    main()
