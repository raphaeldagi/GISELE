# Upload recebido (SYNTHAI_consolidado_v0_15_0.py) — auditado SEM executar (Parte 102)

Pedido do usuário: "Veja se algo serve". Pacote consolidado (7,2 MB, 190 módulos .py + 407 arquivos no zip base85).
É um FORK/superset que mescla o meu trabalho antigo (synthai/* até ~Parte 68, rodadas 1-42, calculos.py) com a família de módulos recebida.

## Auditoria de capacidade (AST, sem executar), sobre TODOS os 190 .py
- RECUSADOS (regra da Parte 84/93): `domestico.py` + `testes_domestico.py` (urllib/http: REDE de saída); `trabalho_continuo.py` (subprocess.Popen de si mesmo: auto-relançamento/replicação). NÃO executados, NÃO integrados.
- subprocess legítimo (não integrado, mas inócuo): dialogo/verificar.py (javac), synthai_cli.py, laboratorio/testar.py, testes_bloqueio_checkpoint.
- eval/exec: só na cópia-espelho de calculos.py (p1608 usa ast, não eval) e no relatório externos/arquitetura_pos_asi.py (dado, auditado na Parte 50). socket: nenhum.

## O que JÁ está no meu projeto (ideias reimplementadas em biblioteca padrão, seguras)
- modelo_mundo → Partes 93-98 (synthai/mundo.py). sete_camadas → Parte 83. recursiva_paraconsistente/LFI1 → Partes 88/101 (synthai/autopoiese.py).
- compressao/quantização → Partes 87/95. inovacao/otimizacao/annealing → Partes 84/87. rl_grupos/GRPO → Parte 87.
- metacognicao_algebra_geometria → Partes 70/83. gradientes_inferencias → Partes 34/91. paradoxos/auditoria_logica → Parte 88.

## CANDIDATOS novos e seguros a reimplementar (stdlib, sem rede/replicação)
- workspace_global.py (GWT/RPT/AST: um "quadro-negro" global que transmite a saída vencedora a todos os módulos) — NOVO e no tema AGI; só argparse+deque. ESCOLHIDO para a Parte 102.
- neurossimbolico.py; extensao_curvatura.py / controle_adaptativo.py / objetivos_cognitivos.py (usam numpy — reimplementar sem numpy); transferencia_metacognitiva.py.

Fontes guardadas como DADO em externos/pacote_v015/ (workspace_global, neurossimbolico, objetivos_cognitivos). NUNCA executados.
