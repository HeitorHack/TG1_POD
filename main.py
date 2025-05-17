
import sys
import random
from RPG.classe import Guerreiro, Mago, Ladino
from RPG.habilidade import BolaDeFogo, Cura, TiroDeArco
from RPG.personagem import Personagem
from RPG.arena import Arena
from RPG.item import PocaoDeVida, Bomba, Escudo, AnelMagico, PocaoDeAtaque, PocaoDeDefesa

# Dicionários de classes e habilidades
CLASSES = {
    "Guerreiro": Guerreiro,
    "Mago": Mago,
    "Ladino": Ladino
}

HABILIDADES = {
    "BolaDeFogo": BolaDeFogo,
    "Cura": Cura,
    "Tiro de Arco": TiroDeArco
}

ITENS_DISPONIVEIS = [
    PocaoDeVida, Bomba, Escudo, AnelMagico, PocaoDeAtaque, PocaoDeDefesa
]

def registrar_erro(mensagem):
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(mensagem + "\n")

def carregar_personagens(caminho_md):
    personagens = []
    with open(caminho_md, "r", encoding="utf-8") as f:
        linhas = f.readlines()

    nome = None
    classe_nome = None
    habilidades = []

    for linha in linhas:
        linha = linha.strip()
        if linha.startswith("### "):
            if nome:
                personagem = criar_personagem(nome, classe_nome, habilidades)
                if personagem:
                    personagens.append(personagem)
            nome = linha.replace("### ", "")
            classe_nome = None
            habilidades = []
        elif linha.startswith("- **Classe**"):
            classe_nome = linha.split(":")[-1].strip()
        elif linha.startswith("- ") or linha.startswith("  - "):
            hab = linha.strip("- *")
            habilidades.append(hab)

    if nome:
        personagem = criar_personagem(nome, classe_nome, habilidades)
        if personagem:
            personagens.append(personagem)

    return personagens

def criar_personagem(nome, classe_nome, habilidades_str):
    if classe_nome not in CLASSES:
        registrar_erro(f"Classe invalida para personagem {nome}: {classe_nome}")
        return None

    classe = CLASSES[classe_nome]()
    habilidades = []
    for h in habilidades_str:
        if h in HABILIDADES:
            habilidades.append(HABILIDADES[h]())
        else:
            registrar_erro(f"Habilidade invalida para personagem {nome}: {h}")

    if len(habilidades) > classe.limite_habilidades:
        registrar_erro(f"{nome} possui habilidades demais: {len(habilidades)} > {classe.limite_habilidades}")
        return None

    itens = random.sample(ITENS_DISPONIVEIS, 2)
    return Personagem(nome, classe, habilidades, [item() for item in itens])

def listar_personagens(personagens):
    if not personagens:
        print("\n[Nenhum personagem carregado. Verifique o arquivo config.md ou o log.txt]\n")
    else:
        print("\n=== PERSONAGENS DISPONÍVEIS ===")
        for i, p in enumerate(personagens):
            habilidades = ", ".join(h.__class__.__name__ for h in p.inventario)
            print(f"{i} - {p.nome} ({p.classe})")
            print(f"    Habilidades: {habilidades}")

def escolher_personagem(personagens):
    while True:
        try:
            listar_personagens(personagens)
            idx = int(input("Escolha o personagem (número): "))
            if 0 <= idx < len(personagens):
                return personagens[idx]
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def menu():
    print("\n=== MENU ===")
    print("1. Combate entre dois personagens")
    print("2. Free For All")
    print("0. Sair")
    return input("Escolha: ")

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py config.md")
        sys.exit(1)

    personagens = carregar_personagens(sys.argv[1])
    if not personagens:
        print("Nenhum personagem carregado. Encerrando o programa.")
        sys.exit(1)

    arena = Arena()

    while True:
        opcao = menu()
        if opcao == "1":
            print("Escolha dois personagens para o duelo:")
            p1 = escolher_personagem(personagens)
            p2 = escolher_personagem(personagens)
            arena.combate(p1, p2)
        elif opcao == "2":
            for p in personagens:
                arena.adicionar_personagem(p)
            arena.free_for_all()
        elif opcao == "0":
            print("Saindo...")
            sys.exit(0)
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
