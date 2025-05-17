from abc import ABC, abstractmethod
from .dado import Dado, D6, D8, D12

class Classe(ABC):
    def __init__(self, nome, pontos_vida, dado_de_ataque: Dado, pontos_ataque, pontos_defesa, limite_habilidades):
        self.nome = nome
        self.pontos_vida = pontos_vida
        self.dado_de_ataque = dado_de_ataque
        self.pontos_ataque = pontos_ataque
        self.pontos_defesa = pontos_defesa
        self.limite_habilidades = limite_habilidades

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f"Classe({self.nome})"


from .dado import D12


class Guerreiro(Classe):
    def __init__(self):
        pontos_defesa = 8
        super().__init__(
            nome="Guerreiro",
            pontos_vida=10 + (pontos_defesa * 5),
            dado_de_ataque=D12(),
            pontos_ataque=6,
            pontos_defesa=pontos_defesa,
            limite_habilidades=2
        )


from .dado import D6


class Mago(Classe):
    def __init__(self):
        pontos_defesa = 3
        super().__init__(
            nome="Mago",
            pontos_vida=8 + (pontos_defesa * 2),
            dado_de_ataque=D6(),
            pontos_ataque=10,
            pontos_defesa=pontos_defesa,
            limite_habilidades=5
        )


from .dado import D8


class Ladino(Classe):
    def __init__(self):
        pontos_defesa = 5
        super().__init__(
            nome="Ladino",
            pontos_vida=6 + (pontos_defesa * 3),
            dado_de_ataque=D8(),
            pontos_ataque=8,
            pontos_defesa=pontos_defesa,
            limite_habilidades=3
        )
