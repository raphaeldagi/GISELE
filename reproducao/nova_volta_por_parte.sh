#!/bin/bash
# Uma volta do loop com UMA PARTE POR PROCESSO (Parte 131: o contêiner reinicia a cada ~30 min e mata blocos longos).
# Cada parte roda isolada (python3 -c "import calculos; calculos.PARTES[k]()"), num arquivo bloco_K_.txt com marca FIM_OK;
# a unificação (regressão) roda uma vez, em unificacao.txt. Retomável: o que tem FIM_OK é pulado.
# Uso: reproducao/nova_volta_por_parte.sh N COMMIT
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
open(sys.argv[1] + "/partes.txt", "w").write("\n".join(map(str, ks)) + "\nunificacao\n")
PY
cat > $R/rodar_parte.sh <<EOS
#!/bin/bash
k=\$1
if [ "\$k" = unificacao ]; then out=$R/saidas/unificacao.txt; cmd="import calculos; calculos._unificacao()"; else out=$R/saidas/bloco_\${k}_.txt; cmd="import calculos; calculos.PARTES[\$k]()"; fi
grep -q "^FIM_OK" "\$out" 2>/dev/null && exit 0
cd $R/GISELE; inicio=\$(date +%s); python3 -c "\$cmd" > "\$out" 2>&1; st=\$?
echo "FIM_OK status=\$st segundos=\$(( \$(date +%s) - inicio ))" >> "\$out"
EOS
chmod +x $R/rodar_parte.sh
(xargs -P 3 -L 1 $R/rodar_parte.sh < $R/partes.txt; echo TUDO_FIM > $R/saidas/TUDO_FIM) > $R/driver.log 2>&1 &
[ -x $R/rodar_testes.sh ] && $R/rodar_testes.sh > $R/testes.log 2>&1 &
wait
