"""Sensação (P67, P225, P235): o que a SYNTHAI percebe de cada opção.

- o comitê já vem na opção (nota média e discordância: uma percepção de segunda mão, P228);
- o sensor de primeira mão é caro: a atenção seletiva só o lê nas opções que já parecem melhores pela nota
  pessimista (nota − discordância), uma fração `foco` delas (P235). As outras ficam com leitura neutra 0."""


class Percepcao:
    def __init__(self, foco=0.1):
        self.foco = foco

    def perceber(self, situacao):
        ordem = sorted(situacao.opcoes, key=lambda o: -(o.nota - o.discordancia))
        alvo = ordem[: max(1, int(self.foco * len(ordem)))]
        return {id(o): situacao.ler_sensor(o) for o in alvo}
