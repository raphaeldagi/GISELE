"""Rodada 89 do diálogo Python <-> Java (Parte 122): a decomposição de Murphy COMPLETA do Brier (BS = REL − RES + UNC + WBV − WBC),
bit a bit. Previsões p = x/2³¹ de um LCG, eventos y = [u < p·p] (outro sorteio do mesmo LCG), N = 3000, 10 faixas. Somas em laço sequencial
(o sum() do Python 3.12 é compensado: Parte 34). Imprime as sete grandezas em hexadecimal. Da raiz: python3 dialogo/rodada89.py"""

N = 3000
FAIXAS = 10
SEMENTE = 1221


def dados():
    x = SEMENTE
    p, y = [], []
    for _ in range(N):
        x = (1103515245 * x + 12345) % 2147483648
        q = x / 2147483648.0
        x = (1103515245 * x + 12345) % 2147483648
        u = x / 2147483648.0
        p.append(q)
        y.append(1 if u < q * q else 0)
    return p, y


def decompor(p, y):
    n = len(p)
    soma_y = 0
    for v in y:
        soma_y += v
    obar = soma_y / n
    grupos = [[] for _ in range(FAIXAS)]
    for q, v in zip(p, y):
        k = int(q * FAIXAS)
        grupos[k if k < FAIXAS else FAIXAS - 1].append((q, v))
    rel = res = wbv = wbc = 0.0
    for g in grupos:
        if not g:
            continue
        nk = len(g)
        sp = 0.0
        so = 0
        for q, v in g:
            sp += q
            so += v
        pk = sp / nk
        ok = so / nk
        rel += nk * ((pk - ok) * (pk - ok))
        res += nk * ((ok - obar) * (ok - obar))
        for q, v in g:
            wbv += (q - pk) * (q - pk)
            wbc += 2.0 * ((q - pk) * (v - ok))
    rel, res, wbv, wbc = rel / n, res / n, wbv / n, wbc / n
    unc = obar * (1.0 - obar)
    bs = 0.0
    for q, v in zip(p, y):
        bs += (q - v) * (q - v)
    bs = bs / n
    return bs, rel, res, unc, wbv, wbc, rel - res + unc + wbv - wbc


def main():
    p, y = dados()
    nomes = ("brier", "rel", "res", "unc", "wbv", "wbc", "soma")
    for nome, v in zip(nomes, decompor(p, y)):
        print(nome + " " + v.hex())
    print("fim")


if __name__ == "__main__":
    main()
