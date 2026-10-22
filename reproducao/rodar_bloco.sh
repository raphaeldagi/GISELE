#!/bin/bash
# roda um bloco de partes no clone limpo; pula se já concluído (marca FIM_OK)
R=/tmp/claude-0/-home-user-GISELE/bf182fb7-673a-58ba-807e-9361a8b43d3e/scratchpad/reproducao
nome=$(echo "$*" | tr ' ' '_')
out=$R/saidas/bloco_$nome.txt
if grep -q "^FIM_OK" "$out" 2>/dev/null; then exit 0; fi
cd $R/GISELE
inicio=$(date +%s)
python3 calculos.py "$@" > "$out" 2>&1
st=$?
echo "FIM_OK status=$st segundos=$(( $(date +%s) - inicio ))" >> "$out"
