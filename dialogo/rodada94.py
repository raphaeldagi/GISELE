"""Rodada 94 do diálogo Python <-> Java (Parte 143): o retrocesso e a memória congelada de synthai.memoria_congelada (de
externos/pacote3/transferencia_metacognitiva.py) bit a bit. Tarefas quadráticas d = 6 de um LCG (A = I/2 + MᵀM/(2d), alvo e partida em
[−1, 1]), sem ruído e sem conflito; 8 tarefas de treino alimentam a MemoriaFalhas REAL, que é congelada; 8 tarefas de teste rodam com o
fator dela, passo 0,2, orçamento 24. O lado Python chama o executar REAL do módulo. Imprime as contagens, os três fatores e as razões de
custo em hexadecimal. Da raiz: python3 dialogo/rodada94.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from synthai.memoria_congelada import MemoriaFalhas, executar  # noqa: E402

D = 6
x = 15194


def u():
    global x
    x = (1103515245 * x + 12345) % 2147483648
    return 2.0 * (x / 2147483648.0) - 1.0


def tarefa(i):
    M = [[u() for _ in range(D)] for _ in range(D)]
    A = []
    for a in range(D):
        linha = []
        for b in range(D):
            t = 0.0
            for k in range(D):
                t += M[k][a] * M[k][b]
            linha.append((0.5 if a == b else 0.0) + t / (2.0 * D))
        A.append(linha)
    return dict(A=A, alvo=[u() for _ in range(D)], x0=[u() for _ in range(D)], sigma=0.0, conflito=0.0,
                familia="suave", chave=(94, 1, i))


def main():
    treino = [tarefa(i) for i in range(8)]
    teste = [tarefa(100 + i) for i in range(8)]
    col = MemoriaFalhas()
    for t in treino:
        executar(t, 0.2, coletor=col)
    fator = col.congelar()
    for c in ("baixo", "medio", "alto"):
        n, r = col.contagens[c]
        print(c + " " + str(n) + " " + str(r) + " " + fator(c).hex())
    for t in teste:
        print("razao " + executar(t, 0.2, fator=fator).hex())
    print("fim")


if __name__ == "__main__":
    main()
