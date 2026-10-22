#!/bin/bash
# Uma volta do loop (Partes 128+): clone limpo do GitHub no commit dado, 16+ blocos retomáveis (3 em paralelo) e os testes.
# Uso: reproducao/nova_volta.sh N COMMIT   (as saídas ficam em $BASE/reproducaoN/saidas)
N=$1; COMMIT=$2
BASE=${BASE:-/tmp/claude-0/-home-user-GISELE/bf182fb7-673a-58ba-807e-9361a8b43d3e/scratchpad}
R=$BASE/reproducao$N
mkdir -p $R/saidas
if [ ! -d $R/GISELE ]; then
  git clone -q --branch claude/asi-agi-technical-questions-duan00 https://github.com/raphaeldagi/GISELE $R/GISELE && (cd $R/GISELE && git checkout -q $COMMIT)
fi
cd $R/GISELE
python3 - "$R" <<'PY'
import re, sys
s = open("calculos.py").read()
ks = sorted(set(int(k) for k in re.findall(r"(\d+): _parte_", s[s.index("PARTES = {"):][:20000]) + [int(k) for k in re.findall(r"PARTES\[(\d+)\] = _parte_", s)]))
open(sys.argv[1] + "/blocos.txt", "w").write("\n".join(" ".join(map(str, ks[j:j + 8])) for j in range(0, len(ks), 8)) + "\n")
PY
cat > $R/rodar_bloco.sh <<EOS
#!/bin/bash
nome=\$(echo "\$*" | tr ' ' '_'); out=$R/saidas/bloco_\$nome.txt
grep -q "^FIM_OK" "\$out" 2>/dev/null && exit 0
cd $R/GISELE; inicio=\$(date +%s); python3 calculos.py "\$@" > "\$out" 2>&1; st=\$?
echo "FIM_OK status=\$st segundos=\$(( \$(date +%s) - inicio ))" >> "\$out"
EOS
chmod +x $R/rodar_bloco.sh
MODS=$(grep -o "synthai\.testes[a-z0-9_]*" CLAUDE.md | sort -u | tr '\n' ' '); REV=$(ls synthai/revisado/testes_*_revisao.py | sed 's#/#.#g; s#\.py$##' | tr '\n' ' ')
cat > $R/rodar_testes.sh <<EOS
#!/bin/bash
cd $R/GISELE
t(){ out=$R/saidas/\$1; shift; grep -q "^FIM_OK" \$out 2>/dev/null && return; "\$@" > \$out 2>&1; echo "FIM_OK status=\$?" >> \$out; }
t testes_suite.txt python3 -m unittest $MODS $REV
t testes_lab.txt python3 laboratorio/testar.py
t dialogo.txt python3 dialogo/verificar.py
t testes_modulos.txt bash -c 'for f in entregas/modulos/*.py; do python3 -I \$f --testes || exit 1; done'
t testes_gpt.txt python3 -I entregas/synthai_gpt/SYNTHAI_GPT.py teste
t testes_nexus.txt python3 -I entregas/nexus_raphael_3/nexus_raphael.py teste
EOS
chmod +x $R/rodar_testes.sh
(xargs -P 3 -L 1 $R/rodar_bloco.sh < $R/blocos.txt; echo TUDO_FIM > $R/saidas/TUDO_FIM) > $R/driver.log 2>&1 &
$R/rodar_testes.sh > $R/testes.log 2>&1 &
wait
