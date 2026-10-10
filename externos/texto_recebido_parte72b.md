# Texto recebido do usuário na Parte 72 (o segundo), guardado como DADO: nunca executado

Guardado para a auditoria estática da Parte 72 (P1608): o código abaixo é lido pela árvore sintática (`ast.parse`), que analisa sem executar.

### 3.1. Implementação Python

Este é o primeiro componente real do protótipo. O código mantém um pequeno grafo de conceitos, impede duplicações, valida relações e gera identificadores hexadecimais.

```python

import json
import hashlib

class SemanticLake:
    """Protótipo mínimo de memória semântica verificável."""

    def __init__(self):
        self.entries = {}
        self.next_id = 1

    def add(self, word, definition, relations=None,
            evidence_status="hypothesis"):
        key = word.strip().lower()

        if not key:
            raise ValueError("word must not be empty")

        if key in self.entries:
            raise ValueError(f"duplicate concept: {key}")

        entry_id = self.next_id
        self.next_id += 1

        entry = {
            "id": entry_id,
            "hex_id": f"0x{entry_id:04X}",
            "word": key,
            "definition": definition,
            "relations": list(relations or []),
            "evidence_status": evidence_status,
        }

        self.entries[key] = entry
        return entry

    def link(self, source, relation, target):
        if source not in self.entries:
            raise KeyError(f"unknown source: {source}")

        if target not in self.entries:
            raise KeyError(f"unknown target: {target}")

        self.entries[source]["relations"].append({
            "type": relation,
            "target": target,
        })

    def find(self, word):
        return self.entries.get(word.strip().lower())

    def export_json(self):
        return json.dumps(
            self.entries,
            sort_keys=True,
            ensure_ascii=False,
            indent=2,
        )

    def fingerprint(self):
        data = self.export_json().encode("utf-8")
        return hashlib.sha256(data).hexdigest()

def run_tests():
    lake = SemanticLake()

    lake.add(
        "reasoning",
        "Drawing conclusions from information and rules.",
        ["logic", "inference"],
    )
    lake.add(
        "logic",
        "Study of valid inference and argument.",
    )
    lake.add(
        "inference",
        "A conclusion derived from premises.",
    )

    lake.link("reasoning", "uses", "inference")

    # Teste 1: quantidade de conceitos
    assert len(lake.entries) == 3

    # Teste 2: unicidade dos identificadores
    ids = [e["hex_id"] for e in lake.entries.values()]
    assert len(ids) == len(set(ids))

    # Teste 3: equivalência decimal/hexadecimal
    for entry in lake.entries.values():
        assert int(entry["hex_id"], 16) == entry["id"]

    # Teste 4: integridade da relação
    assert lake.entries["reasoning"]["relations"][-1] == {
        "type": "uses",
        "target": "inference",
    }

    # Teste 5: rejeição de conceitos vazios
    try:
        lake.add("", "invalid")
        raise AssertionError("Empty word accepted")
    except ValueError:
        pass

    # Teste 6: rejeição de referências inexistentes
    try:
        lake.link("reasoning", "related_to", "missing")
        raise AssertionError("Missing concept accepted")
    except KeyError:
        pass

    return {
        "tests": 6,
        "status": "passed",
        "concept_count": len(lake.entries),
        "fingerprint": lake.fingerprint(),
    }

if __name__ == "__main__":
    print(json.dumps(run_tests(), indent=2))
```

Resultado da simulação realizada: os seis testes passaram. Foram criados três conceitos, com identificadores `0x0001`, `0x0002` e `0x0003`.

Essa execução verifica somente as propriedades implementadas. Ela não demonstra aprendizagem autônoma, compreensão geral ou inteligência artificial geral.

### 4. O ciclo de ensino: IA Python e IA Java

Agente Python — Lógica Criativa: propõe hipóteses, gera casos de teste, encontra contraexemplos e experimenta algoritmos.
Agente Java — Criatividade Lógica: verifica contratos, tipos, invariantes e resultados; sugere uma implementação mais rigorosa.

O ciclo: Python propõe uma solução; Java analisa as condições de validade; ambos recebem os mesmos casos de teste; o verificador compara os resultados; as divergências são
registradas como problemas; uma nova versão é criada e testada novamente. (Interoperabilidade futura: interface de serviços ou JPype.)

### 5. Hexadecimal: módulo matemático independente

N_10 = Σ_{i=0}^{k} d_i 16^i. Exemplo: 0x2F3 = 2·16² + 15·16¹ + 3·16⁰ = 512 + 240 + 3 = 755. E a conversão inversa: 755 = 2·16² + 15·16 + 3. "Portanto, ." (a fórmula final veio vazia).
Um identificador hexadecimal identifica uma entrada; não significa que ela seja mais importante ou mais verdadeira.

### 6. O dicionário inglês como data lake

WordNet como ponto de partida; modelo de dados com lemma, sense_id, definition, examples, relations, source, confidence, evidence_status, hex_id, revision. Exemplo: bird is_a animal;
"Se algo é um pássaro, então é um animal": verificar se a relação existe na fonte e distinguir a informação lexical de uma regra lógica geral.

### 7. Próximo ciclo (perguntas do texto)

Gerar perguntas a partir das relações; distinguir dedução válida de associação provável; armazenar provas e contraexemplos; Python e Java verificando o mesmo resultado; medir se uma
versão nova melhorou; não presumir que o dicionário contém todo o conhecimento; combinar simbólico, numérico e estatístico. "Não consigo executar uma interação infinita em segundo plano."

### 3. Código Python — motor de inferência executável

Este protótipo utiliza regras do tipo Horn: uma conclusão só é derivada quando todas as premissas da regra estão presentes na base de conhecimento.

```python

from collections import deque

class InferenceEngine:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        if not isinstance(fact, str) or not fact.strip():
            raise ValueError("O fato não pode ser vazio")
        self.facts.add(fact.strip())

    def add_rule(self, premises, conclusion, label="rule"):
        premises = tuple(p.strip() for p in premises)

        if not premises or any(not p for p in premises):
            raise ValueError("A regra exige premissas válidas")

        if not isinstance(conclusion, str) or not conclusion.strip():
            raise ValueError("A conclusão não pode ser vazia")

        self.rules.append(
            (premises, conclusion.strip(), label)
        )

    def infer(self):
        known = set(self.facts)
        proofs = {
            fact: {"rule": "given", "premises": []}
            for fact in known
        }

        changed = True

        while changed:
            changed = False

            for premises, conclusion, label in self.rules:
                if conclusion in known:
                    continue

                if all(p in known for p in premises):
                    known.add(conclusion)
                    proofs[conclusion] = {
                        "rule": label,
                        "premises": list(premises),
                    }
                    changed = True

        return known, proofs

    def ask(self, target):
        known, proofs = self.infer()

        if target in known:
            return {
                "question": target,
                "status": "supported",
                "proof": proofs[target],
            }

        missing = []

        for premises, conclusion, _ in self.rules:
            if conclusion == target:
                missing.extend(
                    p for p in premises if p not in known
                )

        return {
            "question": target,
            "status": "unknown",
            "missing_premises": sorted(set(missing)),
            "note": "Unknown does not mean false.",
        }

def test_engine():
    engine = InferenceEngine()

    engine.add_fact("Tweety is a bird")

    engine.add_rule(
        ["Tweety is a bird"],
        "Tweety is an animal",
        "bird_implies_animal",
    )

    engine.add_rule(
        ["Tweety is an animal"],
        "Tweety is a living thing",
        "animal_implies_living",
    )

    known, proofs = engine.infer()

    assert "Tweety is an animal" in known
    assert "Tweety is a living thing" in known

    assert engine.ask(
        "Tweety is an animal"
    )["status"] == "supported"

    assert engine.ask(
        "Tweety can fly"
    )["status"] == "unknown"

    # Entradas inválidas devem ser rejeitadas.
    for invalid_operation in [
        lambda: engine.add_fact(""),
        lambda: engine.add_rule([], "X"),
    ]:
        try:
            invalid_operation()
            raise AssertionError("Entrada inválida aceita")
        except ValueError:
            pass

    # Um ciclo sem fatos iniciais não cria conhecimento.
    cycle = InferenceEngine()
    cycle.add_rule(["A"], "B")
    cycle.add_rule(["B"], "A")

    assert cycle.infer()[0] == set()

    return {
        "status": "passed",
        "tests_passed": 8,
        "derived_facts": sorted(known),
        "proof_example": proofs["Tweety is an animal"],
        "unknown_example": engine.ask("Tweety can fly"),
    }

if __name__ == "__main__":
    print(test_engine())
```

Resultado dos testes (segundo o texto): "8 verificações passaram". Fatos derivados: Tweety is a bird → Tweety is an animal → Tweety is a living thing; "Tweety can fly" → unknown.

### 4. Análise de complexidade (do texto)

F fatos conhecidos, R regras, P premissas no total. "Um limite simples para o tempo é O((F+1)RP)." Próxima otimização: fila de fatos recém-descobertos e índices das regras que dependem de cada fato.

### 5–7. Java como verificador independente (HashSet, ArrayDeque); "não devemos considerar a resposta correta apenas porque duas implementações concordam: ambas podem conter o mesmo erro
lógico"; o dicionário e o hexadecimal com funções diferentes; perguntas do Módulo 002: geração de perguntas, proveniência, contradições, aprendizagem, cooperação Python–Java, dicionário,
hexadecimal (hash não é prova de correção).
