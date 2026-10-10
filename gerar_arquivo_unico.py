"""Gera SYNTHAI_completo.py: um arquivo .py único com TODO o código do projeto (calculos.py e o pacote synthai/).

O arquivo único guarda cada fonte como texto, na ordem em que aparecem no repositório, e, ao rodar, recria os módulos
numa pasta temporária e executa o original. Assim ele dá exatamente os mesmos números (as classes de `calculos.py` e
de `synthai/` têm nomes em comum e não podem ser simplesmente coladas no mesmo espaço de nomes).

Uso: python3 gerar_arquivo_unico.py   (rodar de novo sempre que o código mudar)"""

import os

RAIZ = os.path.dirname(os.path.abspath(__file__))
FONTES = ["calculos.py", "CLAUDE.md"] + sorted(
    os.path.join("synthai", f) for f in os.listdir(os.path.join(RAIZ, "synthai")) if f.endswith(".py")) + sorted(
    os.path.join("externos", f) for f in os.listdir(os.path.join(RAIZ, "externos")) if f.endswith(".py"))  # Parte 33


def _textos_lidos_pelo_codigo():
    """Os textos que as funções leem (Parte 68): o resultados.txt (as rodadas 18 a 21 e a P853 o leem), os documentos das partes (P1031, P1452,
    P1481 os leem), o diálogo inteiro (as pNN das rodadas importam dialogo/rodadaNN.py, a P1241 lê o DIALOGO.md; os .java vão como texto,
    para o verificar.py funcionar depois de --extrair) e os textos de externos/ (só dados, nunca executados)."""
    saida = ["resultados.txt"] + sorted(f for f in os.listdir(RAIZ) if f.startswith("ASI_AGI_") and f.endswith(".md"))
    saida += sorted(os.path.join("externos", f) for f in os.listdir(os.path.join(RAIZ, "externos")) if f.endswith(".md"))
    for pasta, subpastas, arquivos in sorted(os.walk(os.path.join(RAIZ, "dialogo"))):
        subpastas[:] = sorted(d for d in subpastas if d != "__pycache__")
        for f in sorted(arquivos):
            if f.endswith((".py", ".java", ".md", ".tsv", ".txt")):
                saida.append(os.path.relpath(os.path.join(pasta, f), RAIZ))
    return saida


FONTES += _textos_lidos_pelo_codigo()
DADOS = sorted(os.path.join("dados", f) for f in os.listdir(os.path.join(RAIZ, "dados"))
               if f.endswith((".gz", ".txt", ".py")))  # o dicionário (Parte 30): binários em base64

CABECALHO = '''#!/usr/bin/env python3
"""SYNTHAI — o projeto inteiro num arquivo só (Partes 1 a PARTE_FINAL, perguntas P1 a PPNN_FINAL).

Este arquivo contém, como texto, TODO o código do repositório GISELE:
  - calculos.py: os cálculos e simulações de todas as partes (funções pNN_..., a linhagem da SYNTHAI, os testes de
    regressão);
  - synthai/: o protótipo em módulos, uma função de Jung por arquivo (percepção, pensamento, intuição, sentimento,
    relação com o humano), os mundos, as réguas e as suítes de testes de unidade;
  - CLAUDE.md: as convenções do projeto (a P143 mede o tamanho dele);
  - dados/: o dicionário WordNet 3.0 (Parte 30) e o português da OpenWordNet-PT (Parte 39, CC BY 4.0), em base64, com as licenças;
  - os textos que o código lê: os documentos das partes (ASI_AGI_*.md), o resultados.txt, e o diálogo Python <-> Java inteiro
    (dialogo/: as rodadas em Python, que as funções importam, e em Java, como texto; o DIALOGO.md).

Como rodar (só biblioteca padrão do Python 3):
  python3 SYNTHAI_completo.py              todas as partes (leva horas: melhor em blocos, como abaixo) e a unificação
  python3 SYNTHAI_completo.py 22 26        só as partes pedidas, e a unificação
  python3 SYNTHAI_completo.py --demo       a mesma SYNTHAI em três tipos de tarefa
  python3 SYNTHAI_completo.py --testes     os testes de unidade do pacote
  python3 SYNTHAI_completo.py --extrair P  recria os arquivos originais na pasta P

Gerado por gerar_arquivo_unico.py a partir do repositório; não editar à mão.
"""

import base64
import os
import runpy
import sys
import tempfile

FONTES = {}
DADOS = {}  # o dicionário WordNet 3.0 (Parte 30), em base64; licença em dados/WORDNET_LICENSE.txt
'''

RODAPE = '''

def extrair(destino):
    for nome, fonte in FONTES.items():
        caminho = os.path.join(destino, nome)
        os.makedirs(os.path.dirname(caminho) or destino, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(fonte)
    for nome, b64 in DADOS.items():
        caminho = os.path.join(destino, nome)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "wb") as f:
            f.write(base64.b64decode(b64))
    return destino


def main(args):
    if args[:1] == ["--extrair"]:
        print("arquivos recriados em", extrair(args[1]))
        return
    pasta = extrair(tempfile.mkdtemp(prefix="synthai_"))
    sys.path.insert(0, pasta)
    os.chdir(pasta)
    if args[:1] == ["--testes"]:
        import unittest
        nomes = ["synthai." + n[len("synthai/"):-3] for n in FONTES if n.startswith("synthai/testes")]
        suite = unittest.defaultTestLoader.loadTestsFromNames(nomes)
        sys.exit(0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1)
    if args[:1] == ["--demo"]:
        sys.argv = ["synthai"]
        runpy.run_module("synthai", run_name="__main__", alter_sys=True)
        return
    sys.argv = [os.path.join(pasta, "calculos.py")] + args
    runpy.run_path(sys.argv[0], run_name="__main__")


if __name__ == "__main__":
    main(sys.argv[1:])
'''


def literal(texto):
    """Texto como string Python entre aspas triplas, legível: só a barra invertida e as aspas triplas são escapadas."""
    return '"""' + texto.replace("\\", "\\\\").replace('"""', '\\"\\"\\"') + '"""'


def gerar(saida="SYNTHAI_completo.py"):
    import re
    codigo = open(os.path.join(RAIZ, "calculos.py"), encoding="utf-8").read()
    pnn = max(int(n) for n in re.findall(r"^def p(\d+)_", codigo, re.M))
    parte = max(int(n) for n in re.findall(r"^def _parte_(\d+)\(", codigo, re.M))
    partes = [CABECALHO.replace("PARTE_FINAL", str(parte)).replace("PNN_FINAL", str(pnn))]
    for nome in FONTES:
        texto = open(os.path.join(RAIZ, nome), encoding="utf-8").read()
        partes.append(f"\n# {'=' * 100}\n# {nome}  ({texto.count(chr(10))} linhas)\n# {'=' * 100}\n"
                      f"FONTES[{nome!r}] = {literal(texto)}\n")
    import base64
    for nome in DADOS:
        b64 = base64.b64encode(open(os.path.join(RAIZ, nome), "rb").read()).decode()
        linhas = [b64[i:i + 120] for i in range(0, len(b64), 120)]
        partes.append(f"\n# {'=' * 100}\n# {nome}  (dados, base64)\n# {'=' * 100}\n"
                      f"DADOS[{nome!r}] = (\n" + "\n".join(f"    {l!r}" for l in linhas) + "\n)\n")
    partes.append(RODAPE)
    with open(os.path.join(RAIZ, saida), "w", encoding="utf-8") as f:
        f.write("".join(partes))
    return saida


if __name__ == "__main__":
    print(gerar())
