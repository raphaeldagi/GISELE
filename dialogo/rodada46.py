"""Rodada 46 do diálogo Python <-> Java: o motor de Horn em tempo linear (Dowling e Gallier, 1984), a otimização que o texto recebido na Parte 72
deixou para depois. Com `--preparar PASTA`, o Python grava em PASTA/horn46.txt os fatos (animal e pessoa, os primeiros sentidos de substantivo) e as
84.427 regras "p ⇒ c" da hiperonímia dos substantivos (calculos.p1611). As duas linguagens rodam o mesmo algoritmo (contadores de premissas, fila FIFO)
e imprimem, para cada fato inicial: quantos átomos derivou, uma soma de controle da ORDEM de derivação, os decrementos e a cadeia de prova do último
átomo derivado. Rodar da raiz: python3 dialogo/rodada46.py PASTA"""

import os
import sys
from collections import deque

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
MOD = (1 << 61) - 1


def preparar(pasta):
    import calculos
    from synthai.dicionario import Dicionario
    d = Dicionario()
    fatos, regras = calculos.p1611_regras_de_animal(d)
    pessoa = min(i for i in d.lemas["person"] if d.sinsets[i][0] == "n")
    with open(os.path.join(pasta, "horn46.txt"), "w") as f:
        f.write(f"{fatos[0]} {pessoa}\n")
        for prem, c in regras:
            f.write(" ".join(str(a) for a in prem) + f" {c}\n")


def ler(pasta):
    linhas = [l for l in open(os.path.join(pasta, "horn46.txt")).read().split("\n") if l]
    fatos = [int(x) for x in linhas[0].split()]
    regras = []
    for l in linhas[1:]:
        xs = [int(x) for x in l.split()]
        regras.append((xs[:-1], xs[-1]))
    return fatos, regras


def horn(fato, regras):
    falta, vigia = [], {}
    for r, (prem, _) in enumerate(regras):
        distintas = []
        for a in prem:
            if a not in distintas:
                distintas.append(a)
        falta.append(len(distintas))
        for a in distintas:
            vigia.setdefault(a, []).append(r)
    prova, ordem, fila = {fato: -1}, [fato], deque([fato])
    dec = 0
    while fila:
        a = fila.popleft()
        for r in vigia.get(a, ()):
            falta[r] -= 1
            dec += 1
            c = regras[r][1]
            if falta[r] == 0 and c not in prova:
                prova[c] = r
                ordem.append(c)
                fila.append(c)
    controle = 0
    for k, a in enumerate(ordem):
        controle = (controle + (k + 1) * a) % MOD
    cadeia, a = [], ordem[-1]
    while prova[a] != -1:
        cadeia.append(prova[a])
        a = regras[prova[a]][0][0]
    return len(ordem), controle, dec, cadeia


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        preparar(sys.argv[2])
        return
    fatos, regras = ler(sys.argv[1])
    for fato in fatos:
        n, controle, dec, cadeia = horn(fato, regras)
        print(f"fato {fato}: derivados {n} controle {controle} decrementos {dec} prova {' '.join(str(r) for r in cadeia)}")


if __name__ == "__main__":
    main()
