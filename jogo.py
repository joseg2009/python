import random
cura = True

def exibir_barra_hp(nome, hp, hp_max):
    porcentagem = int((hp / hp_max) * 10)  # Calcula a porcentagem de HP
    barra = "█" * porcentagem + "░" * (10 - porcentagem)  # Monta a barra
    print(f"{nome}: [{barra}] {hp}/{hp_max}")  # Exibe barra e valores

personagem = {
    "nome": "JT",
    "hp_max": 100,
    "hp_atual": 100,
    
    "habilidades": {
        "cassetete": {
            "dano": 10,
            "tipo": "contudente",
        },  # <-- Adicionada a vírgula aqui
        "pistola": {
            "dano": 25,
            "mun_max": 12,
            "mun_atual": 12,
            "tipo": "perfurante",
        },
    },
}
nome = personagem["nome"]

bestiario = {
    1: {
        "nome": "mulher",
        "hp_max": 75,
        "hp_atual": 75,
        "habilidades": {
            1: {"ataque":"apunhalar", "dano" : 12},
            2: {"ataque":"Ecos da Escuridão", "dano" : 17},
            3: {"ataque":"Cansaço", "dano" : 0}
        },
        "fraqueza": "contudente"
    },
    2: {
        "nome": "amante",
        "hp_max": 125,
        "hp_atual": 125,
        "habilidades": {
            1: {"ataque":"gancho", "dano" : 20},
            2: {"ataque":"dilaçerar", "dano" : 25},
            3: {"ataque":"ancioso",}
        },
        "fraqueza": "perfurante"
    },
    3:{
        "nome": "marido",
        "hp_max": 150,
        "hp_atual": 150,
        "habilidades": {
            1: {"ataque":"cuspe de veneno", "dano" : 22},
            2: {"ataque":"aranhão venenoso", "dano" : 30},
        },
    }
}

def combate (bestiario):
    print(f"inimigo emcontrado a o entrar no recinto {bestiario["nome"]}")
    while True: 

        if personagem["hp_atual"] <= 0:
            break
        if bestiario["hp_atual"] <= 0:
            break

        print("Comandos: \n [a] ATACAR \n [d] DEFENDER \n [f] SAIR \n")
        comando = input("⬆️  Digite um dos comandos acima ⬆️  - ").strip().lower()
        if comando in ["a", "atacar", "ATACAR", "ataca"]:
            acao = "a"
        elif comando in ["d", "defender", "defende","defesa" ]:
            acao = "d"
        elif comando in ["f", "fuga","fugir"]:
            acao = "f"
        else:
            comando = "invalido"

        
        match acao:

            case "a":
                
                print(f"Opção: pistola para um disparo rapido | cassetete para ataques rapidos consecutivos")
                escolha = input("Escolha sua habilidade: ").strip().lower()
                
                match escolha:
                        # pistola
                    case "p" | "pistola" : 
                        pistola = personagem["habilidades"]["pistola"]
                        print(personagem["habilidades"]["pistola"]["dano"])
                        if bestiario["fraqueza"] == "perfurante":
                            bestiario["hp_atual"] -= personagem["habilidades"]["pistola"]["dano"] * 2
                            print(f"Inimigo tomou dano dobrado")
                            exibir_barra_hp(bestiario["nome"],bestiario["hp_atual"],bestiario["hp_max"])
                        else :
                            bestiario["hp_atual"] -= personagem["habilidades"]["pistola"]["dano"]
                            print(f"Inimigo tomou dano ")
                            exibir_barra_hp(bestiario["nome"],bestiario["hp_atual"],bestiario["hp_max"])
                            
                        # cassetete
                    case "c" | "cassetete" :
                        cassetete = personagem["habilidades"]["cassetete"]
                        print(personagem["habilidades"]["cassetete"]["dano"])
                        if bestiario["fraqueza"] == "contudente":
                            bestiario["hp_atual"] -= personagem["habilidades"]["cassetete"]["dano"] * 2
                            print(f"Inimigo tomou dano dobrado")
                            exibir_barra_hp(bestiario["nome"],bestiario["hp_atual"],bestiario["hp_max"])
                        else :
                            bestiario["hp_atual"] -= personagem["habilidades"]["cassetete"]["dano"] 
                            print(f"Inimigo tomou dano ")
                            exibir_barra_hp(bestiario["nome"],bestiario["hp_atual"],bestiario["hp_max"])

            case "d": 
                r = random.randint(1,3)
                personagem["hp_atual"] -= bestiario["habilidades"][r]["dano"] * 0.5
                print(f"Voçê se defendeu tomou apenas metade do dano")
                print(f"Ataque e Dano do inimigo : {bestiario["habilidades"][r]["ataque"]} Dano: {bestiario["habilidades"][r]["dano"]}")
                exibir_barra_hp(nome,personagem["hp_atual"],personagem["hp_max"])

            case "f":
                r = random.randint(1,3)
                personagem["hp_atual"] -= bestiario["habilidades"][r]["dano"] 
                print("Voçê faliu a o fugir do combate")
                print("Voçê tomou dano a o tentar fugir")
                print(f"dano do inimigo {bestiario["habilidades"][r]["ataque"]}{bestiario["habilidades"][r]["dano"] }")
                exibir_barra_hp(nome,personagem["hp_atual"],personagem["hp_max"])

                print(bestiario["habilidades"][r]["ataque"], bestiario["habilidades"][r]["dano"])
                exibir_barra_hp(nome,personagem["hp_atual"],personagem["hp_max"])
                print("voce falhou ao fugir")

        if bestiario["nome"] == "marido" :
            if bestiario["hp_atual"] <= bestiario["hp_max"] * 0.5:
                if cura == True:
                    bestiario["hp_atual"] *= 1.25
                    cura = False




r = random.randint(1,2)
combate (bestiario [r])



    



# print(f"personagem: {personagem}")