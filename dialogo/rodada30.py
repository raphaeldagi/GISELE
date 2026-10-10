"""Rodada 30 do diálogo Python <-> Java: os empates nas escolhas das rodadas antigas. Para as rodadas que escolhem (12, 14,
18, 19, 20, 24), recalcula os valores de que a escolha impressa depende: nas listas ordenadas, os valores dos k primeiros e
do (k+1)-ésimo (a fronteira); nos máximos, o melhor e o segundo. Um empate é um par de vizinhos com o MESMO valor bit a bit:
a escolha entre eles é decidida pela regra de desempate, não pelo valor. Com `--preparar PASTA` escreve PASTA/valores30.txt
(rodada TAB grupo TAB valores em hexadecimal); sem argumento, conta os empates a partir do mesmo arquivo gerado em memória.
Rodar da raiz do repositório: python3 dialogo/rodada30.py"""

import importlib.util
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, RAIZ)


def _carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(AQUI, nome + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def grupos():
    """[(rodada, grupo, [valores em ordem de escolha])]."""
    import calculos
    from synthai.engenharia_reversa import padroes_repetidos
    from synthai.semiotica import trigramas_de_forma
    res = []
    # 12: os 12 4-gramas (documentos, ocorrências) e o 13º, a fronteira; o valor é documentos·10⁶ + ocorrências (exato em double)
    docs, _ = calculos._meus_textos()
    res.append(("12", "4-gramas", [float(nd * 1000000 + nt) for _, nd, nt in padroes_repetidos(docs, 4, topo=13)]))
    # 14: os pesos da P732 (o mesmo cálculo de calculos.p732_trigramas), os 13 mais e os 13 menos "animais"
    ca, co = {}, {}
    for lema, y in calculos._formas_732():
        for t in trigramas_de_forma(lema):
            (ca if y else co)[t] = (ca if y else co).get(t, 0) + 1
    voc = set(ca) | set(co)
    na, no, v = sum(ca.values()), sum(co.values()), len(voc)
    peso = {t: math.log((ca.get(t, 0) + 1) / (na + v)) - math.log((co.get(t, 0) + 1) / (no + v)) for t in voc}
    ok = sorted((t for t in voc if ca.get(t, 0) + co.get(t, 0) >= 10), key=lambda t: (-peso[t], t))
    res.append(("14", "mais-animais", [peso[t] for t in ok[:13]]))
    res.append(("14", "menos-animais", [peso[t] for t in ok[::-1][:13]]))
    # 18 e 19: em cada seção, o melhor e o segundo escore entre os documentos
    for nome in ("rodada18", "rodada19"):
        r = _carregar(nome)
        dc, sec = r.documentos(), r.secoes()
        partes = sorted(k for k in dc if k in sec)
        dn = {k: r.numeros(open(os.path.join(RAIZ, dc[k]), encoding="utf-8").read()) for k in partes}
        df = {}
        for k in partes:
            for t in dn[k]:
                df[t] = df.get(t, 0) + 1
        for n in partes:
            rr = r.numeros(sec[n])
            esc = []
            for k in partes:
                s = 0.0
                for t in sorted(rr & dn[k]):
                    s += math.log(len(partes) / df[t])
                esc.append(s)
            esc.sort(reverse=True)
            res.append((nome[-2:], f"parte{n}", esc[:2]))
    # 20: a diferença de escore entre as duas épocas (empate = diferença zero: dois valores iguais, escore(1) e escore(2))
    r20 = _carregar("rodada20")
    for n, ep, pv, dif in r20.deixar_um_de_fora(r20.dados()):
        res.append(("20", f"parte{n}", [dif, 0.0]))
    # 24: o melhor e o segundo documento escolhidos pelo texto
    r24 = _carregar("rodada24")
    ds, texto = r24.dados()
    esc = sorted((s for _, s in r24.pontuar(ds, texto)), reverse=True)
    res.append(("24", "texto", esc[:2]))
    return res


def contar(linhas):
    """Empates por rodada: pares de vizinhos com o mesmo valor bit a bit, em cada grupo."""
    por = {}
    for r, g, vals in linhas:
        e = sum(1 for a, b in zip(vals, vals[1:]) if a == b)
        por[r] = por.get(r, 0) + e
    return por


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--preparar":
        with open(os.path.join(sys.argv[2], "valores30.txt"), "w", encoding="ascii") as f:
            for r, g, vals in grupos():
                f.write(f"{r}\t{g}\t{' '.join(x.hex() for x in vals)}\n")
        return
    linhas = []
    if len(sys.argv) == 2:
        for l in open(os.path.join(sys.argv[1], "valores30.txt"), encoding="ascii").read().split("\n"):
            if l:
                r, g, vs = l.split("\t")
                linhas.append((r, g, [float.fromhex(x) for x in vs.split(" ")]))
    else:
        linhas = grupos()
    por = contar(linhas)
    for r in sorted(por):
        print(f"rodada{r}: {por[r]} empates")
    print(f"rodadas com empate na escolha impressa: {sum(1 for x in por.values() if x > 0)} de {len(por)}")


if __name__ == "__main__":
    main()
