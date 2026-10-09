"""Rodada 4 do diálogo Python <-> Java: a auditoria da arquitetura "pós-ASI" (externos/arquitetura_pos_asi.py), em Python
pelo módulo ast (synthai/rsi.py, auditar_ast; nada é executado), e o selo do avaliador externo (o SHA-256 do código de
regret_do_genoma, como o AvaliadorSelado o calcula). Rodar da raiz do repositório: python3 dialogo/rodada04.py"""

import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from synthai.rsi import AvaliadorSelado, auditar_ast  # noqa: E402

r = auditar_ast(os.path.join(RAIZ, "externos", "arquitetura_pos_asi.py"))
print(f"transformador devolve o no: {r['transformador_so_devolve_o_no']}")
print(f"nos mudados: {r['nos_mudados']}")
print(f"texto mutado: {', '.join(r['texto_mutado'])}")
print(f"run_benchmarks constante: {float(r['run_benchmarks_constante']).hex()}")
print(f"avaliador pergunta ao agente: {r['avaliador_pergunta_ao_agente']}")
print(f"selo do avaliador: {AvaliadorSelado.assinatura()}")
