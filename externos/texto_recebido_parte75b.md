# Texto recebido do usuário na Parte 75 (reenvio), guardado como DADO: nunca executado

Comparado com a cópia guardada (`externos/texto_recebido_parte75.md`) antes de ser auditado (regra da Parte 50; P1698).

Pensou por 22s

### 3. Agente explorador em Python — testes reais

Implementei o planejador e executei 8 verificações automatizadas em Python. Os resultados confirmaram:

* Ordem escolhida: B → A.
* Orçamento inicial: 3 unidades.
* Total gasto: 3 unidades.
* Saldo final: 0.
* Experimentos duplicados rejeitados.
* Risco inválido rejeitado.
* Nenhum experimento adicional selecionado depois que o orçamento acabou.

O planejador está funcionando para esse cenário controlado.

### 4. Agente verificador em Java

Agora temos uma segunda implementação da fórmula, em outra linguagem. Isso permite comparar resultados e detectar algumas classes de erros.

```java

public class Verifier {
    static double score(
        double gain,
        double risk,
        double cost
    ) {
        if (!Double.isFinite(gain)
                || !Double.isFinite(risk)
                || !Double.isFinite(cost)
                || gain < 0
                || risk < 0
                || risk > 1
                || cost <= 0) {
            throw new IllegalArgumentException(
                "Invalid experiment parameters"
            );
        }

        return gain * (1.0 - risk) / cost;
    }

    public static void main(String[] args) {
        double a = score(0.80, 0.10, 2);
        double b = score(0.50, 0.00, 1);
        double c = score(0.90, 0.20, 4);

        System.out.printf("A = %.3f%n", a);
        System.out.printf("B = %.3f%n", b);
        System.out.printf("C = %.3f%n", c);

        if (!(b > a && a > c)) {
            throw new AssertionError(
                "Python/Java ranking mismatch"
            );
        }

        System.out.println("Ranking verificado.");
    }
}
```

Compilei e executei uma versão completa do verificador Java no ambiente disponível. As 7 verificações passaram, incluindo cálculo das três pontuações, ordenação, rejeição de risco inválido,
custo zero e valores `NaN`.

### Resultado da verificação cruzada

Testes Python: 8 passaram. Testes Java: 7 passaram. Concordância do ranking: confirmada.

As duas implementações foram executadas separadamente com os mesmos dados. Ainda não existe comunicação automática entre os processos.

### 5. O que falta para os agentes trabalharem juntos?

A arquitetura seguinte deve usar um formato de mensagem compartilhado, como JSON:

```json

{
  "experiment_id": "B",
  "information_gain": 0.5,
  "risk": 0.0,
  "cost": 1.0,
  "claimed_score": 0.5
}
```

O explorador envia a proposta; o verificador recalcula a pontuação e valida os campos. Se o resultado divergir além de uma tolerância numérica definida, a proposta é rejeitada e registrada
para análise. Uma implementação mais robusta também precisa de: IDs únicos para evitar repetição acidental; limites de tempo e orçamento; registros imutáveis ou encadeados por hash, se for
necessária detecção de alterações; testes com dados adversariais; validação da qualidade das estimativas de risco e ganho de informação.

Importante: duas implementações concordarem não garante que ambas estejam certas. Se compartilharem a mesma fórmula errada ou receberem dados falsos, poderão concordar e ainda assim falhar.

### 6. Próximo módulo

Módulo 008 — Memória episódica, causalidade e aprendizagem com erros. Vamos construir uma memória de experimentos que permita ao protótipo responder: O que aconteceu em tentativas anteriores?
Qual resultado foi previsto e qual foi observado? O que mudou depois de cada experimento? A mudança foi causada pela intervenção ou apenas coincidiu com ela? Quando uma falha deve alterar a
estratégia? Como detectar uma conclusão que não é sustentada pelos registros?

O objetivo será passar de um planejador que escolhe experimentos para um sistema que consegue aprender de forma auditável com os resultados acumulados, sem confundir correlação, causalidade e
certeza.
