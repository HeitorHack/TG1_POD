from RPG.classe import Classe
from RPG.habilidade import Habilidade

class Personagem:
    def __init__(self, nome: str, classe: Classe, habilidades=None, itens=None):
        self.nome = nome
        self.classe = classe
        self.inventario = habilidades[:classe.limite_habilidades] if habilidades else []
        self.itens = itens if itens else []
        self.pontos_vida = classe.pontos_vida
        self.dado_de_ataque = classe.dado_de_ataque
        self.pontos_ataque = classe.pontos_ataque
        self.pontos_defesa = classe.pontos_defesa
        self._buff_ataque = 0
        self._buff_defesa = 0
        self._imune = False

        self.nivel = 1
        self.xp = 0
        self.limite_base_habilidades = classe.limite_habilidades

    def __eq__(self, other):
        return self.nome == other.nome and self.classe.nome == other.classe.nome

    def __str__(self):
        return f"{self.nome} ({self.classe}) Nível {self.nivel}"

    def __repr__(self):
        return f"Personagem({self.nome})"

    def aplicar_buffs(self):
        ataque = self.pontos_ataque + int(self._buff_ataque)
        defesa = self.pontos_defesa + int(self._buff_defesa)
        self._buff_ataque = 0
        self._buff_defesa = 0
        return ataque, defesa

    def usar_habilidade(self, alvo):
        if not self.inventario:
            return 0
        habilidade = self.inventario.pop(0)
        dano = habilidade.usar()
        if dano < 0:
            self.pontos_vida += abs(dano)
            return -dano
        else:
            alvo.pontos_vida -= dano
            return dano

    def atacar(self, alvo):
        import random
        if self.inventario and random.randint(1, 100) <= 50:
            return self.usar_habilidade(alvo)

        rolagem = self.dado_de_ataque.jogar()
        valor_ataque = rolagem + self.pontos_ataque

        if valor_ataque > alvo.pontos_defesa:
            alvo.pontos_vida -= valor_ataque
            return valor_ataque
        return 0

    def usar_item(self, alvo):
        if not self.itens:
            return ("nenhum", 0)
        item = self.itens.pop(0)
        efeito, valor = item.usar(self, alvo)
        if efeito == "buff_ataque_temporario":
            self._buff_ataque = int(valor)
        elif efeito == "buff_defesa_temporario":
            self._buff_defesa = int(valor)
        return efeito, valor

    def ganhar_xp(self, quantidade, relatorio=None):
        self.xp += quantidade
        if relatorio is not None:
            relatorio.append(f"{self.nome} ganhou {quantidade} XP (total: {self.xp})")

        while self.xp >= self._xp_para_proximo_nivel():
            self.xp -= self._xp_para_proximo_nivel()
            self.nivel += 1
            self.pontos_vida += 3
            self.pontos_ataque += 1
            self.pontos_defesa += 1
            self.classe.limite_habilidades += 1
            if relatorio is not None:
                relatorio.append(f"{self.nome} subiu para o nível {self.nivel}!")
                relatorio.append("Ganhou +3 vida, +1 ataque, +1 defesa, +1 habilidade")

    def _xp_para_proximo_nivel(self):
        return 10 + (self.nivel - 1) * 10

























































