"""Fontes reproduzíveis por domínio e coordenadas, sem consumo global compartilhado."""

import hashlib
import json
import random
import sys
from dataclasses import dataclass


PROTOCOLO_ALEATORIO = "synthai-mundos-v2"


@dataclass(frozen=True)
class FontesAleatorias:
    semente: int
    mundo: str

    def __post_init__(self):
        if type(self.semente) is not int or not isinstance(self.mundo, str) or not self.mundo:
            raise ValueError("semente deve ser inteira e mundo deve ter um nome")

    def gerador(self, canal, *coordenadas):
        if not isinstance(canal, str) or not canal or any(type(c) is not int or c < 0 for c in coordenadas):
            raise ValueError("canal deve ter nome e coordenadas devem ser inteiros não negativos")
        texto = json.dumps([PROTOCOLO_ALEATORIO, self.semente, self.mundo, canal, coordenadas],
                           separators=(",", ":"), ensure_ascii=False)
        semente = int.from_bytes(hashlib.sha256(texto.encode()).digest(), "big")
        return random.Random(semente)

    def uniforme(self, canal, *coordenadas):
        return self.gerador(canal, *coordenadas).random()

    @property
    def manifesto(self):
        return {"protocolo": PROTOCOLO_ALEATORIO, "semente": self.semente, "mundo": self.mundo,
                "derivacao": "SHA-256(JSON compacto UTF-8 de [protocolo,semente,mundo,canal,coordenadas])",
                "gerador": "random.Random", "python": sys.version,
                "implementacao": sys.implementation.name}
