#!/usr/bin/env python3
"""Monta SYNTHAI_GPT.py: cabeçalho do produto + laboratório NEXUS-RAPHAEL 3.0.0 + motor GPT + testes e CLI."""
from pathlib import Path
import sys

AQUI = Path(__file__).resolve().parent
NEXUS = AQUI.parent / "nexus_raphael_3" / "nexus_raphael.py"
SAIDA = AQUI / "SYNTHAI_GPT.py"


def montar() -> str:
    nexus = NEXUS.read_text(encoding="utf-8")
    ini = nexus.index('"""NEXUS')
    fim = nexus.index('"""', ini + 3) + 3
    cabecalho = (AQUI / "partes" / "g0_cabecalho.txt").read_text(encoding="utf-8").strip()
    corpo = nexus[:ini] + cabecalho + nexus[fim:]
    corte = corpo.index('\nif __name__ == "__main__":')
    corpo = corpo[:corte].rstrip() + "\n"
    for p in ("g1_motor.py", "g2_produto.py", "g3_testes_cli.py"):
        corpo += (AQUI / "partes" / p).read_text(encoding="utf-8").rstrip() + "\n"
    corpo += '''

if __name__ == "__main__":
    try:
        sys.exit(principal_unificado())
    except (ValueError, OSError, sqlite3.Error, TimeoutError) as erro:
        print(serie_json({"erro": str(erro), "tipo": type(erro).__name__}), file=sys.stderr)
        sys.exit(2)
'''
    return corpo


if __name__ == "__main__":
    t = montar()
    SAIDA.write_text(t, encoding="utf-8")
    print(SAIDA, len(t.splitlines()), "linhas")
    sys.exit(0)
