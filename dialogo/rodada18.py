"""Rodada 18 do diálogo Python <-> Java: reconstruir as perguntas a partir só dos números. Para cada parte com documento e
seção no resultados.txt, tiram-se os rótulos (Pnnn, 0x...) e ficam os números (só os dígitos, sem zeros à esquerda, 3 ou
mais); cada seção escolhe o documento com a maior soma de ln(K/df) sobre os números em comum. Com `--preparar PASTA`,
escreve PASTA/docs18.txt (parte TAB arquivo), que o Java lê. Rodar da raiz do repositório: python3 dialogo/rodada18.py"""

import glob
import math
import os
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exatas import log_  # noqa: E402  (Parte 73: log próprio, exato nas duas línguas)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTULO = re.compile(r"P[0-9]+|0x[0-9A-Fa-f]+")
NUMERO = re.compile(r"[0-9][0-9.,]*[0-9]|[0-9]")


def documentos():
    docs = {1: "ASI_AGI_perguntas_e_respostas.md"}
    for f in glob.glob(os.path.join(RAIZ, "ASI_AGI_parte*.md")):
        nome = os.path.basename(f)
        docs[int(re.match(r"ASI_AGI_parte([0-9]+)_", nome).group(1))] = nome
    return docs


def numeros(texto):
    res = set()
    for x in NUMERO.findall(ROTULO.sub(" ", texto)):
        d = x.replace(".", "").replace(",", "").lstrip("0")
        if len(d) >= 3:
            res.add(d)
    return res


def secoes():
    sec, atual = {1: []}, 1
    for linha in open(os.path.join(RAIZ, "resultados.txt"), encoding="utf-8").read().split("\n"):
        m = re.match(r"--- Parte ([0-9]+)", linha)
        if m:
            atual = int(m.group(1))
            sec[atual] = []
        elif linha.startswith("=== Unificacao"):
            break
        else:
            sec[atual].append(linha)
    return {k: "\n".join(v) for k, v in sec.items()}


def reconstruir(docs):
    sec = secoes()
    partes = sorted(k for k in docs if k in sec)
    dn = {k: numeros(open(os.path.join(RAIZ, docs[k]), encoding="utf-8").read()) for k in partes}
    df = {}
    for k in partes:
        for t in dn[k]:
            df[t] = df.get(t, 0) + 1
    K = len(partes)
    res = []
    for n in partes:
        r = numeros(sec[n])
        melhor, me = None, -1.0
        for k in partes:
            s = 0.0
            for t in sorted(r & dn[k]):
                s += log_(K / df[t])
            if s > me:
                melhor, me = k, s
        res.append((n, melhor, me, len(r)))
    return res


def main():
    docs = documentos()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "docs18.txt"), "w", encoding="utf-8") as f:
            for k in sorted(docs):
                f.write(f"{k}\t{docs[k]}\n")
        return
    acertos = 0
    for n, k, s, m in reconstruir(docs):
        acertos += n == k
        print(f"parte {n}: {m} numeros; escolhe a parte {k}; escore = {s.hex()}")
    print(f"acertos: {acertos}")


if __name__ == "__main__":
    main()
