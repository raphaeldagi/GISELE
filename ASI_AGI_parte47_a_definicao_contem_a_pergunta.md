# Como eu construiria uma AGI/ASI — Parte 47 (0x2F): a definição contém a pergunta

> Continuação da Parte 46. **Em andamento: previsões registradas antes de qualquer execução.**

## As perguntas desta parte

1. **P851 (0x353).** No dicionário, a resposta (a definição) contém a pergunta (a categoria)? E o contrário? ↩ P821
2. **P852 (0x354).** Hexadecimal: um número cujo hexadecimal parece decimal, lido como decimal, gera outro; quantos passos até aparecer uma letra?
3. **P853 (0x355).** O diálogo, rodada 19: as palavras, sem os números, reconstroem a parte? ↩ P824
4. **P854 (0x356).** Engenharia reversa: responder ao padrão, não ao caso.
5. **P855 (0x357).** Jung: o gênero e a diferença.
6. **P879 (0x36F).** Placar. **P880 (0x370).** Unificação.

## Previsões pré-registradas (antes de escrever o código das medidas)

**P851, gênero e diferença (WordNet 3.0, substantivos com hiperônimo).** Acerto direto: a definição (a glosa sem exemplos, minúscula) contém, como
palavra inteira, algum lema do hiperônimo direto (com `_` trocado por espaço; aceito também o lema + "s"/"es"). Acerto inverso: a definição do
hiperônimo contém algum lema de algum dos seus hipônimos (por par hipônimo–hiperônimo).
- (a) fração direta em **[0,26; 0,77]** (instinto 0,45, ×1,72; sem conta de mecanismo, marcado como instinto)
- (b) fração inversa em **[0,023; 0,069]** (instinto 0,04, ×1,72)
- (c) a razão direta/inversa > 5

**P852, a cadeia hexadecimal.** f(n) = o hexadecimal de n lido como decimal, enquanto ele não tiver letras. Para cada n de 10 a 850, contar quantas
vezes f se aplica antes de aparecer uma letra.
- A conta antes: de 1 a 850 há 9 + 90 + 200 + 53 = **352** números sem letra no hexadecimal (1 dígito: 9; 2 dígitos: 9·10; 0x100–0x2FF: 2·100;
  0x300–0x352: 5·10 + 3). Para n de 10 a 850: p₁ = (352 − 9)/841 = 0,408. Depois, os números crescem: com 4 dígitos hexadecimais, p₂ ≈ (9/15)(10/16)³ =
  0,146; com 5, p₃ ≈ (9/15)(10/16)⁴ = 0,092. Supondo independência: E = p₁ + p₁p₂ + p₁p₂p₃ = 0,408 + 0,0596 + 0,0055 = **0,473**.
- (d) a contagem exata de 1 a 850 dá **352**
- (e) a média de passos em **[0,40; 0,55]** (±15% em torno da conta; a independência pode falhar, porque os dígitos de f(n) vêm dos de n)

**P853, rodada 19:** no `dialogo/DIALOGO.md`.

**Refazer (Parte 46), por honestidade:** a execução única das Partes 1–45 foi morta duas vezes por reinícios do contêiner; ela está sendo refeita em blocos
(1–14 da execução única; 15–45 em 9 blocos). A previsão (a) da Parte 46 será pontuada em cada bloco, com a mudança registrada.
