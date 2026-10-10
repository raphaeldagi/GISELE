"""Rodada 6 do diálogo Python <-> Java: o Naive Bayes com pares de palavras (P492) treinado nas tarefas A e B do dicionário
e testado no teste de A. Com `--preparar PASTA`, escreve os exemplos (classe, TAB, atributos separados por espaço) em
PASTA/treino06.txt e PASTA/teste06.txt, que o Java lê. Imprime a acurácia, o SHA-256 das previsões e os escores das 4
classes nos 50 primeiros exemplos, em hexadecimal. Rodar da raiz do repositório: python3 dialogo/rodada06.py"""

import hashlib
import os
import sys
from math import log

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import calculos  # noqa: E402
from synthai.dicionario import NaiveBayesContagens  # noqa: E402

A, B, teste = calculos._dados_464(bigramas=True)
if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
    for nome, dados in (("treino06.txt", A + B), ("teste06.txt", teste)):
        with open(os.path.join(sys.argv[2], nome), "w", encoding="utf-8") as f:
            for x, y in dados:
                f.write(y + "\t" + " ".join(x) + "\n")
    sys.exit(0)
m = NaiveBayesContagens()
for x, y in A + B:
    m.aprender(x, y)
prev = [m.prever(x) for x, _ in teste]
acertos = sum(p == y for p, (_, y) in zip(prev, teste))
print(f"acertos = {acertos} de {len(teste)}; sha = {hashlib.sha256(''.join(prev).encode()).hexdigest()}")
n = sum(m.ncls.values())
v = len(m.vocab)
for i, (x, _) in enumerate(teste[:50]):
    esc = []
    for cl in sorted(m.ncls):
        s = log(m.ncls[cl] / n)
        c, t = m.cont[cl], m.total[cl]
        for w in x:
            s += log((c.get(w, 0) + m.alfa) / (t + m.alfa * v))
        esc.append(s.hex())
    print(f"{i}: " + " ".join(esc))
