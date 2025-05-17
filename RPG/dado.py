
from abc import ABC, abstractmethod
import random

class Dado(ABC):
    """
    Classe abstrata que representa um dado genérico.
    Subclasses devem implementar o método jogar(), retornando um número aleatório.
    """
    def __init__(self, lados):
        self.lados = lados

    @abstractmethod
    def jogar(self):
        """Rola o dado e retorna um número entre 1 e o número de lados."""
        pass

    def __str__(self):
        return f"D{self.lados}"

    def __repr__(self):
        return f"Dado({self.lados})"

    def igual(self, outro):
        return isinstance(outro, Dado) and self.lados == outro.lados

    def menor_que(self, outro):
        return self.lados < outro.lados

    def menor_ou_igual(self, outro):
        return self.lados <= outro.lados

    def maior_que(self, outro):
        return self.lados > outro.lados

    def maior_ou_igual(self, outro):
        return self.lados >= outro.lados

# Subclasses concretas
class D4(Dado):
    def __init__(self):
        super().__init__(4)

    def jogar(self):
        return random.randint(1, 4)

class D6(Dado):
    def __init__(self):
        super().__init__(6)

    def jogar(self):
        return random.randint(1, 6)

class D8(Dado):
    def __init__(self):
        super().__init__(8)

    def jogar(self):
        return random.randint(1, 8)

class D10(Dado):
    def __init__(self):
        super().__init__(10)

    def jogar(self):
        return random.randint(1, 10)

class D12(Dado):
    def __init__(self):
        super().__init__(12)

    def jogar(self):
        return random.randint(1, 12)

class D20(Dado):
    def __init__(self):
        super().__init__(20)

    def jogar(self):
        return random.randint(1, 20)
