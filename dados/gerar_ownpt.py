"""Gera dados/ownpt_sinsets.tsv.gz a partir da OpenWordNet-PT (OWN-PT, https://github.com/own-pt/openWordnet-PT,
licença Creative Commons Atribuição 4.0, ver dados/OWNPT_LICENSE.txt), Parte 39.

Uma linha por sinset com conteúdo em português: o identificador do WordNet 3.0 (deslocamento-classe, o mesmo do data
lake em inglês), os lemas em português separados por "|", e a glosa em português (vazia se não houver).
Uso: python3 dados/gerar_ownpt.py CAMINHO/openWordnet-PT/data"""

import gzip
import os
import re
import sys

ID = re.compile(r"^own-pt:synset-(\d{8}-[nvars]) ")
GLOSA = re.compile(r'owns:gloss "((?:[^"\\]|\\.)*)"@pt')
SENTIDO = re.compile(r"^own-pt:wordsense-(\d{8}-[nvars])-\d+ a owns:WordSense")
ROTULO = re.compile(r'rdfs:label "((?:[^"\\]|\\.)*)"@pt')


def blocos(caminho):
    with open(caminho, encoding="utf-8") as f:
        bloco = []
        for linha in f:
            if linha.strip() == "":
                if bloco:
                    yield "".join(bloco)
                bloco = []
            else:
                bloco.append(linha)
        if bloco:
            yield "".join(bloco)


def main(pasta):
    glosas, lemas = {}, {}
    for b in blocos(os.path.join(pasta, "own-pt-synsets.ttl")):
        m = ID.match(b)
        if m:
            g = GLOSA.search(b)
            glosas[m.group(1)] = (g.group(1).replace('\\"', '"') if g else "").replace("\t", " ").replace("\n", " ")
    for b in blocos(os.path.join(pasta, "own-pt-wordsenses.ttl")):
        m = SENTIDO.match(b)
        if m:
            r = ROTULO.search(b)
            if r:
                lemas.setdefault(m.group(1), []).append(r.group(1).strip().replace("\t", " "))
    ids = sorted({i for i in set(glosas) | set(lemas) if lemas.get(i) or glosas.get(i)}, key=lambda x: (x[-1], x))
    saida = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ownpt_sinsets.tsv.gz")
    with gzip.open(saida, "wt", encoding="utf-8", compresslevel=9) as f:
        for i in ids:
            f.write(i + "\t" + "|".join(lemas.get(i, [])) + "\t" + glosas.get(i, "") + "\n")
    print(len(ids), "sinsets;", sum(1 for i in ids if lemas.get(i)), "com lemas;", sum(1 for i in ids if glosas.get(i)), "com glosa")


if __name__ == "__main__":
    main(sys.argv[1])
