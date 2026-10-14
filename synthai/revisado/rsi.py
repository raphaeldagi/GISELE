"""Busca experimental de parâmetros (RSI), para testar afirmações da arquitetura "pós-ASI" (Parte 33).

Nada aqui executa código gerado: o que muda é um GENOMA (os parâmetros de um aprendiz e, no nível L4, o próprio passo
de mutação), nunca o texto do programa. O avaliador SELADO detecta mudanças no catálogo de dependências após sua
criação; não oferece isolamento contra código hostil no mesmo processo. O avaliador da arquitetura original
(externos/arquitetura_pos_asi.py)
pergunta ao próprio agente a nota dele; aqui isso é a `autoavaliacao`, para medir o que acontece.

Regras de aceitação:
- "dgm": a da arquitetura original. O filho entra se a nota dele for maior que a nota GUARDADA do pai (o melhor do arquivo).
- "godel": uma "prova" estatística, no espírito da máquina de Gödel: filho e pai são reavaliados em sementes NOVAS e
  pareadas, e o filho só entra se a diferença tiver t > 3.

Só biblioteca padrão.
"""

import hashlib
import json
import marshal
import random
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from types import CodeType, FunctionType
from math import isfinite
from math import exp, sqrt

from . import decisao
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


@dataclass(frozen=True)
class ConfiguracaoAvaliacao:
    k: int = 10
    t: int = 2000

    def __post_init__(self):
        if any(type(x) is not int or x < 1 for x in (self.k, self.t)):
            raise ValueError("k e t devem ser inteiros positivos")


def _json_canonico(valor):
    return json.dumps(valor, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _codigo_sem_caminho(codigo):
    """A localização do checkout não faz parte da identidade do algoritmo."""
    constantes = tuple(_codigo_sem_caminho(c) if isinstance(c, CodeType) else c for c in codigo.co_consts)
    return codigo.replace(co_filename="<avaliacao>", co_consts=constantes)


def _resumo_objeto(obj):
    if obj is None or type(obj) in (str, int, float, bool):
        return obj
    if isinstance(obj, (list, tuple)):
        return [_resumo_objeto(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _resumo_objeto(v) for k, v in obj.items()}
    nome = getattr(obj, "__qualname__", getattr(obj, "__name__", type(obj).__qualname__))
    resumo = {"tipo": type(obj).__name__, "modulo": getattr(obj, "__module__", ""), "nome": nome}
    if isinstance(obj, FunctionType):
        resumo.update(
            codigo=hashlib.sha256(marshal.dumps(_codigo_sem_caminho(obj.__code__))).hexdigest(),
            defaults=_resumo_objeto(obj.__defaults__), kwdefaults=_resumo_objeto(obj.__kwdefaults__))
    return resumo


def _dependencias_da_nota():
    """Catálogo explícito do caminho executado; revise-o ao mudar o benchmark."""
    deps = {"regret_do_genoma": regret_do_genoma, "rsi.rodar_bandido": rodar_bandido,
            "decisao.rodar_bandido": decisao.rodar_bandido,
            "rsi.QEpsilon": QEpsilon, "decisao.QEpsilon": decisao.QEpsilon, "random.Random": random.Random}
    for nome in ("__init__", "escolher", "atualizar", "__new__", "__getattribute__", "__setattr__"):
        deps["QEpsilon." + nome] = getattr(QEpsilon, nome)
    for nome in ("__init__", "seed", "random", "choice", "randrange", "_randbelow", "getrandbits", "__new__"):
        deps["Random." + nome] = getattr(random.Random, nome)
    for chave, obj in tuple(deps.items()):
        if not isinstance(obj, FunctionType):
            continue
        for nome in obj.__code__.co_names:
            if nome in obj.__globals__:
                deps[chave + ".global." + nome] = obj.__globals__[nome]
            elif nome in obj.__builtins__:
                deps[chave + ".builtin." + nome] = obj.__builtins__[nome]
        for i, celula in enumerate(obj.__closure__ or ()):
            deps[f"{chave}.closure.{i}"] = celula.cell_contents
    return deps


class AvaliadorSelado:
    """Nota externa com verificação de integridade e registro reproduzível.

    O selo cobre arquivos, código/defaults e bindings de um catálogo explícito,
    configuração e versão do Python. É conferido antes e depois de calcular.
    Este processo é cooperativo: o próprio auditor e sua base inicial precisam
    ser confiáveis. Não há isolamento, autenticação de origem ou proteção contra
    alterações transitórias entre verificações.
    """

    def __init__(self, k=10, t=2000):
        self._config = ConfiguracaoAvaliacao(k, t)
        self._arquivos = {"rsi.py": Path(__file__).resolve(),
                          "decisao.py": Path(decisao.__file__).resolve(),
                          "random.py": Path(random.__file__).resolve()}
        self._bindings = _dependencias_da_nota()
        self._manifesto = self._manifesto_atual()
        self._selo_inicial = hashlib.sha256(_json_canonico(self._manifesto).encode()).hexdigest()
        self.selo = self._selo_inicial
        self.chamadas = 0
        self._registros = []

    @property
    def configuracao(self):
        return self._config

    @property
    def manifesto(self):
        return deepcopy(self._manifesto)

    @property
    def registros(self):
        return tuple(deepcopy(self._registros))

    def _manifesto_atual(self):
        deps = _dependencias_da_nota()
        classes = {nome: {k: _resumo_objeto(v) for k, v in vars(cls).items()}
                   for nome, cls in (("QEpsilon", QEpsilon), ("Random", random.Random))}
        return {"versao": 1, "protocolo": "bernoulli-qepsilon-regret-v1",
                "configuracao": {"k": self._config.k, "t": self._config.t},
                "limites_genoma": _resumo_objeto(LIMITES),
                "sementes": "mundo=s; aprendiz=s+1; recompensas=s+2",
                "runtime": {"python": sys.version, "implementacao": sys.implementation.name,
                            "cache_tag": sys.implementation.cache_tag, "marshal": marshal.version},
                "arquivos": {nome: hashlib.sha256(p.read_bytes()).hexdigest()
                             for nome, p in self._arquivos.items()},
                "dependencias": {nome: _resumo_objeto(obj) for nome, obj in deps.items()},
                "classes": classes}

    def assinatura(self):
        return hashlib.sha256(_json_canonico(self._manifesto_atual()).encode()).hexdigest()

    def _verificar(self):
        try:
            atuais = _dependencias_da_nota()
            iguais = atuais.keys() == self._bindings.keys() and all(
                atuais[nome] is obj for nome, obj in self._bindings.items())
            if not iguais or self.selo != self._selo_inicial or self.assinatura() != self._selo_inicial:
                raise RuntimeError("dependências ou configuração do avaliador mudaram: avaliação recusada")
        except (OSError, TypeError, ValueError, AttributeError) as erro:
            raise RuntimeError("não foi possível verificar a integridade do avaliador") from erro

    def nota(self, genoma, sementes):
        self._verificar()
        # Materializar antes do cálculo evita perder geradores e referências mutáveis.
        sementes = tuple(sementes)
        if not sementes or any(type(s) is not int for s in sementes):
            raise ValueError("sementes devem conter ao menos um inteiro")
        snapshot = json.loads(_json_canonico(genoma))
        if not isinstance(snapshot, dict):
            raise ValueError("genoma deve ser um objeto de parâmetros")
        for nome, (menor, maior) in LIMITES.items():
            v = snapshot.get(nome)
            if type(v) not in (int, float) or not isfinite(v) or not menor <= v <= maior:
                raise ValueError(f"parâmetro inválido: {nome}")
        # Um iterador de entrada pode ter alterado dependências durante a leitura.
        self._verificar()
        nota = -regret_do_genoma(deepcopy(snapshot), sementes, k=self._config.k, t=self._config.t)
        self._verificar()
        if not isfinite(nota) or not -self._config.t <= nota <= 0:
            raise ValueError("nota fora do domínio do benchmark")
        registro = {"numero": self.chamadas + 1, "selo": self.selo,
                    "configuracao": {"k": self._config.k, "t": self._config.t},
                    "genoma": snapshot, "sementes": list(sementes), "nota": nota}
        registro["sha256"] = hashlib.sha256(_json_canonico(registro).encode()).hexdigest()
        self._registros.append(registro)
        self.chamadas += 1
        return nota


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
