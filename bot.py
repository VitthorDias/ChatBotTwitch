import asyncio
from random import randint
from twitchio.ext import commands

# Dados do canal do bot
oauth_key = 'oauth:'
client_key = 'KEY'

# Lista para ser usado no game do !duelo (Deixe vazio senão o game não funcionará)
player = []

# Mensagens para lembrar de tomar água
agua = "Bora todo mundo beber água DrinkPurple "
water = "Let's go everyone drink water DrinkPurple "

# Emotions do game SPIN
spin = ['EarthDay', 'PurpleStar', 'PraiseIt',
        'duDudu', 'ItsBoshyTime', "PorscheWIN"]

# Váriavel para fazer as interações e conectar com os canaais
bot = commands.Bot(
    irc_token=oauth_key,
    api_token=client_key,
    nick=bot_nick,
    prefix='!',
    initial_channels=[channels]
)


# Register an event with the bot
@bot.event
async def event_ready():
    ws = bot._ws
    print(bot.initial_channels[0], f"Let's go, @{bot.nick} is online now.")

    while True:
        await ws.send_privmsg(bot.initial_channels[0], f"{agua}")
        await ws.send_privmsg(bot.initial_channels[0], f"{water}")
        await asyncio.sleep(1800)


# Recebe uma mensagem e responde que o chamou
@bot.event
async def event_message(ctx):
    # Só algumas apresentações
    if 'bom dia' in ctx.content.lower():
        await ctx.channel.send(f"Bom dia @{ctx.author.name}. Bem vindo a minha live.")

    elif 'boa tarde' in ctx.content.lower():
        await ctx.channel.send(f"Boa tarde @{ctx.author.name}. Bem vindo a minha live.")

    elif 'boa noite' in ctx.content.lower():
        await ctx.channel.send(f"Boa noite @{ctx.author.name}. Bem vindo a minha live.")

    elif 'good morning' in ctx.content.lower():
        await ctx.channel.send(f'Good morning @{ctx.author.name}. Welcome to my stream.')

    elif 'good afternoon' in ctx.content.lower():
        await ctx.channel.send(f'Good afternoon @{ctx.author.name}. Welcome to my stream.')

    elif 'good evening' in ctx.content.lower():
        await ctx.channel.send(f'Good evening @{ctx.author.name}. Welcome to my stream.')

    elif 'good night' in ctx.content.lower():
        await ctx.channel.send(f'Good night @{ctx.author.name}. Welcome to my stream.')

    await bot.handle_commands(ctx)


# Sorteia um número entre 0 e 6 como se fosse um dado
@bot.command(name='roll')
async def fn_roll(ctx):
    dado = randint(0, 6)  # Sorteia um número do dado

    if dado >= 3:  # Caso ele ganhe
        msg = f"PogChamp Você ganhou @{ctx.author.name}!!! Você tirou {dado} no dado. PogChamp "
        await ctx.channel.send(msg)
    else:  # Caso ele perca
        msg = f"LUL Você perdeu @{ctx.author.name}!!! Você tirou {dado} no dado. LUL "
        await ctx.channel.send(msg)


# Jogo de azar SPIN
@bot.command(name='spin')
async def fn_spin(ctx):
    sort = [randint(0, 5) for i in range(3)]  # Sorteia 3 números (posições)

    #  Verifica se são iguais ou não
    if sort[0] == sort[1] == sort[2]:
        msg = f". A sua sorte está em dia, você ganhou @{ctx.author.name} CoolCat"
        # Seleciona os 3 emotions + mensagem
        ret = f"{spin[sort[0]]} {spin[sort[1]]} {spin[sort[2]]} {msg}"
    else:
        msg = f". A sua sorte está em falta, você perdeu @{ctx.author.name} TearGlove"
        # Seleciona os 3 emotions + mensagem
        ret = f"{spin[sort[0]]} {spin[sort[1]]} {spin[sort[2]]} {msg}"

    await ctx.channel.send(ret)


# Duelo part1 (chamando um segundo player para o duelo)
@bot.command(name='duel')
async def fn_duel(ctx):
    global player

    # Verifica se já possui um duelo ativo ou não
    if len(player) == 0:
        player = [ctx.author.name, ctx.content.split()[1]]  # Seleciona os dois players
        msg = f"""PogChamp Oloco @{player[0]} chamou o @{player[1]} pro fight,
        eu não deixa viu PogChamp"""

        msg1 = f"""@{player[1]} utilize !accept ou !decline para aceitar ou recusar.
        Você tem 60s!!!"""

        await ctx.channel.send(msg)
        await ctx.channel.send(msg1)

        await asyncio.sleep(60)  # Sleep para um tempo de duração do duelo
        player.clear()  # Esvaziar a lista de player para liberar outros rounds
    else:
        await ctx.channel.send(f"@{ctx.author.name} tem um duelo na fila, espere um pouco.")


# Duelo part2 (Caso o outro player aceite)
@bot.command(name='accept')
async def fn_accept(ctx):
    try:
        if ctx.author.name == player[1]:  # Verifica se o player tem um duelo pendente
            fight = [randint(0,10), randint(0,10)]

            if fight[0] > fight[1]:
                msg = f"""O @{player[0]} tirou {fight[0]} e o @{player[1]} tirou {fight[1]},
                chamou e honrou o nome Kappa"""

            elif fight[0] < fight[1]:
                msg = f"""O @{player[0]} tirou {fight[0]} e o @{player[1]} tirou {fight[1]},
                chamou e perdeu LUL"""

            else:
                msg = f"""O @{player[0]} tirou {fight[0]} e o @{player[1]} tirou {fight[1]},
                fizeram o semi-impossivel PogChamp"""

            await ctx.channel.send(msg)
        else:
            raise NameError  # Levantar uma excessão caso tende aceitar o proprio duelo
    except IndexError:  # Excessão para caso não tenha duelo
        await ctx.channel.send(f"@{ctx.author.name} você não tem duelo.")
    except NameError:
        await ctx.channel.send(f"@{ctx.author.name} ItsBoshyTime 404 Not found.")
        return

    player.clear()  # Esvaziar a lista de player para liberar outros rounds


# Duelo part2 (Caso o outro player recuse)
@bot.command(name='decline')
async def fn_accept(ctx):
    try:
        if ctx.author.name == player[1]:  # Verifica se o player tem um duelo pendente
            msg = f"O @{player[1]} ficou com medinho e recusou o duelo LUL"
            await ctx.channel.send(msg)
        else:
            raise NameError  # Levantar uma excessão caso tende recusar o proprio duelo
    except IndexError:  # Excessão para caso não tenha duelo
        await ctx.channel.send(f"@{ctx.author.name} você não tem duelo.")
    except NameError:
        await ctx.channel.send(f"@{ctx.author.name} ItsBoshyTime 404 Not found.")
        return

    player.clear()  # Esvaziar a lista de player para liberar outros rounds


if __name__ == '__main__':
    bot.run()
