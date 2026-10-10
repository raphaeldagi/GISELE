"""Rodada 9 do diálogo Python <-> Java: a média bayesiana de modelos (synthai/decisao.py, ThompsonMistura, P541): quatro
ThompsonBOCPD com H em {0, 1/2000, 1/500, 1/100}, pesos pela soma dos logs das preditivas. Três braços em rodízio,
recompensas do gerador da rodada 5 (semente 909), médias trocadas no passo 600. Imprime os log-pesos, as perdas de cada
modelo e a da mistura, e os pesos normalizados, em hexadecimal. Rodar da raiz: python3 dialogo/rodada09.py

Parte 77: a versão original importava a ThompsonMistura de synthai/decisao.py, que usa o exp e o log da biblioteca (a fronteira
da Parte 52: passava por sorte). Esta versão copia as duas classes, só com o que a rodada usa (atualizar e pesos), trocando exp e
log pelos próprios de dialogo/exatas.py; o synthai/decisao.py fica intacto. O sum() continua (compensado no Python 3.12+), porque
o Java já o reproduz com a soma compensada da rodada 5. A original está em dialogo/registro/rodada09_libm.py."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exatas import exp_, log_  # noqa: E402
from rodada05 import LCG  # noqa: E402


class BOCPD:
    """A ThompsonBOCPD de synthai/decisao.py, sem o sorteio (a rodada não escolhe braços: eles vêm em rodízio)."""

    def __init__(self, k, risco, hipoteses=16):
        self.risco, self.hipoteses = risco, hipoteses
        self.mist = [[[1.0, 1.0, 1.0]] for _ in range(k)]

    def _risco(self, hs):
        H = self.risco
        for h in hs:
            h[0] *= 1 - H
        for h in hs:
            if h[1] == 1.0 and h[2] == 1.0:
                h[0] += H
                return
        hs.append([H, 1.0, 1.0])

    def atualizar(self, braco, r):
        for hs in self.mist:
            self._risco(hs)
        hs = self.mist[braco]
        for h in hs:
            h[0] *= (h[1] if r else h[2]) / (h[1] + h[2])
            if r:
                h[1] += 1
            else:
                h[2] += 1
        hs.sort(key=lambda h: -h[0])
        del hs[self.hipoteses:]
        tot = sum(h[0] for h in hs)
        for h in hs:
            h[0] /= tot
        for i, outro in enumerate(self.mist):
            if i != braco and len(outro) > self.hipoteses:
                outro.sort(key=lambda h: -h[0])
                del outro[self.hipoteses:]
                tot = sum(h[0] for h in outro)
                for h in outro:
                    h[0] /= tot


class Mistura:
    """A ThompsonMistura de synthai/decisao.py (atualizar e pesos), com exp_ e log_."""

    def __init__(self, k, riscos=(0.0, 1 / 2000, 1 / 500, 1 / 100), hipoteses=16):
        self.modelos = [BOCPD(k, h, hipoteses) for h in riscos]
        self.riscos = riscos
        self.logw = [0.0] * len(riscos)
        self.perda = [0.0] * len(riscos)
        self.perda_mistura = 0.0

    def pesos(self):
        m = max(self.logw)
        e = [exp_(x - m) for x in self.logw]
        t = sum(e)
        return [x / t for x in e]

    def atualizar(self, braco, r):
        ws = self.pesos()
        preds = []
        for mod, H in zip(self.modelos, self.riscos):
            hs = mod.mist[braco]
            pr = sum(h[0] * ((h[1] if r else h[2]) / (h[1] + h[2])) for h in hs)
            preds.append((1 - H) * pr + H * 0.5)
        self.perda_mistura -= log_(sum(w * p for w, p in zip(ws, preds)))
        for i, p in enumerate(preds):
            self.logw[i] += log_(p)
            self.perda[i] -= log_(p)
        for mod in self.modelos:
            mod.atualizar(braco, r)


def main():
    g = LCG(909)
    t = Mistura(3)
    for passo in range(1200):
        ps = (0.2, 0.5, 0.8) if passo < 600 else (0.8, 0.5, 0.2)
        braco = passo % 3
        t.atualizar(braco, 1 if g.uniforme() < ps[braco] else 0)
    print("logw = " + " ".join(x.hex() for x in t.logw))
    print("perda = " + " ".join(x.hex() for x in t.perda))
    print("perda da mistura = " + t.perda_mistura.hex())
    print("pesos = " + " ".join(x.hex() for x in t.pesos()))


if __name__ == "__main__":
    main()
