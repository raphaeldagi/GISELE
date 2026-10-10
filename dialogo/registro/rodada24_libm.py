"""Rodada 24 do diálogo Python <-> Java: a pergunta reconhece a sua resposta? O texto pós-ASI (externos/pos_asi_texto_parte50.md,
reenviado pelo usuário) é pontuado contra os documentos das Partes 1-49 com as palavras da Rodada 19 (soma de ln(K/df) sobre
as palavras em comum; df contado nos documentos). Com `--preparar PASTA`, escreve PASTA/docs24.txt (parte TAB palavras) e
PASTA/texto24.txt. Rodar da raiz do repositório: python3 dialogo/rodada24.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
_spec = importlib.util.spec_from_file_location("rodada19", os.path.join(AQUI, "rodada19.py"))
r19 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(r19)
TEXTO = os.path.join(RAIZ, "externos", "pos_asi_texto_parte50.md")


def dados(ate=49):
    docs = r19.documentos()
    ds = [(k, sorted(r19.numeros(open(os.path.join(RAIZ, docs[k]), encoding="utf-8").read()))) for k in sorted(docs) if k <= ate]
    return ds, sorted(r19.numeros(open(TEXTO, encoding="utf-8").read()))


def pontuar(ds, texto):
    K = len(ds)
    df = {}
    for _, ws in ds:
        for w in ws:
            df[w] = df.get(w, 0) + 1
    t = set(texto)
    res = []
    for k, ws in ds:
        s = 0.0
        for w in ws:
            if w in t:
                s += math.log(K / df[w])
        res.append((k, s))
    return res


def main():
    ds, texto = dados()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "docs24.txt"), "w", encoding="ascii") as f:
            for k, ws in ds:
                f.write(f"{k}\t{' '.join(ws)}\n")
        with open(os.path.join(sys.argv[2], "texto24.txt"), "w", encoding="ascii") as f:
            f.write(" ".join(texto) + "\n")
        return
    res = pontuar(ds, texto)
    for k, s in res:
        print(f"parte {k}: escore = {s.hex()}")
    melhor, me = None, -1.0
    for k, s in res:
        if s > me:
            melhor, me = k, s
    print(f"o texto escolhe a parte {melhor}")


if __name__ == "__main__":
    main()
