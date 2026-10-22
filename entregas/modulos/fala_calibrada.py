"""SYNTHAI — módulo FALA COM CONFIANÇA CALIBRADA (Parte 124). Arquivo único, só biblioteca padrão.

Um agente que fala "certo", "quase certo", "provavelmente", "talvez" só é útil se, quando diz "quase certo", acerta
quase sempre. Este módulo mede a calibração (ECE, Brier) de um classificador excessivamente confiante e a conserta de dois
jeitos, ambos ajustados num conjunto de calibração separado:
- Platt (1999): p = σ(a·logit(p_bruta) + b), por Newton (problema convexo, solução exata);
- regressão isotônica (PAV, pool-adjacent-violators): a melhor função monótona, sem supor forma.
Depois traduz a probabilidade calibrada em palavras com faixas fixas e confere a frequência de acerto dentro de cada palavra.

Conta fechada: se a verdade é p = σ(z) e o classificador diz σ(3z) (confiança triplicada no logit), o Platt recupera a = 1/3, b = 0.

Uso:  python3 fala_calibrada.py           (demonstração)
      python3 fala_calibrada.py --testes  (testes de unidade)
"""

import math
import random
import sys
import unittest

PALAVRAS = (("talvez", 0.5, 0.65), ("provavelmente", 0.65, 0.8), ("muito provavelmente", 0.8, 0.9),
            ("quase certo", 0.9, 0.97), ("certo", 0.97, 1.0001))


def sigmoide(x):
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def logit(p, eps=1e-12):
    p = min(1 - eps, max(eps, p))
    return math.log(p / (1 - p))


def gerar(n, exagero=3.0, desvio=2.0, semente=0):
    """(p_bruta, y): z ~ N(0, desvio); y ~ Bernoulli(σ(z)); o classificador diz σ(exagero·z)."""
    rng = random.Random(semente)
    dados = []
    for _ in range(n):
        z = rng.gauss(0, desvio)
        y = 1 if rng.random() < sigmoide(z) else 0
        dados.append((sigmoide(exagero * z), y))
    return dados


def brier(ps, ys):
    return sum((p - y) ** 2 for p, y in zip(ps, ys)) / len(ys)


def ece(ps, ys, caixas=10):
    """Erro de calibração esperado sobre a CONFIANÇA da classe prevista (max(p, 1−p)), caixas iguais em [0,5; 1]."""
    soma = [0.0] * caixas
    acerto = [0.0] * caixas
    cont = [0] * caixas
    for p, y in zip(ps, ys):
        conf = max(p, 1 - p)
        certo = (p >= 0.5) == (y == 1)
        i = min(caixas - 1, int((conf - 0.5) * 2 * caixas))
        soma[i] += conf
        acerto[i] += certo
        cont[i] += 1
    n = len(ys)
    return sum(abs(soma[i] - acerto[i]) for i in range(caixas) if cont[i]) / n


class Platt:
    """Logística sobre logit(p_bruta), ajustada por Newton (2 parâmetros, Hessiana 2×2)."""

    def __init__(self):
        self.a, self.b = 1.0, 0.0

    def ajustar(self, ps, ys, passos=100):
        """Newton com busca linear (corta o passo pela metade até a perda logarítmica cair). O Newton puro, partindo de a = 1,
        diverge quando os logits são grandes (|x| ~ 20): o passo cheio salta para a = 77 e a Hessiana zera em ponto flutuante."""
        xs = [logit(p) for p in ps]

        def perda(a, b):
            t = 0.0
            for x, y in zip(xs, ys):
                z = a * x + b
                t += (math.log1p(math.exp(-abs(z))) + max(z, 0.0)) - y * z      # ln(1 + e^z) − y·z, estável
            return t

        a, b = 1.0, 0.0
        atual = perda(a, b)
        for _ in range(passos):
            ga = gb = haa = hab = hbb = 0.0
            for x, y in zip(xs, ys):
                q = sigmoide(a * x + b)
                r = q - y
                w = q * (1 - q)
                ga += r * x
                gb += r
                haa += w * x * x
                hab += w * x
                hbb += w
            det = haa * hbb - hab * hab
            if det <= 0:
                break
            da = (hbb * ga - hab * gb) / det
            db = (haa * gb - hab * ga) / det
            passo = 1.0
            while passo > 1e-12:
                na, nb = a - passo * da, b - passo * db
                nova = perda(na, nb)
                if nova <= atual:
                    break
                passo /= 2
            else:
                break
            a, b, atual = na, nb, nova
            if abs(passo * da) + abs(passo * db) < 1e-13:
                break
        self.a, self.b = a, b
        return self

    def __call__(self, p):
        return sigmoide(self.a * logit(p) + self.b)


class Isotonica:
    """PAV: blocos com média monótona em p_bruta; prevê pela média do bloco (degrau)."""

    def ajustar(self, ps, ys):
        pares = sorted(zip(ps, ys))
        blocos = []                     # [soma_y, n, p_min, p_max]
        for p, y in pares:
            blocos.append([float(y), 1, p, p])
            while len(blocos) > 1 and blocos[-2][0] / blocos[-2][1] >= blocos[-1][0] / blocos[-1][1]:
                s, n, lo, hi = blocos.pop()
                blocos[-1][0] += s
                blocos[-1][1] += n
                blocos[-1][3] = hi
        self.limites = [b[3] for b in blocos]
        self.valores = [b[0] / b[1] for b in blocos]
        return self

    def __call__(self, p):
        lo, hi = 0, len(self.limites) - 1
        while lo < hi:
            m = (lo + hi) // 2
            if self.limites[m] < p:
                lo = m + 1
            else:
                hi = m
        return self.valores[lo]


def palavra(p):
    conf = max(p, 1 - p)
    for nome, lo, hi in PALAVRAS:
        if lo <= conf < hi:
            return nome
    return PALAVRAS[-1][0]


def tabela_de_palavras(ps, ys):
    """Para cada palavra: (vezes dita, fração de acerto da classe prevista)."""
    tab = {}
    for p, y in zip(ps, ys):
        w = palavra(p)
        n, a = tab.get(w, (0, 0))
        tab[w] = (n + 1, a + ((p >= 0.5) == (y == 1)))
    return {w: (n, a / n) for w, (n, a) in tab.items()}


def demonstracao():
    cal = gerar(5000, semente=1)
    tes = gerar(20000, semente=2)
    pc, yc = zip(*cal)
    pt, yt = zip(*tes)
    platt = Platt().ajustar(pc, yc)
    iso = Isotonica().ajustar(pc, yc)
    print(f"Platt: a = {platt.a:.4f} (conta fechada 1/3 = 0,3333), b = {platt.b:+.4f} (conta: 0)")
    for nome, f in (("bruta", lambda p: p), ("Platt", platt), ("isotônica", iso)):
        q = [f(p) for p in pt]
        print(f"  {nome:>10}: ECE {ece(q, yt):.4f}  Brier {brier(q, yt):.4f}")
    print("Palavras (Platt) — vezes dita e acerto real; a faixa nominal entre parênteses:")
    tab = tabela_de_palavras([platt(p) for p in pt], yt)
    for nome, lo, hi in PALAVRAS:
        if nome in tab:
            n, a = tab[nome]
            print(f"  {nome:>20}: {n:>6}  acerto {a:.3f}  ({lo:.2f}–{min(hi, 1):.2f})")
    tab = tabela_de_palavras(pt, yt)
    print("Palavras (bruta, sem calibrar):")
    for nome, lo, hi in PALAVRAS:
        if nome in tab:
            n, a = tab[nome]
            print(f"  {nome:>20}: {n:>6}  acerto {a:.3f}  ({lo:.2f}–{min(hi, 1):.2f})")


class Testes(unittest.TestCase):
    def test_platt_identidade(self):
        # dados já calibrados (exagero 1): a ~ 1, b ~ 0
        d = gerar(20000, exagero=1.0, semente=3)
        pl = Platt().ajustar(*zip(*d))
        self.assertAlmostEqual(pl.a, 1.0, delta=0.06)
        self.assertAlmostEqual(pl.b, 0.0, delta=0.06)

    def test_platt_gradiente_zero_no_otimo(self):
        d = gerar(3000, semente=4)
        ps, ys = zip(*d)
        pl = Platt().ajustar(ps, ys)
        g = sum((pl(p) - y) for p, y in zip(ps, ys))
        self.assertLess(abs(g), 1e-8)

    def test_pav_e_monotona_e_conserva_a_media(self):
        d = gerar(2000, semente=5)
        ps, ys = zip(*d)
        iso = Isotonica().ajustar(ps, ys)
        self.assertTrue(all(a <= b for a, b in zip(iso.valores, iso.valores[1:])))
        self.assertAlmostEqual(sum(iso(p) for p in ps), sum(ys), delta=1e-6)

    def test_ece_zero_num_caso_perfeito(self):
        ps = [0.75] * 4 + [0.25] * 4
        ys = [1, 1, 1, 0, 0, 0, 0, 1]
        self.assertAlmostEqual(ece(ps, ys), 0.0)

    def test_palavras_cobrem_a_faixa(self):
        for p in (0.5, 0.6, 0.7, 0.85, 0.95, 0.999, 1.0, 0.0, 0.3):
            self.assertIn(palavra(p), [w for w, _, _ in PALAVRAS])

    def test_calibrar_reduz_ece(self):
        cal, tes = gerar(3000, semente=6), gerar(3000, semente=7)
        pc, yc = zip(*cal)
        pt, yt = zip(*tes)
        pl = Platt().ajustar(pc, yc)
        self.assertLess(ece([pl(p) for p in pt], yt), ece(pt, yt))


if __name__ == "__main__":
    if "--testes" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        demonstracao()
