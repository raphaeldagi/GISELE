"""Rodada 19 do diálogo Python <-> Java: reconstruir a parte a partir só das PALAVRAS (a Rodada 18 usou os números). Tiram-se
os rótulos (Pnnn, 0x...), os acentos (NFD sem as marcas combinantes), minúsculas, e ficam as palavras a-z de 4 letras ou mais;
o resto é a Rodada 18 (soma de ln(K/df), empate para a menor parte). Com `--preparar PASTA`, escreve PASTA/docs19.txt.
Rodar da raiz do repositório: python3 dialogo/rodada19.py"""

import glob
import math
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROTULO = re.compile(r"P[0-9]+|0x[0-9A-Fa-f]+")
PALAVRA = re.compile(r"[a-z]{4,}")


def documentos():
    docs = {1: "ASI_AGI_perguntas_e_respostas.md"}
    for f in glob.glob(os.path.join(RAIZ, "ASI_AGI_parte*.md")):
        nome = os.path.basename(f)
        docs[int(re.match(r"ASI_AGI_parte([0-9]+)_", nome).group(1))] = nome
    return docs


def numeros(texto):
    """As palavras (o nome ficou da Rodada 18, para o resto do código ser o mesmo)."""
    t = unicodedata.normalize("NFD", ROTULO.sub(" ", texto))
    t = "".join(c for c in t if not unicodedata.category(c).startswith("M")).lower()
    return set(PALAVRA.findall(t))


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
                s += math.log(K / df[t])
            if s > me:
                melhor, me = k, s
        res.append((n, melhor, me, len(r)))
    return res


def main():
    docs = documentos()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "docs19.txt"), "w", encoding="utf-8") as f:
            for k in sorted(docs):
                f.write(f"{k}\t{docs[k]}\n")
        return
    acertos = 0
    for n, k, s, m in reconstruir(docs):
        acertos += n == k
        print(f"parte {n}: {m} palavras; escolhe a parte {k}; escore = {s.hex()}")
    print(f"acertos: {acertos}")


if __name__ == "__main__":
    main()
