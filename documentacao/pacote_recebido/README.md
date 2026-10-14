# SYNTHAI — código consolidado

Esta distribuição reúne as fontes extraídas do material SYNTHAI fornecido, com as correções já verificadas de comparação pareada, abstenção, integridade cooperativa do avaliador e aleatoriedade coordenada. Inclui os dois mecanismos de laboratório, seus testes e seus contratos. O código principal e o laboratório usam a biblioteca padrão; a versão testada é Python 3.12.

## Arquivo único

O arquivo SYNTHAI_consolidado.py contém um ZIP de fontes comprimido, cujo hash é conferido antes da extração. Ao executar, ele extrai para uma pasta temporária, executa o ponto de entrada e remove a pasta ao terminar. Isso permite que o avaliador e os testes acessem os arquivos por __file__. O hash verifica integridade do conteúdo embutido; não constitui uma assinatura de autoria.

```sh
python SYNTHAI_consolidado.py demo
python SYNTHAI_consolidado.py demo --semente 1 --json
python SYNTHAI_consolidado.py testes
python SYNTHAI_consolidado.py laboratorio
python SYNTHAI_consolidado.py info
```

Para conservar uma cópia editável:

```sh
python SYNTHAI_consolidado.py --extrair minha_synthai
cd minha_synthai
python synthai_cli.py demo
python synthai_cli.py testes --relatorio verificacao.json
```

A extração exige um destino vazio. O comando testes pode gravar seu relatório fora da pasta temporária quando --relatorio recebe um caminho escolhido pelo usuário.

## Fontes editáveis

O ZIP de entrega também fornece diretamente synthai_cli.py, verificar.py, fontes/, laboratorio/ e documentacao/. Depois de extrair o pacote, execute synthai_cli.py com os mesmos comandos. Para usar a biblioteca original:

```sh
cd fontes
python -m synthai
```

Os exports públicos originais são Synthai, SynthaiExploradora e SynthaiComposta. calculos.py permanece incluído porque o núcleo e os testes dependem de utilitários históricos. Os scripts históricos estão preservados, mas não são executados automaticamente pelo ponto de entrada.

## Escopo e limites

- Trata-se de um protótipo de agentes em simuladores. A entrega não demonstra AGI, ASI ou a implementação de um milhão de componentes.
- O laboratório permanece separado do ciclo do agente. evidencia.py exige a hipótese Bernoulli condicional e apostas previsíveis; não é um promotor geral para retornos contínuos.
- feedback.py protege no máximo uma atualização do acumulador local por decisão. Não garante execução externa exatamente uma vez, autenticação de origem ou atomicidade de aprendizagem arbitrária.
- O avaliador selado é cooperativo e depende da base inicialmente confiável. Não isola código hostil.
- A regra de promoção de rsi.evoluir permanece uma implementação histórica com validade estatística pendente. Disponibilizá-la no pacote não a transforma em mecanismo de promoção confirmado.
- Os dados binários de WordNet/OpenWordNet-PT não foram recuperados do arquivo original. Experimentos opcionais de léxico dependem desses dados adicionais. A demonstração, a regressão selecionada e o laboratório não os exigem.
- Os testes selecionados conservam alguns ResourceWarning preexistentes de leituras de arquivos. O resultado das verificações deve ser interpretado no escopo registrado.

O registro de validação informa a execução de 123 testes selecionados do núcleo e 27 do laboratório. Isso não significa que todos os testes históricos, datasets ou hipóteses arquiteturais tenham sido verificados.
