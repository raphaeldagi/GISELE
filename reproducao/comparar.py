"""Compara, parte por parte, a saída refeita no clone limpo com o resultados.txt commitado (Parte 128)."""
import difflib, glob, json, re, sys
CAB = re.compile(r"^(?:---|===) Parte (\d+)\b")
FIM = re.compile(r"^=== Unifica")
def partes(texto, inicio=None):
    # a Parte 1 não tem cabeçalho: as linhas antes do primeiro cabeçalho são dela, quando o arquivo começa por ela
    d, atual = ({inicio: []}, inicio) if inicio else ({}, None)
    for l in texto.split("\n"):
        m = CAB.match(l)
        if m:
            atual = int(m.group(1)); d[atual] = []; continue
        if FIM.match(l) or l.startswith("FIM_OK"):
            atual = None; continue
        if atual is not None and l.strip() and "ResourceWarning" not in l and "tracemalloc" not in l and "return ds, sorted" not in l:
            d[atual].append(l)
    return d
ref = partes(open(sys.argv[1], encoding="utf-8").read(), inicio=1)
novo = {}
regs = []
for f in sorted(glob.glob(sys.argv[2] + "/bloco_*.txt")):
    t = open(f, encoding="utf-8").read()
    novo.update(partes(t, inicio=1 if f.split("/")[-1].startswith("bloco_1_") else None))
    regs += [(f.split("/")[-1], l) for l in t.split("\n") if l.startswith("Regressao:") or l.startswith("Traceback") or l.startswith("FIM_OK")]
tot = dif = 0
por_parte = {}
for k in sorted(novo):
    if k not in ref:
        por_parte[k] = ("sem referência", len(novo[k])); continue
    a, b = ref[k], novo[k]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    iguais = sum(m.size for m in sm.get_matching_blocks())
    tot += len(a); dif += len(a) - iguais
    if len(a) - iguais or len(a) != len(b):
        por_parte[k] = [(op, a[i1:i2], b[j1:j2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
print(json.dumps({"partes_refeitas": len(novo), "linhas_ref": tot, "linhas_diferentes": dif,
                  "fracao": dif / tot if tot else None, "partes_com_diferenca": sorted(k for k in por_parte if not isinstance(por_parte[k], tuple)),
                  "sem_referencia": [k for k in por_parte if isinstance(por_parte[k], tuple)]}, ensure_ascii=False))
for r in regs: print(r)
if len(sys.argv) > 3:
    for k, v in por_parte.items():
        print("\n## Parte", k)
        if isinstance(v, tuple): print(v); continue
        for op, x, y in v:
            print(op); [print("  - " + l[:200]) for l in x]; [print("  + " + l[:200]) for l in y]
