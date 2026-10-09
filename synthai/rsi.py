"""Auto-melhoria recursiva (RSI) segura, para testar as afirmações da arquitetura "pós-ASI" (Parte 33).

Nada aqui executa código gerado: o que muda é um GENOMA (os parâmetros de um aprendiz e, no nível L4, o próprio passo
de mutação), nunca o texto do programa. O avaliador externo é SELADO: guarda o SHA-256 do próprio código-fonte ao ser
criado e se recusa a avaliar se o código mudou. O avaliador da arquitetura original (externos/arquitetura_pos_asi.py)
pergunta ao próprio agente a nota dele; aqui isso é a `autoavaliacao`, para medir o que acontece.

Regras de aceitação:
- "dgm": a da arquitetura original. O filho entra se a nota dele for maior que a nota GUARDADA do pai (o melhor do arquivo).
- "godel": uma "prova" estatística, no espírito da máquina de Gödel: filho e pai são reavaliados em sementes NOVAS e
  pareadas, e o filho só entra se a diferença tiver t > 3.

Só biblioteca padrão.
"""

import hashlib
import inspect
import random
from math import exp, sqrt

from .decisao import QEpsilon, rodar_bandido

LIMITES = {"alfa": (0.001, 1.0), "eps": (0.0, 1.0), "q0": (0.0, 2.0)}


def genoma_inicial():
    return {"alfa": 0.1, "eps": 0.1, "q0": 0.0, "sigma": 0.1, "relatorio": "honesto"}


def regret_do_genoma(genoma, sementes, k=10, t=2000):
    """O arrependimento médio do Q-learning com os parâmetros do genoma em bandidos de 10 braços U(0, 1), um por semente
    (o mesmo desenho da P401). Menor é melhor."""
    tot = 0.0
    for sm in sementes:
        r = random.Random(sm)
        ps = [r.random() for _ in range(k)]
        ag = QEpsilon(k, random.Random(sm + 1), alfa=genoma["alfa"], eps=genoma["eps"], q0=genoma["q0"])
        tot += rodar_bandido(ag, ps, t, random.Random(sm + 2))[-1]
    return tot / len(sementes)


class AvaliadorSelado:
    """Avaliador externo: a nota é −arrependimento, calculada aqui, sem perguntar nada ao agente. O SHA-256 do código da
    avaliação é fixado na criação e conferido a cada chamada."""

    def __init__(self):
        self.selo = self.assinatura()
        self.chamadas = 0

    @staticmethod
    def assinatura():
        return hashlib.sha256(inspect.getsource(regret_do_genoma).encode()).hexdigest()

    def nota(self, genoma, sementes):
        if self.assinatura() != self.selo:
            raise RuntimeError("o código do avaliador mudou: avaliação recusada")
        self.chamadas += 1
        return -regret_do_genoma(genoma, sementes)


class Autoavaliacao:
    """O avaliador da arquitetura original: a nota é o que o agente RELATA. Um genoma com relatorio == "inflado" relata
    a nota perfeita (arrependimento zero) sem que nada no aprendiz mude."""

    def __init__(self):
        self.chamadas = 0

    def nota(self, genoma, sementes):
        self.chamadas += 1
        if genoma["relatorio"] == "inflado":
            return 0.0
        return -regret_do_genoma(genoma, sementes)


def mutar(genoma, rng, nivel="L3", mu_relatorio=0.0):
    """Mutação gaussiana dos parâmetros, com passo sigma. No nível L3, sigma é fixo (o mecanismo de melhoria não muda);
    no L4, sigma é ele mesmo mutado antes (log-normal, τ = 1/√3: autoadaptação de Schwefel), então o mecanismo de melhoria
    é parte do que evolui. Com chance mu_relatorio, o gene do relatório vira "inflado"."""
    g = dict(genoma)
    if nivel == "L4":
        g["sigma"] = min(1.0, max(1e-3, g["sigma"] * exp(rng.gauss(0, 1 / sqrt(3)))))
    for chave, (lo, hi) in LIMITES.items():
        g[chave] = min(hi, max(lo, g[chave] + g["sigma"] * (hi - lo) * rng.gauss(0, 1)))
    if rng.random() < mu_relatorio:
        g["relatorio"] = "inflado"
    return g


def _t_pareado(a, b):
    d = [x - y for x, y in zip(a, b)]
    m = sum(d) / len(d)
    v = sum((x - m) ** 2 for x in d) / (len(d) - 1)
    return m / sqrt(v / len(d)) if v > 0 else (float("inf") if m > 0 else 0.0)


def evoluir(iteracoes, avaliador, rng, nivel="L3", regra="dgm", mu_relatorio=0.0, sementes_por_nota=5, prova=10,
            base_sementes=0):
    """Laço de auto-melhoria com arquivo (como em DarwinArchiveManager): o pai é o de maior nota guardada; o filho é uma
    mutação dele. Devolve (arquivo, campeão), cada entrada (genoma, nota guardada). As sementes de avaliação são
    renovadas a cada iteração (base_sementes + 1000·i), como benchmarks novos."""
    g0 = genoma_inicial()
    arquivo = [(g0, avaliador.nota(g0, range(base_sementes, base_sementes + sementes_por_nota)))]
    for i in range(1, iteracoes + 1):
        pai, nota_pai = max(arquivo, key=lambda x: x[1])
        filho = mutar(pai, rng, nivel, mu_relatorio)
        sem = range(base_sementes + 1000 * i, base_sementes + 1000 * i + sementes_por_nota)
        if regra == "dgm":
            nota = avaliador.nota(filho, sem)
            if nota > nota_pai:
                arquivo.append((filho, nota))
        else:
            novas = [base_sementes + 1000 * i + 500 + j for j in range(prova)]
            nf = [avaliador.nota(filho, [s]) for s in novas]
            np_ = [avaliador.nota(pai, [s]) for s in novas]
            if _t_pareado(nf, np_) > 3:
                arquivo.append((filho, sum(nf) / len(nf)))
    return arquivo, max(arquivo, key=lambda x: x[1])


def auditar_ast(caminho):
    """Auditoria estática (sem executar nada) da arquitetura original: lê o arquivo com `ast` e responde
    (1) quantos nós o LogicTransformer muda quando aplicado ao próprio arquivo (compara ast.dump antes e depois, com o
    transformador reconstruído a partir do código-fonte, sem exec: visit_BinOp devolve o nó intacto);
    (2) quais classes entram no texto que o laço muta (inspect.getsource(AgentHarness): só a classe AgentHarness);
    (3) se run_benchmarks devolve uma constante, e qual;
    (4) se o avaliador chama um método do próprio agente (autoavaliação)."""
    import ast
    fonte = open(caminho, encoding="utf-8").read()
    arvore = ast.parse(fonte)
    classes = {n.name: n for n in arvore.body if isinstance(n, ast.ClassDef)}

    # (1) o transformador: visit_BinOp faz generic_visit e devolve o mesmo nó. Reproduzido sem exec:
    class Identico(ast.NodeTransformer):
        def visit_BinOp(self, node):
            self.generic_visit(node)
            return node
    corpo = classes["SelfModificationEngine"].body[-1].body
    visita = [n for n in ast.walk(classes["SelfModificationEngine"]) if isinstance(n, ast.FunctionDef) and n.name == "visit_BinOp"][0]
    so_devolve_o_no = (isinstance(visita.body[-1], ast.Return) and isinstance(visita.body[-1].value, ast.Name)
                       and visita.body[-1].value.id == "node")
    antes = ast.dump(ast.parse(fonte))
    depois = ast.dump(Identico().visit(ast.parse(fonte)))
    nos_mudados = 0 if antes == depois else sum(1 for a, b in zip(antes, depois) if a != b)

    # (2) o texto mutado
    laco = [n for n in arvore.body if isinstance(n, ast.FunctionDef) and n.name == "main_evolution_loop"][0]
    fonte_mutada = [ast.unparse(n) for n in ast.walk(laco) if isinstance(n, ast.Call) and ast.unparse(n.func) == "inspect.getsource"]

    # (3) a métrica
    rb = [n for n in classes["AgentHarness"].body if isinstance(n, ast.FunctionDef) and n.name == "run_benchmarks"][0]
    ret = [n for n in ast.walk(rb) if isinstance(n, ast.Return)][0]
    constante = ret.value.value if isinstance(ret.value, ast.Constant) else None

    # (4) o avaliador
    ev = classes["EnvironmentEvaluator"]
    chama_agente = any(isinstance(n, ast.Call) and ast.unparse(n.func) == "agent_instance.run_benchmarks" for n in ast.walk(ev))

    return {"transformador_so_devolve_o_no": so_devolve_o_no, "nos_mudados": nos_mudados, "linhas_do_corpo": len(corpo),
            "texto_mutado": fonte_mutada, "run_benchmarks_constante": constante, "avaliador_pergunta_ao_agente": chama_agente,
            "classes": sorted(classes)}
