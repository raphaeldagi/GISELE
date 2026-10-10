"""O lago semântico e o motor de Horn, corrigidos (Parte 72; ↩ P1608).

Versões escritas do zero a partir das ideias do texto recebido na Parte 72 (o `SemanticLake` e o `InferenceEngine`), sem executar aquele código,
com cada defeito achado na auditoria estática corrigido e testado (`synthai/testes_parte72.py`):
- um esquema só para as relações (dicionários {"tipo", "alvo"}), validadas na criação e na ligação, sem duplicatas;
- a mesma normalização da palavra em toda entrada (`add`, `ligar`, `achar`);
- uma impressão digital que depende só do conteúdo (não da ordem de inserção);
- identificadores hexadecimais com largura para o WordNet inteiro (117.659 sinsets = 0x1CB9B: 5 dígitos);
- premissas de regra que são uma lista de textos (uma string sozinha é recusada, e não lida letra por letra);
- o motor em tempo linear (contadores e fila: Dowling e Gallier, 1984; `calculos.p1609_horn_linear`), com a prova completa de cada conclusão.
Só biblioteca padrão."""

import hashlib
import json

import calculos

ESTADOS = ("hipotese", "fonte", "derivado")


def _chave(palavra):
    if not isinstance(palavra, str) or not palavra.strip():
        raise ValueError("a palavra não pode ser vazia")
    return palavra.strip().lower()


class LagoSemantico:
    """Memória semântica mínima e verificável. Cada conceito tem uma definição, um estado de evidência (um de ESTADOS) e relações {"tipo", "alvo"}
    para conceitos que existem."""

    LARGURA_HEX = 5

    def __init__(self):
        self.conceitos = {}
        self.proximo = 1

    def adicionar(self, palavra, definicao, relacoes=(), estado="hipotese"):
        k = _chave(palavra)
        if k in self.conceitos:
            raise ValueError(f"conceito repetido: {k}")
        if estado not in ESTADOS:
            raise ValueError(f"estado de evidência desconhecido: {estado}")
        if self.proximo >= 16 ** self.LARGURA_HEX:
            raise OverflowError("identificador além da largura hexadecimal")
        rels = []
        for tipo, alvo in relacoes:
            a = _chave(alvo)
            if a not in self.conceitos:
                raise KeyError(f"alvo desconhecido: {a}")
            if {"tipo": tipo, "alvo": a} not in rels:
                rels.append({"tipo": tipo, "alvo": a})
        self.conceitos[k] = {"id": self.proximo, "hex": f"0x{self.proximo:0{self.LARGURA_HEX}X}", "palavra": k,
                             "definicao": definicao, "relacoes": rels, "estado": estado}
        self.proximo += 1
        return self.conceitos[k]

    def ligar(self, origem, tipo, alvo):
        o, a = _chave(origem), _chave(alvo)
        for x in (o, a):
            if x not in self.conceitos:
                raise KeyError(f"conceito desconhecido: {x}")
        r = {"tipo": tipo, "alvo": a}
        if r in self.conceitos[o]["relacoes"]:
            return False
        self.conceitos[o]["relacoes"].append(r)
        return True

    def achar(self, palavra):
        return self.conceitos.get(_chave(palavra))

    def impressao_digital(self):
        """SHA-256 do conteúdo (palavras, definições, estados, relações ordenadas), sem os identificadores, que dependem da ordem de inserção."""
        conteudo = {k: {"definicao": c["definicao"], "estado": c["estado"],
                        "relacoes": sorted((r["tipo"], r["alvo"]) for r in c["relacoes"])}
                    for k, c in self.conceitos.items()}
        return hashlib.sha256(json.dumps(conteudo, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


class MotorHorn:
    """Regras de Horn (premissas ⇒ conclusão) e fatos, com inferência em tempo linear e a prova completa (a árvore de regras até os fatos)."""

    def __init__(self):
        self.fatos = []
        self.regras = []

    def fato(self, f):
        f = _chave(f)
        if f not in self.fatos:
            self.fatos.append(f)

    def regra(self, premissas, conclusao):
        if isinstance(premissas, str) or not isinstance(premissas, (list, tuple)) or not premissas:
            raise ValueError("as premissas são uma lista não vazia de textos")
        self.regras.append((tuple(_chave(p) for p in premissas), _chave(conclusao)))

    def inferir(self):
        ordem, prova, _ = calculos.p1609_horn_linear(self.fatos, self.regras)
        return ordem, prova

    def perguntar(self, alvo):
        """("sustentado", prova completa) ou ("desconhecido", premissas que faltam até os fatos, em todos os níveis). Desconhecido não é falso."""
        a = _chave(alvo)
        ordem, prova = self.inferir()
        if a in prova:
            return "sustentado", self._arvore(a, prova)
        falta, vistos, pilha = set(), set(), [a]
        while pilha:
            x = pilha.pop()
            if x in vistos:
                continue
            vistos.add(x)
            regras_x = [p for p, c in self.regras if c == x]
            if not regras_x:
                falta.add(x)
            for prem in regras_x:
                pilha.extend(p for p in prem if p not in prova)
        return "desconhecido", sorted(falta)

    def _arvore(self, a, prova):
        r = prova[a]
        if r is None:
            return a
        prem, concl = self.regras[r]
        return (concl, [self._arvore(p, prova) for p in prem])
