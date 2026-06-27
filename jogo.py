import random
import msvcrt
from rich import print
from nava import play,stop
from time import sleep

def esperar_tecla(mensagem):
    print(f'[bold blue] {mensagem}')
    msvcrt.getch()

# ==========================================
# CONFIGURAÇÕES DE DADOS (ESTADO DO JOGO)
# ==========================================

personagem = {
    "nome": "JT",
    "hp_max": 100,
    "hp_atual": 100,
    "inventario": [],  
    "habilidades": {
        "cassetete": {
            "dano": 15,
            "tipo": "contudente",
        },  
        "pistola": {
            "dano": 30,
            "mun_max": 12,
            "mun_atual": 12,
            "tipo": "perfurante",
        },
    },
}

bestiario = {
    1: {
        "id": 1,
        "nome": "mulher (O Espírito Desolado)",
        "hp_max": 75,
        "hp_atual": 75,
        "habilidades": {
            1: {"ataque": "apunhalar", "dano": 12},
            2: {"ataque": "Ecos da Escuridão", "dano": 17},
            3: {"ataque": "Cansaço", "dano": 0}
        },
        "fraqueza": "contudente",
        "drop": None
    },
    2: {
        "id": 2,
        "nome": "Espírito do Amante",
        "hp_max": 130,      # Aumentado (era menor, o que tornava a luta curta)
        "hp_atual": 130,
        "fraqueza": "perfurante",   # Removida a fraqueza para a pistola não dar dano dobrado fácil
        "habilidades": {
            1: {"ataque": "Lamento Dilacerante", "dano": 18},
            2: {"ataque": "Toque Gélido", "dano": 22}
        },
        "drop": "Chave do Porão"
    },
    3: {
        "id": 3,
        "nome": "O Marido (Demônio do Rancor)",
        "hp_max": 105,     
        "hp_atual": 105,
        "fraqueza": None,
        "habilidades": {
            1: {"ataque": "Cuspe de Veneno", "dano": 15},
            2: {"ataque": "Arranhão Venenoso", "dano": 20}
        },
        "drop": None
    }

}

itens_investigacao = {
    "ato1": {
        1: {"nome": "faca ensanguentada", "lore": "Depois de revirar o sofá inteiro é possível encontrar uma faca com sangue seco, talvez tenha sido a arma do crime.", "importante": True, "visto": False},
        2: {"nome": "vinho na mesa", "lore": "As vítimas conheciam o assassino e estavam tomando o vinho junto com ele ou o assassino entrou e acabou encontrando ambos?", "importante": True, "visto": False},
        3: {"nome": "foto rasgada", "lore": "Uma foto de um casal, o rosto masculino da foto está rasgado.", "importante": False, "visto": False},
        4: {"nome": "papeis amassados", "lore": "Dou uma olhada na lata de lixo, e encontro alguns papéis amassados. Um sendo pedido de divórcio e outro sendo uma carta pelo que parece, nela tá escrito repetidas vezes ME DESCULPA.", "importante": True, "visto": False},
        5: {"nome": "anel de casamento", "lore": "Um anel de casamento... Isso é da vítima ou do assassino?", "importante": True, "visto": False},
        6: {"nome": "relogio quebrado", "lore": "O relógio está quebrado no chão, nele marca 22:53.", "importante": True, "visto": False}
    },
    "ato2": {
        1: {"nome": "quadro de casal destruído", "lore": "O quadro que decorava o corredor foi arrancado e jogado na parede. O vidro está estilhaçado e a foto do marido foi violentamente riscada com algo afiado.", "importante": True, "visto": False},
        2: {"nome": "bilhete amoroso rasgado", "lore": "Pedaços de papel no chão do corredor formam uma carta de amor secreta: 'Mal posso esperar para quando ele não estiver em casa...'", "importante": True, "visto": False},
        3: {"nome": "marcas de arrastamento", "lore": "Marcas escuras no piso do corredor indicam que um corpo pesado foi arrastado em direção à porta trancada do porão.", "importante": True, "visto": False},
        4: {"nome": "lamparina quebrada", "lore": "Uma fonte de luz despedaçada no chão. O óleo derramado ainda cheira forte, indicando um confronto físico recente e desesperado no corredor.", "importante": False, "visto": False}
    },
    "ato3": { 
        1: {
            "nome": "frasco de veneno de rato vazio", 
            "lore": "Um frasco de veneno jogado perto do altar. O Marido ingeriu o conteúdo em seus últimos momentos, tentando cometer suicídio para fugir da polícia após o duplo homicídio. O veneno agora corre em suas veias espirituais.", 
            "importante": True, 
            "visto": False
        },
        2: {
            "nome": "altar do ritual fracassado", 
            "lore": "Um cadáver mutilado serve de oferenda no centro de um círculo místico. Notas rabiscadas no chão mostram que o Marido tentou um ritual de ressurreição ou barganha que deu 'errado'... Em vez de salvação, sua alma foi distorcida pelo puro rancor.", 
            "importante": True, 
            "visto": False
        },
        3: {
            "nome": "cartas de desespero e rancor", 
            "lore": "Páginas manchadas de vômito e sangue revelam os últimos pensamentos dele: 'O ritual não funcionou, eles ainda estão mortos e eu estou queimando por dentro...'. O veneno o matou, mas o rancor o trouxe de volta como algo pior.", 
            "importante": True, 
            "visto": False
        }
    }
}

# ==========================================
# INTERFACE VISUAL (HUD)
# ==========================================

def exibir_barra_hp(nome, hp, hp_max):
    if hp < 0: hp = 0
    porcentagem = int((hp / hp_max) * 10)  
    barra = "█" * porcentagem + "░" * (10 - porcentagem)  
    print(f"{nome}: [{barra}] {hp}/{hp_max}")

# ==========================================
# FUNÇÕES DO JOGO (SISTEMAS MODULARES)
# ==========================================

def mostrar_cutscene_inicial(nome_detetive):
    print('\n--- CUTSCENE ---')
    print(f'Você é [bold italic]{nome_detetive}[/bold italic], um detetive especializado em investigar [red]assassinatos[/red].')
    print('Você chegou em casa cansado depois de analisar diferentes relatórios de mortes estranhas.')
    print('Antes que possa descansar, você recebe uma ligação dizendo que na rua XXXXXXXXX\nna casa de número XXX foram encontrados dois corpos.')
    print('[bold blue]-' *20 )
    print('Chegando no local, o policial Rubert, seu colega, te espera...')
    print('[bold blue]-' *20 )
    esperar_tecla('Digite qualquer tecla para continuar')

    print('\n[bold red]ATO 0: INÍCIO')
    print('[bold blue]-' *20 )
    print('(Com um cigarro na boca e cara de cansado, Rubert diz)')
    print(f'[bold]Rubert:[/bold] Boa noite, [italic]{nome_detetive}[/italic], como você está?')
    print('\n[bold]Opções de resposta:\n1[/bold] - Boa noite Rubert, estou bem e você?\n[bold]2[/bold] - Vamos cortar as apresentações, cadê os outros?\n[bold]3[/bold] - Que desperdício de palavras.')

    try:
        escolha = int(input(f'R: '))
    except ValueError:
        escolha = 1

    print('[bold blue]-' *20 )
    if escolha == 1:
        print('[bold]Rubert:[/bold] Na medida do possível sim.')
    elif escolha == 2:
        print('[bold]Rubert:[/bold] Como sempre, priorizando a eficiência...')
    else:
        print('[bold]Rubert:[/bold] Você sabe que ser assim não te deixa mais maneiro, né?\nIsso parece fala de protagonista de filmes ou jogos de policiais, é vergonhoso.')

    print('(Ele apaga o cigarro depois de ter dado uma tragada)')
    esperar_tecla('Digite qualquer tecla para continuar')
    print('[bold blue]-' *20 )

    print('[bold]Rubert:[/bold] Bom, os outros estão procurando o suspeito pelas redondezas.')
    print('(Ele tira do bolso uma chave)')
    print('[bold]Rubert:[/bold] Eu tentei dar uma vasculhada no lugar, mas sendo sincero não consigo ficar muito tempo nessa casa.')
    print('(Ele joga a chave na sua direção e você pega)')
    esperar_tecla('Digite qualquer tecla para continuar')
    print('[bold]Rubert:[/bold] Não sei para você, mas eu me sinto estranho quando participo de investigações assim.\nTalvez eu tenha um estômago fraco.')
    print('(Ele começa a se afastar e vai embora)')
    esperar_tecla('Digite qualquer tecla para continuar')

def iniciar_investigacao(ato):
    investigacao = 0
    pistas_importantes_encontradas = 0
    itens_do_ato = itens_investigacao[ato]

    limite = 2 if ato in ["ato2", "ato3"] else 5

    while investigacao < limite:
        print(f'\n--- Progresso da Investigação: {investigacao}/{limite} itens vistos ---')
        print('Onde você deseja olhar agora?')

        for id_item, info in itens_do_ato.items():
            if not info["visto"]:
                print(f"{id_item} - Analisar {info['nome']}")
            else:
                print(f"[{id_item} - {info['nome']} (Já investigado)]")

        try:
            escolha_item = int(input('\nR: '))

            if escolha_item in itens_do_ato:
                if not itens_do_ato[escolha_item]["visto"]:
                    itens_do_ato[escolha_item]["visto"] = True
                    investigacao += 1

                    print("\n", "[bold red]="*40)
                    print(f"🔎 {itens_do_ato[escolha_item]['nome'].upper()}:")
                    print(itens_do_ato[escolha_item]["lore"])
                    print("[bold red]="*40)

                    if itens_do_ato[escolha_item]["importante"]:
                        pistas_importantes_encontradas += 1

                    esperar_tecla('[Aperte Qualquer Tecla Para Continuar]')
                else:
                    print('\n[bold][!] Você já revirou esse lugar. Escolha outro ponto de interesse!')
            else:
                print('\n[bold][!] Esse ponto não parece relevante. Escolha um número da lista.')

        except ValueError:
            print('\n[bold][!] Digite apenas o número correspondente ao item.')
            
    return pistas_importantes_encontradas

def combate(dados_monstro):
    nome_player = personagem["nome"]
    pistola = personagem["habilidades"]["pistola"]
    cassetete = personagem["habilidades"]["cassetete"]
    
    # Flag local para garantir que a transformação do Marido só aconteça UMA vez
    furia_ativada = False 
    
    print(f"\n💥 O combate contra [bold red]{dados_monstro['nome'].upper()}[/bold red] começou!")
    
    while personagem["hp_atual"] > 0 and dados_monstro["hp_atual"] > 0: 
        print("\n" + "="*40)
        exibir_barra_hp(nome_player, personagem["hp_atual"], personagem["hp_max"])
        exibir_barra_hp(dados_monstro["nome"], dados_monstro["hp_atual"], dados_monstro["hp_max"])
        print(f"Munição da Pistola: [bold]{pistola['mun_atual']}/{pistola['mun_max']}")
        print("="*40)
        
        print("[bold]Comandos: [a] ATACAR | [d] DEFENDER | [f] FUGIR")
        comando = input("⬆️ Digite um dos comandos acima: ").strip().lower()
        
        if comando in ["a", "atacar", "ataca"]:
            acao = "a"
        elif comando in ["d", "defender", "defesa"]:
            acao = "d"
        elif comando in ["f", "fuga", "fugir"]:
            acao = "f"
        else:
            acao = "invalido"

        match acao:
            case "a":
                print(f"\n[bold]Opções: 'pistola' (Dano: {pistola['dano']}) | 'cassetete' (Dano: {cassetete['dano']})")
                escolha = input("Escolha sua habilidade: ").strip().lower()
                
                dano_causado = 0
                ataque_valido = False
                
                if escolha == "pistola" or escolha == "p":
                    if pistola["mun_atual"] > 0:
                        pistola["mun_atual"] -= 1 
                        dano_causado = pistola["dano"]
                        ataque_valido = True
                        print("\n💥[bold][red] BANG![/red] Você disparou contra o espírito!")
                        print("[bold][yellow]Dano Causado[yellow] [red]30[red]")
                        if dados_monstro.get("fraqueza") == "perfurante":
                            dano_causado *= 2
                            print("🔥[bold red] CRÍTICO! O dano perfurante perfura a névoa!")
                            print("[bold][yellow]Dano Causado[yellow] [red]60[red]")
                    else:
                        print("\n⚠️ [bold] [red]CLIQUE![/red][yellow] A pistola está sem munição!")       
                if escolha == "cassetete" or escolha == "c":
                    dano_causado = cassetete["dano"]
                    ataque_valido = True
                    print("\n🏏[bold][red] TROW![/red] Você desferiu um golpe físico.")
                    print("[bold][yellow]Dano Causado[yellow] [red]15[red]")

                    if dados_monstro.get("fraqueza") == "contudente":
                        dano_causado *= 2
                        print("🔥 [bold red]CRÍTICO! O impacto esmaga a barreira ectoplásmica!")
                        print("[bold][yellow]Dano Causado[yellow] [red]30[red]")
                else:
                    print("\n[bold][!] Comando inválido! Você atacou o vento.")
                
                if ataque_valido:
                    dados_monstro["hp_atual"] -= dano_causado
                
                if dados_monstro["hp_atual"] > 0:
                    qtd_habilidades = len(dados_monstro["habilidades"])
                    r = random.randint(1, qtd_habilidades)
                    ataque_inimigo = dados_monstro["habilidades"][r]
                    personagem["hp_atual"] -= ataque_inimigo["dano"]
                    print(f"👻 [bold]{dados_monstro['nome']}[/bold] contra-atacou com [bold italic red][{ataque_inimigo['ataque']}][/bold italic red] causando [bold]{ataque_inimigo['dano']}[/bold] de dano!")

            case "d":
                qtd_habilidades = len(dados_monstro["habilidades"])
                r = random.randint(1, qtd_habilidades)
                ataque_inimigo = dados_monstro["habilidades"][r]
                dano_reduzido = int(ataque_inimigo["dano"] * 0.5)
                personagem["hp_atual"] -= dano_reduzido
                
                print(f"\n🛡️[bold blue] Você se protegeu! O inimigo usou [{ataque_inimigo['ataque']}].")
                print(f"\n[bold] blueEm vez de {ataque_inimigo['dano']}, você sofreu apenas {dano_reduzido} de dano.")

            case "f":
                qtd_habilidades = len(dados_monstro["habilidades"])
                r = random.randint(1, qtd_habilidades)
                ataque_inimigo = dados_monstro["habilidades"][r]
                personagem["hp_atual"] -= ataque_inimigo["dano"]
                print(f"\n🏃‍♂️[bold] Você falhou ao fugir! As portas estão seladas!")
                print(f"👻[bold] O espírito te atingiu pelas costas com [italic red][{ataque_inimigo['ataque']}][/italic red] causando {ataque_inimigo['dano']} de dano.")
            
            case _:
                print("\n[!] Você hesitou e perdeu o turno!")

        # --- SISTEMA DE FÚRIA E CURA DO MARIDO (BOSS COMPORTAMENTO) ---
        if dados_monstro["id"] == 3 and dados_monstro["hp_atual"] <= dados_monstro["hp_max"] * 0.5 and dados_monstro["hp_atual"] > 0 and not furia_ativada:
            furia_ativada = True
            
            # Recupera exatamente 1/3 da vida máxima (50 de HP)
            recuperacao = int(dados_monstro["hp_max"] / 3) 
            dados_monstro["hp_atual"] += recuperacao
            
            print("\n" + "☠️" * 25 + "\n")
            print("🚨[bold red] O RANCOR SUPERA A MORTE! O MARIDO ENTRA EM FÚRIA PROFANA!")
            print("[bold red]O veneno de rato ferve em sua essência espiritual e o ritual fracassado se manifesta.")
            print(f"[bold red]O demônio ruge de pura agonia e ódio, recuperando {recuperacao} de HP!")
            print("💥 [bold red]SEUS ATAQUES SE TORNARAM COMPLETAMENTE LETAIS!")
            print("\n"+"☠️" * 25)
            
                        # Ajuste dentro do IF da fúria do ID 3 na função combate:
            dados_monstro["habilidades"] = {
                1: {"ataque": "Erupção de Veneno Macabro", "dano": 20}, 
                2: {"ataque": "Dilaceração Tóxica", "dano": 26}         
            }


    if personagem["hp_atual"] <= 0:
        print("\n💀[bold red] FIM DE JOGO.[/bold red] A escuridão te consumiu...")
        return False
    else:
        print(f"\n✨[bold blue] Você derrotou {dados_monstro['nome']}!")
        if dados_monstro["drop"]:
            item_dropado = dados_monstro["drop"]
            personagem["inventario"].append(item_dropado)
            print(f"🔑[bold] [DROP DE ITEM] O espírito se desfez e deixou cair: {item_dropado.upper()}!")
            print(f"[bold]Inventário Atual:[/bold] {personagem['inventario']}")
        return True

def manifestacao_sobrenatural(pistas, ato):

    # Define o total de pistas possíveis baseado no ato
    total_pistas = 2 if ato in ["ato2", "ato3"] else 5

    print("\n🔮[bold] [SINTONIA SOBRENATURAL]")
    print("Ao desvendar os segredos do ambiente, uma energia gélida ecoa pela sala...")

    # CASO 1: Investigação Perfeita (100% das pistas importantes encontradas)
    if pistas == total_pistas:
        print("\n👁️ [bold]LAMPEJO DE LUCIDEZ:[/bold] Sua mente se conecta perfeitamente ao passado!")
        print("Uma névoa densa espanta o cansaço do seu corpo e materializa o impossível:")
        print("[bold]-> [RESTAURAÇÃO]:[/bold] Seu HP foi completamente regenerado pelo vigor espiritual!")
        print("[bold]-> [MATERIALIZAÇÃO]:[/bold] Duas balas de éter surgem no tambor da sua pistola! (+2 Munição)")

        personagem["hp_atual"] = personagem["hp_max"]
        personagem["habilidades"]["pistola"]["mun_atual"] = min(
            personagem["habilidades"]["pistola"]["mun_atual"] + 2, 
            personagem["habilidades"]["pistola"]["mun_max"]
        )

    # CASO 2: Investigação Parcial (Achou pelo menos metade das pistas importantes)
    elif pistas >= (total_pistas / 2):
        print("\n👻 ECO DOS MORTOS: O ambiente sussurra fragmentos da verdade.")
        print("A compreensão parcial dos fatos estabiliza sua sanidade e fecha suas feridas leves.")
        print("-> [CONFORTO MÓRBIDO]: Você absorve a energia do local, recuperando 30 de HP.")

        personagem["hp_atual"] = min(personagem["hp_atual"] + 30, personagem["hp_max"])

    # CASO 3: Investigação Ruim (Ignorou as pistas)
    else:
        print("\n🖤 O HORROR TE SUFOCA: Você ignorou os detalhes cruciais do ambiente...")
        print("A ignorância deixa sua mente exposta ao medo. O ar parece mais pesado e hostil.")
        print("-> [SUSSURROS ANGOSTIANTES]: Nada acontece. Um calafrio corta sua espinha.")

    print()
    esperar_tecla('[Aperte Qualquer Tecla para encarar o espitito]')

# ==========================================
# FLUXO PRINCIPAL DO PROGRAMA
# ==========================================


print('[bold red ]SINS\n')
musica = play('musica-menu.wav', async_mode=True, loop=True)
print('[bold]Menu\n1 - Começar Jogo \n[/bold]2 - dlc[bold] \n3 - Sair')

try:
    menu = int(input('Digite o número da sua escolha\nR: '))
    sleep(2)
    stop(musica)
except ValueError:
    menu = 3

if menu == 1:
   
    mostrar_cutscene_inicial(personagem["nome"])

    while True:
        print('\n----')
        print('Você olha para a casa. Ela é uma casa comum de dois andares,\nvocê consegue ver algumas luzes acesas pela janela.')
        print('A cada segundo que você passa olhando essa casa, mais estranha ela parece,')
        print('como se um ar de decadência e morte estivesse presente nela.')
        print(f'\nOpções de escolha:\n1 - Estou pensando demais, vamos terminar logo isso...\n2 - Isso não vai dar bom... (Desistir)')

        try:
            escolha = int(input(f'R: '))
        except ValueError:
            escolha = 1

        if escolha == 1:
            print('\nVocê pega a chave da casa e entra.')
            print('Você passa pelos corredores até que chega na sala de estar.')
            print('Logo é possível perceber uma taça de vinho e suas taças em uma mesinha,')
            print('mas o que mais chama atenção é a demarcação de um cadáver no chão e sangue.')
            print('"Lá vamos nós..."')
        elif escolha == 2:
            break;

        # ---         # --- EXECUÇÃO DO ATO 1 ---
        pistas_ato1 = iniciar_investigacao("ato1")
        manifestacao_sobrenatural(pistas_ato1, "ato1")
        
        vitoria_ato1 = combate(bestiario[1])
        if not vitoria_ato1: 
            break
            
        # --- TRANSIÇÃO E EXECUÇÃO DO ATO 2 ---
        print('\n' + '='*50)
        print('   ATO 2: O CORREDOR DAS SOMBRAS')
        print('='*50)
        print('O ar gela instantaneamente. Marcas de arrasto levam à porta do porão.')
        print('O espírito furioso do Amante bloqueia o seu caminho!')
        print()
        esperar_tecla('[Pressione Qualquer tecla para investigar o corredor...]')
        
        pistas_ato2 = iniciar_investigacao("ato2")
        manifestacao_sobrenatural(pistas_ato2, "ato2")
        
        vitoria_ato2 = combate(bestiario[2])
        if not vitoria_ato2: 
            break
            
        # --- TRANSIÇÃO E EXECUÇÃO DO ATO 3 ---
        print('\n' + '='*50)
        print('   ATO 3: O RITUAL DA AGONIA (PORÃO)')
        print('='*50)
        
        if "Chave do Porão" in personagem["inventario"]:
            print("[!] As correntes caem. Cheiro de podridão e veneno invade o ambiente.")
            print("O Marido está ao fundo, transformado pelo puro rancor.")
            print()
            esperar_tecla('[Pressione Qualquer tecla para buscar pistas no porão...]')
        else:
            print("\nA porta está trancada e você não tem a chave. Fim de linha.")
            break
        
        pistas_ato3 = iniciar_investigacao("ato3")
        manifestacao_sobrenatural(pistas_ato3, "ato3")
        
        vitoria_final = combate(bestiario[3])
        
        if vitoria_final:
            print('\n' + '='*50)
            print('🎉 CASO ENCERRADO! PARABÉNS!')
            print('='*50)
            print('O Marido foi derrotado.')
            print('JT caminha para fora da casa enquanto o sol nasce. O terror acabou.')
        
        break


elif menu == 2:
    print('\nAinda em desenvolvimento (o desenvolvedor narigudo não veio).')
elif menu == 3:
    print('\nPorque tu entrou no meu jogo se tu ia sair?\nAinda sim, muito obrigado por ter perdido o seu tempo :)')