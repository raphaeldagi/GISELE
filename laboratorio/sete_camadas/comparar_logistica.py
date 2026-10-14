"""Parte 83 (P1935): o módulo sete_camadas.py recebido do usuário (cópia fiel, nesta pasta), auditado pela árvore sintática antes de rodar, contra dois
controles. (j) o modo síncrono e o assíncrono dele, mesma semente, dão o mesmo resultado? (k, l) uma regressão logística de 5 parâmetros (Python puro;
o NumPy entra só para gerar os MESMOS dados dele) nos mesmos 512 exemplos de treino, avaliada na mesma confirmação, limpa e sob o pior ataque ℓ∞ de 0,15
(exato para um modelo linear: x − ε·sinal(w)·(2y − 1)). Imprime um JSON. Rodar: python3 laboratorio/sete_camadas/comparar_logistica.py"""

import asyncio
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sete_camadas as s  # noqa: E402


def logistica(x, y, passos=3000, taxa=0.5):
    w, b, n = [0.0] * 4, 0.0, len(x)
    for _ in range(passos):
        gw, gb = [0.0] * 4, 0.0
        for xi, yi in zip(x, y):
            z = b + sum(wj * xj for wj, xj in zip(w, xi))
            p = 1.0 / (1.0 + math.exp(-z)) if z >= 0 else math.exp(z) / (1.0 + math.exp(z))
            d = p - yi
            gb += d
            for j in range(4):
                gw[j] += d * xi[j]
        b -= taxa * gb / n
        w = [wj - taxa * g / n for wj, g in zip(w, gw)]
    return w, b


def acerto(w, b, x, y, eps=0.0):
    ok = 0
    for xi, yi in zip(x, y):
        s_ = 1.0 if yi else -1.0
        xa = [xj - eps * s_ * (1.0 if wj > 0 else -1.0 if wj < 0 else 0.0) for xj, wj in zip(xi, w)]
        z = b + sum(wj * xj for wj, xj in zip(w, xa))
        ok += (z >= 0) == bool(yi)
    return ok / len(x)


def main():
    semente = 42
    xt, yt = s.dados(semente + 11, 512)
    xc, yc = s.dados(semente + 53, 512)
    xt, yt = xt.tolist(), [float(v[0]) for v in yt.tolist()]
    xc, yc = xc.tolist(), [float(v[0]) for v in yc.tolist()]
    w, b = logistica(xt, yt)
    saida = {"logistica_pesos": w + [b], "logistica_limpa": acerto(w, b, xc, yc), "logistica_adversa": acerto(w, b, xc, yc, 0.15)}
    rs = {}
    for modo in ("sincrono", "assincrono"):
        r = asyncio.run(s.executar(s.Configuracao(semente=semente, modo=modo)))
        r.pop("segundos")
        for t in r["tracos"]:
            t.pop("modo")
        rs[modo] = r
    saida["modos_identicos"] = json.dumps(rs["sincrono"], sort_keys=True) == json.dumps(rs["assincrono"], sort_keys=True)
    saida["rede_limpa"] = rs["sincrono"]["confirmacao"]["acuracia"]
    saida["rede_adversa"] = rs["sincrono"]["confirmacao"]["adversa"]
    saida["ciclos"] = rs["sincrono"]["ciclos_executados"]
    print(json.dumps(saida))


if __name__ == "__main__":
    main()
