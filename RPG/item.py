
from abc import ABC, abstractmethod

class Item(ABC):
    @abstractmethod
    def usar(self, usuario, alvo):
        pass

class PocaoDeVida(Item):
    def usar(self, usuario, alvo):
        usuario.pontos_vida += 10
        return ("cura", 10)

class Bomba(Item):
    def usar(self, usuario, alvo):
        alvo.pontos_vida -= 8
        return ("dano", 8)

class Escudo(Item):
    def usar(self, usuario, alvo):
        usuario._imune = True
        return ("escudo", 0)

class AnelMagico(Item):
    def usar(self, usuario, alvo):
        usuario.pontos_ataque += 2
        return ("buff_ataque", 2)

class PocaoDeAtaque(Item):
    def usar(self, usuario, alvo):
        return ("buff_ataque_temporario", 2)

class PocaoDeDefesa(Item):
    def usar(self, usuario, alvo):
        return ("buff_defesa_temporario", 2)
