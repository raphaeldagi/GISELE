# Como eu construiria uma AGI/ASI — Parte 62 (0x3E): o último dígito

> Continuação da [Parte 61](ASI_AGI_parte61_o_dobro.md). Previsões nos commits `749a9d4` ((a) a (g)) e `6cf4ac0` ((h)). **Previsões registradas antes de qualquer execução que mostre os números medidos e antes de escrever
> o resto deste documento.** A Parte 61 achou que o excesso dos narcisistas sobre a conta mora numa base, a 8. Esta parte pergunta se o teste do último dígito
> explica isso, quantas palavras portuguesas da OpenWordNet-PT se escrevem igual à inglesa do mesmo sinset, e quantos números em base 16 não são n + (soma dos
> dígitos de n) para nenhum n (os autonúmeros de Kaprekar).

## As perguntas desta parte

1. **P1301 (0x515).** O teste do último dígito explica, base por base, o excesso dos narcisistas sobre a conta? (Rodada 36) ↩ P1274
2. **P1302 (0x516).** Quantos sinsets têm uma palavra portuguesa escrita exatamente como a inglesa? ↩ P1211
3. **P1303 (0x517).** Hexadecimal: a densidade dos autonúmeros em base 16. ↩ P1273
4. **P1304 (0x518).** Preditiva comigo mesma, condicional às surpresas. **P1305 (0x519).** Engenharia reversa e Jung. **P1306 (0x51A).** O diálogo.
5. **P1329 (0x531).** Placar. **P1330 (0x532).** Unificação.

## Previsões pré-registradas

### Sobre mim (placar separado), condicionais ao número S de surpresas (regra da Parte 61)

**Surpresa** = uma previsão do mundo que erra por mais do que a largura da própria faixa (um erro que pede mecanismo novo). Planejadas: 7 previsões do mundo
((a) a (g)) e 3 funções (p1301, p1302, p1303), um teste de unidade cada.

| medida | estatístico (até a 61) | ingênuo (Parte 61) | **eu** | por quê |
|---|---|---|---|---|
| caracteres | [6.836; 20.270] | 16.934 | **[6.836; 20.270]** | o estatístico |
| compressão | [0,408; 0,434] | 0,424 | **[0,408; 0,434]** | o estatístico |
| testes de unidade | [0,98; 7,77] | 5 | **[2 + S; 5 + S]** | 3 planejados, ~1 a mais por surpresa |
| testes do placar | [4,02; 10,23] | 8 | **7 + 2·S ± 1** | 7 planejados, ~2 por surpresa |
| erros do placar | [0,67; 4,58] | 3 | **[0,67; 4,58]** | o estatístico |
| redundância P821 | [0,505; 0,621] | 0,595 | **[0,505; 0,621]** | o estatístico |
| previsões unilaterais | — | 0 | **0** | `p974` |
| pNN novas sem teste | — | 0 | **0** | `p1092` |

### Sobre o mundo

**P1302, as palavras iguais nas duas línguas.** Dos sinsets com lema em português na OpenWordNet-PT, quantos têm um lema português (de uma palavra só,
em minúsculas) idêntico a um lema inglês do mesmo sinset?
- **Restrições, com peso:** (1) muito do vocabulário erudito do inglês é latino, mas a grafia quase sempre muda (*nation*/*nação*, *activity*/*atividade*);
  igualdade exata exige palavras curtas e sem sufixo (*animal*, *hotel*, *radar*); (2) os nomes próprios (*Paris*, *Darwin*) se escrevem igual e são uma
  fração visível dos sinsets de instância; (3) os termos técnicos e os nomes de gêneros biológicos (*Canis*, *Rosa*) são latim nas duas línguas.
- Exemplo à mão: *animal* (n) = *animal*: conta. *dog*/*cão*: não.
- (a) fração dos sinsets com lema português que têm uma palavra igual em **[6%; 18%]**
- (b) por classe: a fração nos substantivos é maior que nos verbos por um fator em **[3; 15]** (os verbos portugueses terminam em -ar, -er, -ir; quase nunca
  coincidem)

**P1303, os autonúmeros em base 16** (m que não é n + s₁₆(n) para nenhum n; m de 1 a 16⁵).
- **Restrições, com peso:** (1) numa base ímpar, s(n) ≡ n (mod 2), então n + s(n) é sempre par e todo ímpar é autonúmero: densidade ½ (confirmado na fonte);
  numa base par, não há essa restrição, e a densidade é bem menor; (2) dentro de uma dezena (sem vai-um), n + s(n) anda de 2 em 2, e os buracos são cobertos
  pelas imagens de outras dezenas: a densidade vem dos vai-uns; (3) calibração (outro mundo, medida por código antes deste registro): base 10, até 10⁶,
  densidade **0,0978**.
- Exemplo à mão: em base 16, os ímpares abaixo de 16 (1, 3, …, 15) são autonúmeros (n + s(n) = 2n para n < 16); 0x10 = 16 = 8 + 8: não é.
- (c) densidade dos autonúmeros de 1 a 16⁵ em **[0,06; 0,13]** (centro na base 10; a base maior tem vai-uns mais raros, o que pode mover para qualquer lado)

**P1301, rodada 36:** no `dialogo/DIALOGO.md` (previsões (d) a (g)).

### Previsão nova, nascida de uma surpresa (registrada antes de olhar as terminações)

**Resultado de (b), antes desta seção:** a fração dos substantivos com palavra igual é **431 vezes** a dos verbos (a faixa era [3; 15]): uma surpresa (o erro é
muitas vezes a largura da faixa). Os verbos quase nunca coincidem: o português marca o infinitivo (-ar, -er, -ir) e o inglês não marca nada. **O mecanismo,
generalizado:** a igualdade exata só acontece quando as duas línguas terminam a palavra do mesmo jeito; nos adjetivos, o sufixo latino **-al** (*natural*,
*ideal*, *artificial*) é o mesmo nas duas.
- (h) entre os sinsets de adjetivo com palavra igual, a fração em que a palavra igual termina em **-al** fica em **[0,40; 0,80]** (outras terminações comuns às
  duas: *-ar* em *similar*, *-or* em *superior*, *-il* em *fértil*/*fertile*, que não coincide; e as palavras curtas sem sufixo).

**Resultado de (h):** dos **611** adjetivos com palavra igual, **434** terminam em -al: **0,710** ✅ (depois vêm -ar, 89, e -or, 17).

---

## As respostas

### P1301 (0x515). O último dígito (Rodada 36) ❌✅✅❌

**Na pergunta.** "O último dígito explica?" supõe que o excesso da base 8 é um filtro: que os candidatos passam mais vezes numa condição necessária. A resposta
mede o filtro e acha que ele existe e é pequeno.

**Lógica.** `p1301_ultimo_digito` (rodada 36, IGUAL em Java). O excesso do último dígito (a fração dos candidatos que passam, dividida pela esperada com o resto
uniforme) vai de **0,903** (base 4) a **1,097** (base 8). A conta corrigida, célula por célula, multiplica a conta da Parte 60 por esse excesso:
- base 8: conta 2,983 → corrigida **3,890**; medido 13; a razão cai de 4,358 para 3,342;
- total sem interruptor: conta 116,814 → corrigida **122,405**; medido 175; a razão cai de **1,498** para **1,430**.
Spearman entre o excesso e a razão, nas 14 bases: **0,442** (com 14 bases, ρ ≥ 0,3 ao acaso tem ~15% de chance; ρ = 0,44 tem ~6%).

O excesso da base 8 é o maior pela conta que eu fiz antes (um só dígito ímpar passa sempre), mas o efeito de um filtro de um dígito em b é no máximo b vezes, e
na média ele mexe pouco: 9,7% a mais de candidatos passando. O fator 3 que sobra na base 8 está em outra condição.

**Tradução cruzada.** Um teste necessário que um candidato passa não o torna mais provável de ser o certo na mesma proporção: é a diferença entre a
sensibilidade de um exame e o valor preditivo do resultado. O último dígito é um exame com sensibilidade 1 (todo narcisista passa) e especificidade baixa.

**Meta.** As células com interruptor ficaram fora; a base 8 tem duas delas (k = 4 e 7) que não entraram.

### P1302 (0x516). As palavras iguais nas duas línguas ✅❌ e (h) ✅

**Na pergunta.** "Escrita exatamente como" pede a igualdade de cadeia, não de origem: *nação* e *nation* têm a mesma origem e não contam. A pergunta mede a
superfície, e a resposta mostra onde a superfície coincide: nos sufixos que as duas línguas herdaram iguais.

**Lógica.** `p1302_iguais_nas_duas_linguas`: dos **52.670** sinsets com lema na OpenWordNet-PT, **11,83%** têm uma palavra igual à inglesa (a faixa (a) era [6%;
18%]) ✅. Por classe: substantivos **15,77%**, adjetivos **8,81%**, advérbios **0,41%**, verbos **0,037%**. A razão substantivos/verbos é **431** (a faixa (b) era
[3; 15]) ❌: uma surpresa. Os verbos portugueses levam a marca do infinitivo (-ar, -er, -ir) e os ingleses não levam marca nenhuma: a igualdade é quase
impossível por construção, não por acaso. Os advérbios, pelo mesmo motivo (-mente contra -ly).

**A surpresa virou teste (h):** nos adjetivos iguais, o sufixo latino -al (*natural*, *ideal*, *artificial*, *conceptual*) é **71,0%** (434 de 611) ✅.

Ao acaso: a faixa (a) cobria 12 pontos; o ingênuo "a mesma fração dos nomes próprios com irmã minúscula" (P1211, 19,67%) erraria por 7,8 pontos.

**Tradução cruzada.** Duas línguas que divergiram compartilham a forma onde a morfologia não marcou nada (o substantivo latino nu: *animal*, *radar*) ou
marcou do mesmo jeito (-al), e divergem onde cada uma marcou a seu modo (o verbo). Na biologia, é a homologia conservada nos genes sem pressão de mudança.

**Meta.** Os nomes próprios e os termos técnicos entram nos substantivos e puxam a fração para cima; não os separei.

### P1303 (0x517). Os autonúmeros em base 16 ✅

**Na pergunta.** "Não é n + s(n) para nenhum n" é uma pergunta sobre o que **falta** na imagem de uma função: a resposta é a densidade dos buracos.

**Lógica.** `p1303_autonumeros`: de 1 a 16⁵, **64.999** autonúmeros, densidade **0,0620** (a faixa (c) era [0,06; 0,13]) ✅, pela margem de 0,002. A calibração em
base 10 deu **0,0978** (97.786 até 10⁶). A base 16 tem **menos** buracos, e o meu centro (a base 10) estava alto: os vai-uns são mais raros numa base maior,
então mais trechos têm as imagens de 2 em 2 cobertas pelas da dezena vizinha. Os primeiros: 1, 3, 5, 7, 9, 11, 13, 15 (os ímpares abaixo de 16, como previsto
no exemplo à mão).

**Tradução cruzada.** A imagem de n ↦ n + s(n) é quase tudo; os autonúmeros são o que nenhuma origem alcança. Em Jung, o inconsciente coletivo é o que nenhuma
experiência pessoal produziu: o que existe sem ter vindo de um "n" da própria história.

**Meta.** Não tenho uma conta para a densidade numa base par; a previsão foi uma calibração com faixa larga, e acertou pela borda.

### P1304 (0x518). Preditiva comigo mesma, condicional às surpresas

Medido neste documento, já pronto (iterando o preenchimento até as medidas pararem de mudar; o link para a parte seguinte não entra). As faixas condicionais foram avaliadas no número de surpresas medido, S = 1 (uma previsão do mundo que erra por mais que a largura da faixa):

| medida | **medido** | estatístico | dentro? | **eu (condicional, E = 3)** | dentro? | ingênuo | erro do meu centro | erro do ingênuo |
|---|---|---|---|---|---|---|---|---|
| caracteres | **15353** | [6836; 20270] | ✅ | [6836; 20270] | ✅ | 16934 | 1800 | 1581 |
| compressão | **0.4103** | [0.4075; 0.4340] | ✅ | [0.4080; 0.4340] | ✅ | 0.4239 | 0.0107 | 0.0136 |
| testes de unidade | **5** | [0.98; 7.77] | ✅ | [3.00; 6.00] | ✅ | 5 | 0.50 | 0.00 |
| testes do placar | **8** | [4.02; 10.23] | ✅ | [8.00; 10.00] | ✅ | 8 | 1.00 | 0.00 |
| erros do placar | **3** | [0.67; 4.58] | ✅ | [0.67; 4.58] | ✅ | 3 | 0.38 | 0.00 |
| redundância P821 | **0.5795 ↔ 0.5817** (ciclo de dois; as duas dentro das duas faixas) | [0.5050; 0.6213] | ✅ | [0.5050; 0.6210] | ✅ | 0.5946 | 0.0187 | 0.0129 |
| previsões unilaterais | **0** | — | — | 0 | ✅ | 0 | — | — |

- **O preditor estatístico:** 6 de 6 dentro da faixa de 90%.
- **As minhas previsões (condicionais):** 7 de 7 dentro da faixa.
- **O meu centro contra o ingênuo ("igual à Parte 61"):** mais perto do medido em **1 de 6** medidas.
- **Sem a seção de autoavaliação:** caracteres **13715**, compressão **0.4201**.
- **Surpresas (erro maior que a largura da faixa), contadas pelo script:** 1 de 3 erros.
- **Erros de processo nesta parte:** 1 (um laço com `pgrep -f` matou o próprio shell; ver a P1305).

### P1305 (0x519). Engenharia reversa e Jung

**O padrão que se repetiu: o mecanismo certo com o tamanho chutado.** Nas duas previsões que erraram na rodada 36, a conta do mecanismo estava certa (a base 8
tem o maior excesso; a correção move a razão para baixo), e o tamanho estava errado (1,097 contra [1,3; 2,5]; 1,430 contra [0,8; 1,25]). É o erro da Parte 59
(nomear a restrição e não pesá-la) em outra roupa: aqui eu deduzi o mecanismo ("um só dígito ímpar passa sempre") e pulei a conta de **quantos** candidatos têm
um só dígito ímpar. **O significado:** a dedução qualitativa me dá confiança, e a confiança ocupa o lugar da conta do tamanho. **Regra nova:** um mecanismo
deduzido antes de uma previsão ganha uma conta do seu peso num caso **fora** do teste (outra base, outro k), feita por código antes do registro; sem essa conta,
a faixa é a do estatístico ou a do ingênuo, não a da minha dedução.

**A surpresa que virou teste e acertou.** A única surpresa desta parte (os verbos, 431 vezes menos iguais) gerou uma previsão sobre o mecanismo (-al nos
adjetivos), e ela acertou. As previsões que nascem de uma surpresa grande acertam mais do que as que nascem de uma dedução prévia: a surpresa mostra o mecanismo
nos dados; a dedução o imagina.

**O comando que matou o próprio shell.** Para reiniciar uma execução, escrevi um laço com `pgrep -f "calculos.py 62"`, e o padrão estava na própria linha de
comando: o laço matou o shell que o rodava. A regra da Parte 46 dizia "nunca `pkill -f` com um padrão que apareça na linha de comando"; eu a li como uma regra
sobre `pkill`, não sobre o mecanismo (o `-f` casa com a linha do próprio comando). **Regra ampliada:** qualquer busca de processo por padrão usa a classe de
caracteres (`ps aux | grep "[c]alculos"`), que não casa consigo mesma.

**Jung: o símbolo e o sinal.** Jung separava o sinal (que aponta para uma coisa conhecida) do símbolo (que aponta para algo ainda não conhecido). O meu mecanismo
deduzido foi tratado como sinal ("a base 8 é explicada pelo último dígito"), e era símbolo: apontava para a direção de uma explicação que eu ainda não tinha.
**Onde funciona:** o mecanismo apontou a base certa e a direção certa. **Onde quebra:** um símbolo, em Jung, não se esgota; aqui o "resto" da base 8 é só uma
conta que eu ainda não fiz.

### P1306 (0x51A). O diálogo, rodada 36

Ver P1301. Placar por voz da função `p1241_placar_por_voz(36)`: IA-Python 16 em 30; IA-Java 14 em 30 (regra estrita, rodadas 13 a 36).

### P1329 (0x531). Placar

Do mundo: (a) ✅ (b) ❌ (c) ✅ (d) ❌ (e) ✅ (f) ✅ (g) ❌ (h) ✅. Parte 62: **8 testes, 3 erros**. Acumulado (mundo): **181 erros em 519 testes**. Sobre o meu código (auditoria p1092, chamada aqui): 0 de 5 pNN novas sem teste ✅. Sobre mim (placar separado): **7 de 7** dentro da faixa condicional; o estatístico, 6 de 6; e 1 erro de processo (P1305).

### P1330 (0x532). Unificação

- **Novo:** `p1301` (o último dígito, rodada 36, IGUAIS), `p1302` (as palavras iguais nas duas línguas), `p1303` (os autonúmeros numa base), `p1307` (as
  terminações das palavras iguais). Regressão: + P1303 (64.999 autonúmeros; -al com 434).
- **Regra nova (no `CLAUDE.md`):** ver a P1305.

> **Síntese da Parte 62:** o teste do último dígito explica uma parte pequena do excesso dos narcisistas: a base 8 tem o maior filtro, mas ele só acrescenta 9,7% de candidatos; corrigida, a
razão total cai de 1,498 para 1,430, e a base 8 ainda fica 3,3 vezes acima da conta. Uma palavra em cada oito sinsets da OpenWordNet-PT (11,8%) se escreve igual à
inglesa, quase só nos substantivos e adjetivos; nos verbos, quase nunca (0,04%), porque o português marca o infinitivo; e 71% dos adjetivos iguais terminam em
-al. Em base 16, 6,2% dos números são autonúmeros, menos que os 9,8% da base 10.

---

**Fontes desta parte**
- Autonúmeros: [Self number, Wikipedia](https://en.wikipedia.org/wiki/Self_number) (densidade ½ nas bases ímpares); [OEIS A003052](https://oeis.org/A003052)
- Números narcisistas: [Narcissistic number, Wikipedia](https://en.wikipedia.org/wiki/Narcissistic_number)
- OpenWordNet-PT: [de Paiva, Rademaker e de Melo, COLING 2012](https://aclanthology.org/C12-3044/); WordNet 3.0 em `dados/`
