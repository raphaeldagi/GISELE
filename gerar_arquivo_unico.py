"""Gera SYNTHAI_completo.py: um arquivo .py único com TODO o código do projeto (calculos.py e o pacote synthai/).

O arquivo único guarda cada fonte como texto, na ordem em que aparecem no repositório, e, ao rodar, recria os módulos
numa pasta temporária e executa o original. Assim ele dá exatamente os mesmos números (as classes de `calculos.py` e
de `synthai/` têm nomes em comum e não podem ser simplesmente coladas no mesmo espaço de nomes).

Uso: python3 gerar_arquivo_unico.py   (rodar de novo sempre que o código mudar)"""

import os

RAIZ = os.path.dirname(os.path.abspath(__file__))
FONTES = ["calculos.py", "CLAUDE.md"] + sorted(
    os.path.join("synthai", f) for f in os.listdir(os.path.join(RAIZ, "synthai")) if f.endswith(".py"))

CABECALHO = '''#!/usr/bin/env python3
"""SYNTHAI — o projeto inteiro num arquivo só (Partes 1 a 26, perguntas P1 a P330).

Este arquivo contém, como texto, TODO o código do repositório GISELE:
  - calculos.py: os cálculos e simulações de todas as partes (funções pNN_..., a linhagem da SYNTHAI, os testes de
    regressão);
  - synthai/: o protótipo em módulos, uma função de Jung por arquivo (percepção, pensamento, intuição, sentimento,
    relação com o humano), os mundos, as réguas e as suítes de testes de unidade;
  - CLAUDE.md: as convenções do projeto (a P143 mede o tamanho dele).

Como rodar (só biblioteca padrão do Python 3):
  python3 SYNTHAI_completo.py              todas as partes (leva ~45 minutos) e a unificação
  python3 SYNTHAI_completo.py 22 26        só as partes pedidas, e a unificação
  python3 SYNTHAI_completo.py --demo       a mesma SYNTHAI em três tipos de tarefa
  python3 SYNTHAI_completo.py --testes     os testes de unidade do pacote
  python3 SYNTHAI_completo.py --extrair P  recria os arquivos originais na pasta P

Gerado por gerar_arquivo_unico.py a partir do repositório; não editar à mão.
"""

import os
import runpy
import sys
import tempfile

FONTES = {}
'''

RODAPE = '''

def extrair(destino):
    for nome, fonte in FONTES.items():
        caminho = os.path.join(destino, nome)
        os.makedirs(os.path.dirname(caminho) or destino, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(fonte)
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
    partes = [CABECALHO]
    for nome in FONTES:
        texto = open(os.path.join(RAIZ, nome), encoding="utf-8").read()
        partes.append(f"\n# {'=' * 100}\n# {nome}  ({texto.count(chr(10))} linhas)\n# {'=' * 100}\n"
                      f"FONTES[{nome!r}] = {literal(texto)}\n")
    partes.append(RODAPE)
    with open(os.path.join(RAIZ, saida), "w", encoding="utf-8") as f:
        f.write("".join(partes))
    return saida


if __name__ == "__main__":
    print(gerar())
