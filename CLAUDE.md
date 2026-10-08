# GISELE — convenções do projeto

Série de perguntas e respostas sobre como construir uma AGI/ASI, em português.

## Formato de cada nova parte
- Um novo arquivo `ASI_AGI_parteN_<tema>.md`, continuando a numeração das perguntas (Pn).
- Cada resposta tem três camadas: **Lógica** (equações e cálculos), **Tradução cruzada**
  (psicologia/filosofia como matemática; física/química/biologia como psicologia/filosofia)
  e **Meta** (suposições, confiança, onde pode estar errado).
- Ir mais fundo que a parte anterior; indicar de qual pergunta anterior a nova nasceu (↩ Pn).
- Ligar a nova parte a partir da anterior.

## Código (sempre)
- Todo número citado deve sair de uma função `pNN_...` em `calculos.py` (só biblioteca padrão).
- Simulações usam semente fixa; não trocar a semente para obter um resultado mais bonito.
- Depois de mudar o código: `python3 calculos.py > resultados.txt` e commitar os dois.
- Se a simulação discordar do texto, corrigir o texto e registrar a correção.
