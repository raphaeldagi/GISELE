#!/bin/bash
R=/tmp/claude-0/-home-user-GISELE/bf182fb7-673a-58ba-807e-9361a8b43d3e/scratchpad/reproducao
xargs -P 3 -L 1 $R/rodar_bloco.sh < $R/blocos.txt
echo TUDO_FIM > $R/saidas/TUDO_FIM
