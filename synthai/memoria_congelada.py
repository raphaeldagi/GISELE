"""A memória congelada de falhas e a comparação pareada de `externos/pacote3/transferencia_metacognitiva.py` (Parte 138), offline e em
biblioteca padrão.

O original otimiza quadráticas de quatro famílias (suave, anisotrópica, rígida, ruidosa) com retrocesso: cada rejeição (o custo subiu
ou o passo deslocou mais que 1) divide o passo por 2, e cada ganho o multiplica por 1,06. No TREINO, uma memória conta, por "contexto
do gradiente", quantas tentativas foram rejeitadas. Os contextos são baixo, médio e alto, pela razão |g|/√f com cortes 3 e 6. A memória é
CONGELADA antes do teste e só mexe no PRIMEIRO passo de cada tarefa: passo·(1 − 0,6·(r + 1)/(n + 2)) se o contexto teve n ≥ 8 tentativas.
A comparação é pareada por tarefa, com bootstrap estratificado por família.

O que não veio: o original importa `recursiva_paraconsistente` (uma geometria restrita com retração, um motor de evidências e uma
"metaprobabilidade"), que não estava no pacote. Aqui a otimização é sem restrição, e o "conflito" sintético da família ruidosa entra
como uma rejeição sorteada com a chance declarada. Os números não são os do original, só o desenho.
"""
import math
import random

from synthai.passos import quadratica_anisotropica, custo, gradiente, _soma

FAMILIAS = ("suave", "anisotropica", "rigida", "ruidosa")
_PARAMETROS = {"suave": (1.0, 1.0, 0.0, 0.0), "anisotropica": (8.0, 3.0, 0.0, 0.0), "rigida": (32.0, 12.0, 0.0, 0.0),
               "ruidosa": (8.0, 3.0, 0.2, 0.1)}


def gerar_tarefas(n, dimensao=8, semente=31, fase=1):
    """n tarefas (múltiplo de 4), famílias em rodízio. A hessiana tem espectro geométrico de escala/condição a escala (como no original);
    alvo e partida gaussianos. Cada tarefa: dict com A (a metade da hessiana: custo dᵀAd), alvo, x0, sigma, conflito, familia, chave."""
    tarefas = []
    for i in range(n):
        fam = FAMILIAS[i % 4]
        cond, escala, sigma, conflito = _PARAMETROS[fam]
        A, lam, _ = quadratica_anisotropica(dimensao, cond, semente * 100000 + fase * 1000 + i)
        A = [[escala / cond * v for v in linha] for linha in A]  # espectro de escala/cond a escala
        r = random.Random(semente * 100000 + fase * 1000 + i + 7)
        tarefas.append(dict(A=A, alvo=[r.gauss(0, 1) for _ in range(dimensao)], x0=[r.gauss(0, 1) for _ in range(dimensao)],
                            sigma=sigma, conflito=conflito, familia=fam, chave=(semente, fase, i)))
    return tarefas


def contexto(g, f):
    """O contexto do original: |g|/√f < 3 baixo, < 6 médio, senão alto. Numa quadrática dᵀAd, |g|²/f = 4·dᵀA²d/dᵀAd, um quociente de
    Rayleigh de A: a razão fica entre 2√λ_min e 2√λ_max. O contexto é uma estimativa de curvatura."""
    razao = math.sqrt(_soma(v * v for v in g)) / math.sqrt(max(f, 1e-12))
    return "baixo" if razao < 3 else ("medio" if razao < 6 else "alto")


class MemoriaFalhas:
    """Conta, no treino, (tentativas sem conflito, rejeições) por contexto; `congelar` devolve o fator do primeiro passo."""

    def __init__(self):
        self.contagens = {c: [0, 0] for c in ("baixo", "medio", "alto")}

    def registrar(self, ctx, motivo):
        if motivo != "conflito":
            self.contagens[ctx][0] += 1
            self.contagens[ctx][1] += int(motivo != "aceita")

    def congelar(self):
        congelado = {c: tuple(v) for c, v in self.contagens.items()}

        def fator(ctx):
            n, r = congelado[ctx]
            return 1 - 0.6 * (r + 1) / (n + 2) if n >= 8 else 1.0
        return fator


def executar(tarefa, passo, orcamento=24, fator=None, coletor=None):
    """O retrocesso do original, sem a geometria restrita. Devolve f_final / f_inicial."""
    s0, fase, i = tarefa["chave"]
    rng = random.Random(s0 * 1000003 + fase * 1009 + i)
    A, alvo, x = tarefa["A"], tarefa["alvo"], list(tarefa["x0"])
    f = custo(A, x, alvo)
    f0 = f
    for t in range(1, orcamento + 1):
        g = gradiente(A, x, alvo)
        if tarefa["sigma"]:
            g = [gi + tarefa["sigma"] * rng.gauss(0, 1) for gi in g]
        ctx = contexto(g, f)
        if t == 1 and fator is not None:
            passo *= fator(ctx)
        cand = [xi - passo * gi for xi, gi in zip(x, g)]
        fc = custo(A, cand, alvo)
        desloc = math.sqrt(_soma((a - b) * (a - b) for a, b in zip(cand, x)))
        conflito = rng.random() < tarefa["conflito"]
        motivo = "conflito" if conflito else ("deslocamento" if desloc > 1.0 else ("custo" if fc > f + 1e-12 else "aceita"))
        ganho = 0.0
        if motivo == "aceita":
            ganho = f - fc
            x, f = cand, fc
        if coletor is not None:
            coletor.registrar(ctx, motivo)
        if motivo in ("custo", "deslocamento"):
            passo = max(0.002, passo * 0.5)
        elif motivo == "aceita" and ganho > 1e-3 * max(f + ganho, 1e-12):
            passo = min(0.4, passo * 1.06)
    return f / max(f0, 1e-12)


def comparacao_pareada(base, nova, familias, replicas=1200, semente=31):
    """Diferenças pareadas base − nova (positivo favorece a nova), com bootstrap estratificado por família. Devolve (média, ganhos,
    perdas, empates, intervalo 95% do bootstrap)."""
    d = [b - n for b, n in zip(base, nova)]
    grupos = [[i for i, f in enumerate(familias) if f == fam] for fam in FAMILIAS]
    r = random.Random(semente * 1000 + 511)
    medias = []
    for _ in range(replicas):
        idx = [g[r.randrange(len(g))] for g in grupos if g for _ in range(len(g))]
        medias.append(_soma(d[i] for i in idx) / len(idx))
    medias.sort()
    lo, hi = medias[int(0.025 * replicas)], medias[int(0.975 * replicas) - 1]
    return (_soma(d) / len(d), sum(x > 1e-12 for x in d), sum(x < -1e-12 for x in d), sum(abs(x) <= 1e-12 for x in d), (lo, hi))
