import os
import json
import os.path
import asyncio
import configparser
from pathlib import Path
from twitchio.ext import commands
from random import randint, choice

# Recupera os comandos criados através do '!comando add'
with open("arquivos/commands.json", 'r', encoding='UTF-8') as file:
    try:
        namecommand = json.load(file)
    finally:
        print(f'Comandos recuperados: {namecommand}')

# Pega os dados necessários no arquivo 'config.ini'
config = configparser.ConfigParser()
config.read('config.ini')

timeroll = False
timespin = False
players = []
duel = False
var_oi = ["oi"]
spam_comp = []

# Emotions game SPIN
spin = ['EarthDay', 'PurpleStar', 'PraiseIt',
        'duDudu', 'ItsBoshyTime', "PorscheWIN"]

# Agua
agua = 'Bora beber água galera DrinkPurple '
water = "Let's go everyone drink water DrinkPurple "

# Váriavel para fazer as interações e conectar com os canaais
bot = commands.Bot(
    irc_token=config.get('bot', 'oauth'),
    api_token=config.get('bot', 'client_id'),
    nick=config.get('bot', 'nick_bot'),
    prefix=config.get('bot', 'prefix'),
    initial_channels=[config.get('bot', 'channel')]
)


# essa função roda quando o bot inicia
@bot.event
async def event_ready():
    ws = bot._ws
    print(bot.initial_channels[0], f"Let's go, @{bot.nick} is online now.")

    # nicksbans = []

    # for i in nicksbans:
    #     await ws.send_privmsg(bot.initial_channels[0], f'/ban {i}')

    await ws.send_privmsg(bot.initial_channels[0], f'/me Soluções LTDA - chegou!!!')
    while True:
        await ws.send_privmsg(bot.initial_channels[0], f'/me {agua}. {water}.')
        await asyncio.sleep(1800)


# Evento que lê toda mensagem enviada no chat
@bot.event
async def event_message(ctx):
    if ctx.author.name == bot.nick:
        return

    if ctx.author.name not in spam_comp:
        if 'bom dia' in ctx.content.lower():
            await ctx.channel.send(f"Bom dia @{ctx.author.name}. Bem vindo a minha live. KonCha ")

        elif 'boa tarde' in ctx.content.lower():
            await ctx.channel.send(f"Boa tarde @{ctx.author.name}. Bem vindo a minha live. KonCha ")

        elif 'boa noite' in ctx.content.lower():
            await ctx.channel.send(f"Boa noite @{ctx.author.name}. Bem vindo a minha live. KonCha ")

        elif 'good morning' in ctx.content.lower():
            await ctx.channel.send(f'Good morning @{ctx.author.name}. Welcome to my stream. KonCha ')

        elif 'good afternoon' in ctx.content.lower():
            await ctx.channel.send(f'Good afternoon @{ctx.author.name}. Welcome to my stream. KonCha ')

        elif 'good evening' in ctx.content.lower():
            await ctx.channel.send(f'Good evening @{ctx.author.name}. Welcome to my stream. KonCha ')

        elif 'good night' in ctx.content.lower():
            await ctx.channel.send(f'Good night @{ctx.author.name}. Welcome to my stream. KonCha ')

        elif 'salve' in ctx.content.lower():
            await ctx.channel.send(f"/me Opaaaa!!! Tal salvado @{ctx.author.name} SeemsGood ")

        else:
            await ctx.channel.send(f"Olá pra ti {ctx.author.name} KonCha")

        spam_comp.append(ctx.author.name)     

    # Este if é para retornar a msg do comando chamado
    # "Apenas dos comandos criados no '!comando add'
    if "!" == ctx.content.split()[0][0]: # Se tiver '!' no inicio da msg
        comando = ctx.content.split()[0] #pega o comando digitado
        
        # Passa por toda a lista de comando
        for command, message in namecommand.items():
            # Se o comando digitado for igual o da lista
            if comando.replace("!", "") == command:
                name = command
                msg = message
                print(f"Comando chamado:'{name}' -> '{msg}'")
                await ctx.channel.send(f'{msg}')

    await bot.handle_commands(ctx)


# Essa função serve para tratar quase todos os erros durante a execução
# Caso remova essa função, o bot crashara por qualquer erro
@bot.event
async def event_command_error(ctx, error):
    print(error)
    pass


# Comando de game. Rola um valor entre 0 e 100, se for maior que X ele ganha
@bot.command(name='roll')
async def fn_roll(ctx):
    global timeroll

    if not timeroll:
        timeroll = True
        dado = randint(0, 100)
        magic = randint(0, 100)
        print(dado, magic, ctx.author.name)

        if dado == magic:
            await ctx.channel.send(f"Mano, você tirou o número mágico, vai se limpar que ta precisando '-'")
            await ctx.channel.send(f"!addpoints {ctx.author.name} 500")

        if dado >= 85:
            msg = f"Você tirou {dado} no dado. Parabéns @{ctx.author.name}, você ganhou VisLaud "
            await ctx.channel.send(f"{msg}")
            await ctx.channel.send(f"!addpoints {ctx.author.name} 50")
        else:
            msg = f"Você tirou {dado} no dado. Parabéns @{ctx.author.name}, você perdeu TearGlove "
            await ctx.channel.send(f"{msg}")

        await asyncio.sleep(10)
        timeroll = False


# Sorteia 3 emotes, caso forem iguais a pessoa ganha
@bot.command(name='spin')
async def fn_spin(ctx):
    global timespin

    if not timespin:
        timespin = True
        
        sort = [randint(0, 5) for i in range(0, 3)]
        if sort[0] == sort[1] == sort[2]:
            msg = f". Parabéns sua sorte está em pleno dia, você ganhou @{ctx.author.name} CoolCat "
            res = f"{spin[sort[0]]} {spin[sort[1]]} {spin[sort[2]]} {msg}"
            await ctx.channel.send(res)
            await ctx.channel.send(f"!addpoints {ctx.author.name} 500")

        else:
            msg = f". Parabéns sua sorte está em grande falta, você perdeu @{ctx.author.name} LUL "
            res = f'{spin[sort[0]]} {spin[sort[1]]} {spin[sort[2]]} {msg}'
            await ctx.channel.send(res)

        await asyncio.sleep(10)
        timespin = False


# Cria um duelo com outro player
@bot.command(name='duel')
async def fn_duel(ctx):
   global players, duel

   # Verifica se tem algum duelo rolando
   if len(players) == 0:
       players = [ctx.author.name, ctx.content.split(
           "@" if "@" in ctx.content else None)[1].lower()]
       if players[0] == players[1]:
           await ctx.channel.send("Você não pode duelar com você mesmo :)")
       else:
           msg = f"Olocoo VisLaud {players[0]} chamou {players[1]} para um duelo. Eae, eu não deixava heim Kappa "
           msg1 = "30 segundos para aceitar !accept ou para recusar !decline"
           await ctx.channel.send(f"{msg} {msg1}")
           await asyncio.sleep(30)
       if not duel:
           players.clear()
       duel = False
       print("Duelo clear")
   else:
       await ctx.content.send("Tem um duelo na fila.")


# Para aceitar um duelo 
@bot.command(name='accept')
async def fn_accept(ctx):
    global duel

    try:
        # Verifica se a pessoa é a mesma da que foi chamada pro duelo
        if ctx.author.name.lower() == players[1]:
            fight = [randint(0, 100), randint(0, 100)]
            if fight[0] > fight[1]:
                msg = f"@{players[0]} tirou {fight[0]} enquanto @{players[1]} tirou {fight[1]}. Chamou e ganhou VisLaud "
            elif fight[0] < fight[1]:
                msg = f"@{players[0]} tirou {fight[0]} enquanto @{players[1]} tirou {fight[1]}. Chamou e perdeu LUL "
            else:
                msg = f"@{players[0]} tirou {fight[0]} enquanto @{players[1]} tirou {fight[1]}. Ninguem ganhou Kappa "

            await ctx.channel.send(msg)
            players.clear()
            print("Duelo clear")
            duel = True
        else:
            # Caso não for a mesma pessoa, ele levanta um erro
            raise NameError
    except IndexError:
        await ctx.channel.send("Não foi encontrado um duelo.")
    except NameError:
        await ctx.channel.send("Não foi encontrado um duelo.")


# Para recusar um duelo criado
@bot.command(name='decline')
async def fn_decline(ctx):
    global duel
    try:
        # Verifica se a pessoa é a mesma da que foi chamada pro duelo
        if ctx.author.name.lower() == players[1]:
            msg = f"Ihhhh. @{players[1]} arregou e recusou o duelo LUL "
            await ctx.content.send(msg)

            duel = True
            players.clear()
            print("Duelo clear")
        else:
            # Caso não for a mesma pessoa, ele levanta um erro
            raise NameError
    except NameError:
        await ctx.channel.send("Não foi encontrado um duelo.")


# Criar comando cia chat
@bot.command(name='comando')
async def add_command(ctx):
    # Retornar caso não for mod
    if not ctx.author.is_mod:
        return

    global namecommand

    # Atualizar os comandos no arquivo
    def save_file(save=dict):
        with open("arquivos/commands.json", 'w+', encoding='utf-8') as file:
            comandos = json.dumps(save, indent=True, ensure_ascii=False)
            file.write(comandos)
            print("comando salvo")

    comando = ctx.content.split()[2]
    msg = " ".join(ctx.content.split()[3:])

    # Para adicionar o comando
    if ctx.content.split()[1] == 'add':
        namecommand[comando] = msg
        print(f"Comando {comando} adicionado por {ctx.author.name}. Lista de comando adicionados {namecommand}")
        save_file(namecommand)
        mensagem = f"Comando '{comando}' com a mensagem '{msg}' foi adicionada com sucesso."

    # Editar um comando existente
    elif ctx.content.split()[1] == 'edit':
        for command, message in namecommand.items():
            if command == comando:
                namecommand[command] = msg
                print(f"A mensagem do comando '{comando}' foi alterado para '{message}'")  
                save_file(namecommand)
                mensagem = f"A mensagem do comando '{comando}' foi alterado para '{msg}' com sucesso."

    # Para remover um comando existente
    elif ctx.content.split()[1] == 'del':
        namecommand.pop(comando)
        save_file(namecommand)
        mensagem = f"O comando '{comando}' foi deletado com sucesso."
    
    await ctx.channel.send(mensagem)


# QUE TA CONTECENO NA LIVE MEU DEUS
@bot.command(name='wtf')
async def command_wtf(ctx):
    await ctx.channel.send("/me QUE Q TA ACONTECENO....")
    await ctx.channel.send("/me W")
    await ctx.channel.send("/me T")
    await ctx.channel.send("/me F")


# Rinha de ban
@bot.command(name='ban')
async def command_ban(ctx):
    pessoa = [ctx.author.name, ctx.content.split(
            "@" if "@" in ctx.content else None)[1]]
    
    if pessoa[0] == pessoa[1]:
        return
        
    print(pessoa[0], pessoa[1])
    await ctx.channel.send(f"@{pessoa[0]} mandou @{pessoa[1]} para BanHamas Kappa ")


# Sorteia uma capital (Mentira, vai sortear uma estado)
@bot.command(name='capital')
async def command_estado(ctx):
    estado = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal','Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul','Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro','Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima','Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins']

    await ctx.channel.send(f'A capital do momento é {choice(estado)}')


# Sorteia uma estado (Mentira, vai sortear uma capital)
@bot.command(name='estado')
async def command_capital(ctx):
    capital = ['Rio Branco', 'Maceió', 'Macapá', 'Manaus', 'Salvador', 'Fortaleza', 'Brasília', 'Vitória', 'Goiânia', 'São Luís', 'Cuiabá', 'Campo Grande', 'Belo Horizonte', 'Belém', 'João Pessoa', 'Curitiba', 'Recife', 'Teresina', 'Rio de Janeiro', 'Natal', 'Porto Alegre', 'Porto Velho', 'Boa Vista', 'Florianópolis', 'São Paulo', 'Aracaju', 'Palmas']

    await ctx.channel.send(f'O estado do momento é {choice(capital)}')


# Sorteia um lugar para ir visitar
@bot.command(name='viagem')
async def command_viagem(ctx):
    capital = ['Rio Branco', 'Maceió', 'Macapá', 'Manaus', 'Salvador', 'Fortaleza', 'Brasília', 'Vitória', 'Goiânia', 'São Luís', 'Cuiabá', 'Campo Grande', 'Belo Horizonte', 'Belém', 'João Pessoa', 'Curitiba', 'Recife', 'Teresina', 'Rio de Janeiro', 'Natal', 'Porto Alegre', 'Porto Velho', 'Boa Vista', 'Florianópolis', 'São Paulo', 'Aracaju', 'Palmas']

    estado = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal','Espírito Santo', 'Goiás', 'Maranhão', 'Mato Grosso', 'Mato Grosso do Sul','Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro','Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima','Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins']

    await ctx.channel.send(f'Quel tal ir visitar a cidade {choice(estado)} do estado {choice(capital)}. É um ótimo lugar, recomendo ;) ')


# Nivel de amizade com a pessoa
@bot.command(name='amizade')
async def command_amizade(ctx):
    friend = ctx.content.split(
            "@" if "@" in ctx.content else None)[1]
    
    await ctx.channel.send(f'/me @{ctx.author.name} sua amizade com @{friend} é de {randint(0, 100)}%. PogChamp')


# Só para testar umas aleatoridades
@bot.command(name='teste')
async def command_test(ctx):
    if 'broadcaster' not in ctx.author.badges:
        print('oi')
        return


# Para rodar o bot
if __name__ == '__main__':
    bot.run()
