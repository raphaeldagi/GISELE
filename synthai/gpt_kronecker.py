"""A forma de GPT com embeddings de Kronecker por nibble (Parte 76; ↩ P1695).

O embedding do caractere de byte b é o produto de Kronecker de dois fatores: A[b ≫ 4] (d₁ números, o nibble alto) e B[b & 0x0F] (d₂ números, o nibble
baixo), com d = d₁·d₂; a coordenada (i, j) do embedding é A[alto][i]·B[baixo][j], na posição i·d₂ + j. A ideia veio de um texto recebido na Parte 75;
aqui ela é medida, não suposta.

Tudo o mais é o GPT de synthai/gpt.py (herdado: a mesma ida, a mesma volta, o mesmo Adam). A diferença: antes de cada ida, E é refeita a partir de A e B;
depois de cada volta, o gradiente de E é levado a A e B pela regra da cadeia:
    ∂L/∂A[h][i] = Σ_c [alto(c) = h] Σ_j ∂L/∂E[c][i·d₂ + j] · B[baixo(c)][j]
    ∂L/∂B[l][j] = Σ_c [baixo(c) = l] Σ_i ∂L/∂E[c][i·d₂ + j] · A[alto(c)][i]
e o gradiente de E é zerado (E não é um parâmetro livre: o Adam não a move). Só biblioteca padrão."""

import math
import random

from synthai.gpt import GPT, _zeros


class GPTKronecker(GPT):
    def __init__(self, vocab, T=16, d1=4, d2=4, h=32, semente=69):
        super().__init__(vocab, T=T, d=d1 * d2, h=h, semente=semente)
        r = random.Random(semente + 1)
        self.d1, self.d2 = d1, d2
        self.alto = [ord(ch) >> 4 for ch in vocab]
        self.baixo = [ord(ch) & 0x0F for ch in vocab]
        if max(ord(ch) for ch in vocab) > 255:
            raise ValueError("o vocabulário precisa caber num byte")
        # escala: o produto de dois fatores com desvio s tem desvio s², e o E do GPT nasce com desvio 0,3
        s = math.sqrt(0.3)
        self.p["A"] = [[r.gauss(0.0, s) for _ in range(d1)] for _ in range(16)]
        self.p["B"] = [[r.gauss(0.0, s) for _ in range(d2)] for _ in range(16)]
        for k in ("A", "B"):
            self.m[k] = _zeros(16, len(self.p[k][0]))
            self.v[k] = _zeros(16, len(self.p[k][0]))
        self._refazer_E()

    def _refazer_E(self):
        A, B, d2 = self.p["A"], self.p["B"], self.d2
        for c in range(len(self.vocab)):
            a, b = A[self.alto[c]], B[self.baixo[c]]
            linha = self.p["E"][c]
            for i in range(self.d1):
                for j in range(d2):
                    linha[i * d2 + j] = a[i] * b[j]

    def adiante(self, x, exp=math.exp):
        self._refazer_E()
        return super().adiante(x, exp)

    def gradiente(self, x, y):
        perda, G = super().gradiente(x, y)
        A, B, d2 = self.p["A"], self.p["B"], self.d2
        GA, GB = _zeros(16, self.d1), _zeros(16, d2)
        for c in range(len(self.vocab)):
            gE = G["E"][c]
            h, l = self.alto[c], self.baixo[c]
            for i in range(self.d1):
                for j in range(d2):
                    g = gE[i * d2 + j]
                    if g != 0.0:
                        GA[h][i] += g * B[l][j]
                        GB[l][j] += g * A[h][i]
            G["E"][c] = [0.0] * len(gE)
        G["A"], G["B"] = GA, GB
        return perda, G

    def adam(self, G, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
        super().adam(G, lr, b1, b2, eps)
        self._refazer_E()

    def pesos_de_embedding(self):
        """(pesos efetivamente usados pelos embeddings de Kronecker, pesos de uma tabela cheia V × d): só contam as linhas de A e B de nibbles que
        aparecem no vocabulário."""
        return len(set(self.alto)) * self.d1 + len(set(self.baixo)) * self.d2, len(self.vocab) * self.d1 * self.d2
