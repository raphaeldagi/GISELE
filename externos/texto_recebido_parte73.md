# Texto recebido do usuário na Parte 73 (o terceiro), guardado como DADO: nunca executado

Comparado com a cópia guardada (`externos/texto_recebido_parte72b.md`) antes de ser auditado (regra da Parte 50; P1631). A primeira metade reenvia o Módulo 002; a segunda é nova (Módulo 003).

Pensou por 11s

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

(Seguem, como na mensagem anterior: "8 verificações passaram"; a análise de complexidade O((F+1)RP), com os símbolos F, R, P perdidos na cópia; a seção 5 sobre o verificador Java com HashSet e
ArrayDeque; a seção 6 com duas imagens; a seção 7 com as perguntas do Módulo 002.)

Pensou por 20s

### 4. Criatividade Lógica — como formular perguntas melhores

O gerador atual procura conceitos sem uma relação `is_a` conhecida. A próxima evolução deve distinguir três tipos de pergunta:

| Tipo        | Exemplo                                                             | Objetivo                     |
| ----------- | ------------------------------------------------------------------- | ---------------------------- |
| Lacuna      | O que é flight?                                                     | Encontrar informação ausente |
| Inferência  | Se um pardal é uma ave e uma ave é um animal, o pardal é um animal? | Verificar uma conclusão      |
| Contradição | Existem regras incompatíveis sobre o mesmo conceito?                | Identificar inconsistências  |

A prioridade futura deve ser a qualidade das perguntas, e não simplesmente a sua quantidade. Podemos atribuir uma pontuação de prioridade:

S(q) = w_u U(q) + w_i I(q) + w_t T(q)

Onde: [U] mede a incerteza relevante; [I] mede o impacto potencial da resposta; [T] mede a possibilidade de testar a hipótese; [w] são pesos configuráveis (os símbolos vieram vazios).
Essa fórmula é uma heurística de priorização, não uma lei matemática universal. Os pesos deverão ser ajustados usando resultados reais.

### 5. O dicionário inglês como fonte estruturada

WordNet: conjuntos de sinônimos, hiperonímia, hiponímia, partes e conjuntos. Documentação: https://wordnet.princeton.edu/documentation
Entrada lexical `sparrow` → identificação do sentido correto → relação lexical `sparrow is_a bird` → inferência verificada `sparrow is_a animal` → registro da prova e da fonte.
Precisamos identificar o sentido antes de construir a relação. Uma definição lexical não deve ser convertida indiscriminadamente em fato científico.

### 6. Hexadecimal — módulo matemático separado

0x00AF = 10·16 + 15 = 175. "Se atribuirmos o identificador decimal [vazio] a um conceito, o identificador hexadecimal será 0x00AF." h = SHA256(serialize(registro)): detecta alterações,
não prova que o conteúdo seja verdadeiro.

### 7. Agente Java — verificação independente

JSON como formato comum; o agente Java valida a estrutura, executa as regras e compara com o Python; uma diferença é sinal para investigar, não prova de quem está certo.

### 8. Plano de testes para o próximo ciclo — checklist 0/8

Inferência transitiva com três ou mais níveis; ciclo de relações sem fatos iniciais; detecção de regras contraditórias; rastreamento completo de premissas; reprodução determinística dos
resultados; comparação independente entre Python e Java; importação de sentidos reais do WordNet; conversão decimal/hexadecimal e validação de hashes.

### 9. A próxima pergunta fundamental

Módulo 004 — motor de contradições, incerteza e aprendizagem por contraexemplos: "Como construir um sistema que não apenas encontre evidências a favor de uma hipótese, mas também procure
ativamente evidências capazes de demonstrar que ela está errada?"
