"""Gera o data lake do dicionário a partir do WordNet 3.0 de Princeton (Parte 30).

Fonte: https://wordnetcode.princeton.edu/3.0/WordNet-3.0.tar.gz
SHA-256 do arquivo usado: 640db279c949a88f61f851dd54ebbb22d003f8b90b85267042ef85a3781d3a52
Licença: a do WordNet 3.0 (copiada em dados/WORDNET_LICENSE.txt), que permite usar, copiar, modificar e distribuir
mantendo o aviso de copyright.

Uso: python3 dados/gerar_wordnet.py <pasta dict/ do WordNet extraído>
Saídas (só biblioteca padrão para ler, com gzip):
  dados/wordnet30_sinsets.tsv.gz  classe gramatical, deslocamento, lemas (vírgula), hiperônimos (classe:desl.), glosa
  dados/wordnet30_excecoes.tsv.gz classe gramatical, forma flexionada, lemas-base (as listas .exc, para a morfologia)"""

import gzip
import os
import sys

CLASSES = {"noun": "n", "verb": "v", "adj": "a", "adv": "r"}


def sinsets(pasta):
    for nome, pos in CLASSES.items():
        with open(os.path.join(pasta, "data." + nome), encoding="latin-1") as f:
            for linha in f:
                if linha.startswith("  "):
                    continue  # cabeçalho da licença
                campos, _, glosa = linha.partition("|")
                p = campos.split()
                desloc, n_palavras = p[0], int(p[3], 16)
                lemas = [p[4 + 2 * i].lower() for i in range(n_palavras)]
                i = 4 + 2 * n_palavras
                n_ptr = int(p[i])
                hiper = []
                for k in range(n_ptr):
                    simbolo, alvo, pos_alvo = p[i + 1 + 4 * k], p[i + 2 + 4 * k], p[i + 3 + 4 * k]
                    if simbolo in ("@", "@i"):
                        hiper.append(f"{pos_alvo.replace('s', 'a')}:{alvo}")
                yield pos, desloc, ",".join(lemas), ",".join(hiper), glosa.strip()


def main(pasta):
    raiz = os.path.dirname(os.path.abspath(__file__))
    n = 0
    with gzip.open(os.path.join(raiz, "wordnet30_sinsets.tsv.gz"), "wt", encoding="utf-8", compresslevel=9) as out:
        for campos in sinsets(pasta):
            out.write("\t".join(campos) + "\n")
            n += 1
    m = 0
    with gzip.open(os.path.join(raiz, "wordnet30_excecoes.tsv.gz"), "wt", encoding="utf-8", compresslevel=9) as out:
        for nome, pos in CLASSES.items():
            with open(os.path.join(pasta, nome + ".exc"), encoding="latin-1") as f:
                for linha in f:
                    p = linha.split()
                    if len(p) >= 2:
                        out.write(f"{pos}\t{p[0]}\t{','.join(p[1:])}\n")
                        m += 1
    print(n, "sinsets;", m, "exceções")


if __name__ == "__main__":
    main(sys.argv[1])
