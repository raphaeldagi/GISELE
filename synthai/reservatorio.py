"""Peças de aprendizagem contínua do módulo recebido `externos/pacote3/aprendizagem_continua.py` (Parte 137), offline e em biblioteca padrão:
a memória por reservatório (amostra uniforme de um fluxo sem saber o tamanho dele), o posto efetivo exp(H(s/Σs)) dos valores singulares das
ativações centradas, a fração de unidades dormentes (atividade média ≤ limiar × média geral) e a medida de esquecimento de uma matriz de
acurácias. Os valores singulares reusam `synthai.contraposto_matrizes.valores_singulares` (Jacobi, Parte 117).
"""
import math
import random

from synthai.contraposto_matrizes import valores_singulares


class Reservatorio:
    """O algoritmo R de Vitter: os primeiros k entram; o n-ésimo substitui uma posição uniforme com probabilidade k/n."""

    def __init__(self, capacidade, semente=0):
        self.capacidade = capacidade
        self.rng = random.Random(semente)
        self.itens = []
        self.vistos = 0

    def adicionar(self, item):
        self.vistos += 1
        if len(self.itens) < self.capacidade:
            self.itens.append(item)
        else:
            j = self.rng.randrange(self.vistos)
            if j < self.capacidade:
                self.itens[j] = item


def posto_efetivo(ativacoes):
    """exp(H(p)) com p = s/Σs, s os valores singulares da matriz de ativações (amostras × unidades) centrada por coluna; 0 se Σs ≈ 0."""
    n, d = len(ativacoes), len(ativacoes[0])
    medias = [sum(l[j] for l in ativacoes) / n for j in range(d)]
    H = [[l[j] - medias[j] for j in range(d)] for l in ativacoes]
    s = [v for v in valores_singulares(H) if v > 0]
    soma = sum(s)
    if soma <= 1e-12:
        return 0.0
    return math.exp(-sum((v / soma) * math.log(v / soma) for v in s))


def fracao_dormente(ativacoes, limiar=0.12):
    """Fração das unidades com atividade média |h| ≤ limiar × a média das atividades (todas dormentes se a média é zero)."""
    n, d = len(ativacoes), len(ativacoes[0])
    atividade = [sum(abs(l[j]) for l in ativacoes) / n for j in range(d)]
    media = sum(atividade) / d
    if media <= 1e-300:
        return 1.0
    return sum(a <= limiar * media for a in atividade) / d


def esquecimento(R):
    """Para cada tarefa j anterior à última: o máximo de R[i][j] nas etapas i de j até a penúltima, menos a acurácia final R[-1][j]."""
    t = len(R)
    return [max(R[i][j] for i in range(j, t - 1)) - R[-1][j] for j in range(t - 1)]
