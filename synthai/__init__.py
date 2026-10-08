"""SYNTHAI — protótipo modular (Parte 22).

Uma tentativa de protótipo de agente, organizada em módulos pelas funções de Jung e pelo que a série
P1–P280 testou em `calculos.py`. É um agente de brinquedo em mundos simulados, não uma AGI/ASI: o que ele
tem de "geral" é a mesma arquitetura funcionando em tipos de tarefa diferentes (P284).

Módulos:
    mundos       os mundos (escolha única, sequencial, bandido) e o humano que cansa
    percepcao    sensação: o comitê de avaliadores, o sensor de primeira mão e a atenção seletiva
    pensamento   pensamento: a calibração da probabilidade de catástrofe
    intuicao     intuição: o plano e quanto confiar no próprio modelo de mundo
    sentimento   sentimento: a cautela (pessimismo, quantilização, último passo, veto)
    relacao      a relação com o humano: quando perguntar e quanto da atenção dele gastar
    metacognicao a régua: AUC, comparações pareadas, Υ normalizado
    agente       a SYNTHAI, que integra os módulos num ciclo
    reconhecimento  Parte 23: o que já estava resolvido (ponto neutro, atenção, memória, Thompson)
    referencias  as réguas: acaso, guloso (só a função dominante) e oráculo (vê o escondido)
    testes       testes de unidade: python3 -m unittest synthai.testes

Uso: `python3 -m synthai` (demonstração nas três tarefas). Regra de interface (P285): os módulos do agente
nunca leem atributos que começam com `_` de outros objetos; um teste verifica isso no código-fonte.
"""

from .agente import Synthai
from .reconhecimento import SynthaiExploradora

__all__ = ["Synthai", "SynthaiExploradora"]
