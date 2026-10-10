"""Rodada 43 do diálogo Python <-> Java: a forma de GPT decide o próximo caractere. Com `--preparar PASTA`, o Python pré-treina um GPT
pequeno (synthai/gpt.py; T = 8, d = 8, h = 16, 400 passos nas definições do WordNet, semente 43) e escreve os pesos em PASTA/gpt43.txt (floats
em hexadecimal). Depois, Python e Java leem os mesmos pesos e fazem a mesma ida (com exp e log próprios, rodada 26) numa frase fixa: o argmax
e a probabilidade do próximo caractere em cada posição, e o total de bits. Rodar da raiz: python3 dialogo/rodada43.py PASTA"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rodada26 import exp_, log_  # noqa: E402

FRASE = "a domestic animal kept for comp"
FORMA = (8, 8, 16)  # T, d, h


def preparar(pasta):
    import calculos
    from synthai.gpt import GPT, PARAMS
    treino, _ = calculos.p1511_corpus_de_glosas("en")
    T, d, h = FORMA
    g = GPT(calculos.VOCAB_GPT, T=T, d=d, h=h, semente=43)
    g.treinar(treino, passos=400, lr=0.01, semente=43)
    with open(os.path.join(pasta, "gpt43.txt"), "w") as f:
        f.write("".join(calculos.VOCAB_GPT) + "\n")
        for nome in PARAMS:
            M = g.p[nome]
            f.write(f"{nome} {len(M)} {len(M[0])}\n")
            for linha in M:
                f.write(" ".join(x.hex() for x in linha) + "\n")


def ler(pasta):
    with open(os.path.join(pasta, "gpt43.txt")) as f:
        linhas = f.read().split("\n")
    vocab = list(linhas[0])
    p, i = {}, 1
    while i < len(linhas) and linhas[i]:
        nome, n, m = linhas[i].split()
        p[nome] = [[float.fromhex(x) for x in linhas[i + 1 + k].split()] for k in range(int(n))]
        i += 1 + int(n)
    return vocab, p


def decisoes(vocab, p):
    """[(t, contexto, argmax, p do argmax, p do real)] e o total de bits, com exp e log próprios."""
    from synthai.gpt import GPT
    T, d, h = FORMA
    g = GPT(vocab, T=T, d=d, h=h)
    g.p = p
    ids = g.codificar(FRASE)
    bits = 0.0
    saida = []
    for t in range(len(ids) - 1):
        janela = ids[max(0, t + 1 - T):t + 1]
        pr = g.adiante(janela, exp=exp_)["probs"][-1]
        melhor = 0
        for j in range(1, len(pr)):
            if pr[j] > pr[melhor]:
                melhor = j
        bits -= log_(pr[ids[t + 1]]) / log_(2.0)
        saida.append((t, FRASE[max(0, t + 1 - T):t + 1], vocab[melhor], pr[melhor], pr[ids[t + 1]]))
    return saida, bits


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        preparar(sys.argv[2])
        return
    saida, bits = decisoes(*ler(sys.argv[1]))
    for t, ctx, arg, pa, pr in saida:
        print(f"t={t} contexto={ctx!r} argmax={arg!r} p={pa.hex()} p_real={pr.hex()}")
    print(f"bits totais={bits.hex()}")


if __name__ == "__main__":
    main()
