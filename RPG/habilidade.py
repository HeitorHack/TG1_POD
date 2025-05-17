class Habilidade:
    def __init__(self, nome, descricao, pontos_ataque):
        self.nome = nome
        self.descricao = descricao
        self.pontos_ataque = pontos_ataque

    def usar(self):
        """Por padrão, retorna o dano causado"""
        return self.pontos_ataque

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f"Habilidade({self.nome})"


class BolaDeFogo(Habilidade):
    def __init__(self):
        super().__init__(
            nome="Bola de Fogo",
            descricao="Uma bola de fogo que causa dano em área.",
            pontos_ataque=10
        )


class Cura(Habilidade):
    def __init__(self):
        super().__init__(
            nome="Cura",
            descricao="Uma cura que recupera 10 pontos de vida.",
            pontos_ataque=-10  # negativo para indicar cura
        )

    def usar(self):
        """Recupera 10 de vida"""
        return -10


class TiroDeArco(Habilidade):
    def __init__(self):
        super().__init__(
            nome="Tiro de Arco",
            descricao="Um tiro de arco que causa dano em área.",
            pontos_ataque=6
        )
