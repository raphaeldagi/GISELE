"""Rodada 17 do diálogo Python <-> Java: a pergunta é a resposta, comprimida (P822). Para cada pergunta deixada no fim de
uma rodada (q) e a rodada seguinte (r): C(q), C(r) e C(r + "\\n" + q), com zlib nível 9. Com `--preparar PASTA`, escreve
PASTA/pares17.txt (base64 de q, TAB, base64 de r, um par por linha), que o Java lê.
Rodar da raiz do repositório: python3 dialogo/rodada17.py"""

import base64
import os
import re
import sys
import zlib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pares():
    texto = open(os.path.join(RAIZ, "dialogo", "DIALOGO.md"), encoding="utf-8").read()
    rodadas = re.split(r"\n## Rodada ", texto)
    res = []
    for atual, prox in zip(rodadas, rodadas[1:]):
        m = re.search(r"\*\*IA-[A-Za-z]+ \((?:a )?pergunta para a Rodada \d+\)\)?:?\*\*:?\s*(.*?)(?:\n\n|$)", atual, re.S)
        if m:
            res.append((m.group(1), prox))
    return res


def main():
    ps = pares()
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "pares17.txt"), "w", encoding="ascii") as f:
            for q, r in ps:
                f.write(base64.b64encode(q.encode()).decode() + "\t" + base64.b64encode(r.encode()).decode() + "\n")
        return
    c = lambda t: len(zlib.compress(t.encode("utf-8"), 9))
    for i, (q, r) in enumerate(ps):
        print(f"par {i}: C(q) = {c(q)}; C(r) = {c(r)}; C(r+q) = {c(r + chr(10) + q)}")


if __name__ == "__main__":
    main()
