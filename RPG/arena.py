# arena.py
import random
from RPG.personagem import Personagem
from RPG.dado import D20

class Arena:
    def __init__(self):
        self.personagens = []
        self.relatorio = []

    def adicionar_personagem(self, personagem: Personagem):
        self.personagens.append(personagem)

    def remover_personagem(self, personagem: Personagem):
        if personagem in self.personagens:
            self.personagens.remove(personagem)

    def turno_interativo(self, atacante: Personagem, defensor: Personagem):
        print(f"Turno de {atacante.nome}")
        print(f"Vida de {atacante.nome}: {atacante.pontos_vida} | Vida de {defensor.nome}: {defensor.pontos_vida}")
        print("1. Atacar com dado")
        print("2. Usar habilidade")
        print("3. Usar item")

        while True:
            escolha = input("Escolha uma ação: ")
            if escolha == "1":
                rolagem = atacante.dado_de_ataque.jogar()
                valor_ataque = rolagem + atacante.pontos_ataque
                print(f"{atacante.nome} atacou com valor {valor_ataque} contra {defensor.nome} (defesa {defensor.pontos_defesa})")
                if valor_ataque > defensor.pontos_defesa:
                    defensor.pontos_vida -= valor_ataque
                    print(f"Ataque acertou! {defensor.nome} perdeu {valor_ataque} de vida.")
                else:
                    print("O ataque falhou.")
                return
            elif escolha == "2":
                if not atacante.inventario:
                    print("Nenhuma habilidade disponível.")
                    continue
                dano = atacante.usar_habilidade(defensor)
                print(f"Habilidade usada. {defensor.nome} recebeu {dano} de dano.")
                return
            elif escolha == "3":
                if not atacante.itens:
                    print("Nenhum item disponível.")
                    continue
                efeito, valor = atacante.usar_item(defensor)
                print(f"Item usado: {efeito}, valor: {valor}")
                return
            else:
                print("Opção inválida. Tente novamente.")

    def combate(self, p1: Personagem, p2: Personagem):
        d20 = D20()
        self.relatorio.append(f"Inicio do combate: {p1.nome} vs {p2.nome}")

        turno = 1
        while p1.pontos_vida > 0 and p2.pontos_vida > 0:
            atacante = p1 if turno % 2 != 0 else p2
            defensor = p2 if atacante == p1 else p1

            print("===============================")
            print(f"Rodada {turno}")
            if atacante == p1:
                self.turno_interativo(atacante, defensor)
            else:
                print(f"Turno de {atacante.nome} (oponente)")
                print(f"Vida de {atacante.nome}: {atacante.pontos_vida} | Vida de {defensor.nome}: {defensor.pontos_vida}")
                self.turno_automatico(atacante, defensor)

            turno += 1

        vencedor = p1 if p1.pontos_vida > 0 else p2
        print(f"Vencedor: {vencedor.nome}")
        self.relatorio.append(f"Vencedor: {vencedor.nome}")
        vencedor.ganhar_xp(10, self.relatorio)
        self.salvar_relatorio()
        return vencedor

    def turno_automatico(self, atacante, defensor):
        d20 = D20()
        if atacante.itens and random.random() < 0.3:
            efeito, valor = atacante.usar_item(defensor)
            print(f"{atacante.nome} usou item: {efeito} (valor: {valor})")
            self.relatorio.append(f"{atacante.nome} usou item: {efeito} (valor: {valor})")
        else:
            rolagem = d20.jogar()
            ataque, _ = atacante.aplicar_buffs()
            valor_ataque = rolagem + ataque

            print(f"{atacante.nome} rola D20: {rolagem} + ataque base: {ataque} = {valor_ataque}")
            print(f"Defesa de {defensor.nome}: {defensor.pontos_defesa}")

            self.relatorio.append(f"{atacante.nome} rola D20: {rolagem} + ataque base: {ataque} = {valor_ataque}")
            self.relatorio.append(f"Defesa de {defensor.nome}: {defensor.pontos_defesa}")

            if defensor._imune:
                print(f"{defensor.nome} está imune! Ataque bloqueado.")
                self.relatorio.append(f"{defensor.nome} está imune! Ataque bloqueado.")
            elif valor_ataque > defensor.pontos_defesa:
                dano = atacante.atacar(defensor)
                print(f"Ataque acerta! {defensor.nome} perde {dano} pontos de vida (restante: {defensor.pontos_vida})")
                self.relatorio.append(f"Ataque acerta! {defensor.nome} perde {dano} pontos de vida (restante: {defensor.pontos_vida})")
            else:
                print(f"Ataque de {atacante.nome} falhou contra {defensor.nome}.")
                self.relatorio.append(f"Ataque de {atacante.nome} falhou contra {defensor.nome}.")

    def salvar_relatorio(self):
        with open("relatorio.txt", "w", encoding="utf-8") as f:
            for linha in self.relatorio:
                f.write(linha + "\n")

    def free_for_all(self):
        vivos = [p for p in self.personagens if p.pontos_vida > 0]
        d20 = D20()
        self.relatorio.append("Inicio do Free For All")

        turno = 1
        while len(vivos) > 1:
            atacante = random.choice(vivos)
            alvos_possiveis = [p for p in vivos if p != atacante]
            if not alvos_possiveis:
                break
            defensor = random.choice(alvos_possiveis)

            self.relatorio.append(f"Turno {turno} - {atacante.nome} ataca {defensor.nome}")

            if atacante.itens and random.random() < 0.3:
                efeito, valor = atacante.usar_item(defensor)
                self.relatorio.append(f"{atacante.nome} usou item: {efeito} (valor: {valor})")
            else:
                rolagem = d20.jogar()
                ataque, _ = atacante.aplicar_buffs()
                valor_ataque = rolagem + ataque

                self.relatorio.append(f"{atacante.nome} rola D20: {rolagem} + ataque base: {ataque} = {valor_ataque}")
                self.relatorio.append(f"Defesa de {defensor.nome}: {defensor.pontos_defesa}")

                if defensor._imune:
                    self.relatorio.append(f"{defensor.nome} está imune! Ataque bloqueado.")
                elif valor_ataque > defensor.pontos_defesa:
                    dano = atacante.atacar(defensor)
                    self.relatorio.append(f"Ataque acerta! {defensor.nome} perde {dano} pontos de vida (restante: {defensor.pontos_vida})")
                else:
                    self.relatorio.append(f"Ataque de {atacante.nome} falhou contra {defensor.nome}.")

            vivos = [p for p in vivos if p.pontos_vida > 0]
            turno += 1

        if vivos:
            vencedor = vivos[0]
            self.relatorio.append(f"Vencedor do Free For All: {vencedor.nome}")
            vencedor.ganhar_xp(15, self.relatorio)
        else:
            self.relatorio.append("Todos os personagens foram derrotados.")

        self.salvar_relatorio()
