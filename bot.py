import asyncio
from random import randint
from twitchio.ext import commands

# Dados do canal do bot
oauth_key = 'oauth:'
client_key = 'KEY'

# Command Countdown
timeroll = False
timespin = False
duel = False

players = []

# Emotions game SPIN
spin = ['EarthDay', 'PurpleStar', 'PraiseIt',
        'duDudu', 'ItsBoshyTime', "PorscheWIN"]

# Agua
agua = 'Bora beber água galera DrinkPurple '
water = "Let's go everyone frink water DrinkPurple "

# Váriavel para fazer as interações e conectar com os canaais
bot = commands.Bot(
    irc_token=oauth_key,
    api_token=client_key,
    nick='nickbot',
    prefix='!',
    initial_channels=['channel']
)


@bot.event
async def event_ready():
    ws = bot._ws
    print(bot.initial_channels[0], f"Let's go, @{bot.nick} is online now.")

    await ws.send_privmsg(bot.initial_channels[0], f'Bot ta on :)')
    while True:
        await ws.send_privmsg(bot.initial_channels[0], f'/me {agua}. {water}.')
        await asyncio.sleep(1800)


@bot.event
async def event_message(ctx):
    if ctx.author.name == bot.nick:
        return

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

    await bot.handle_commands(ctx)


# Error handling
@bot.event
async def event_command_error(ctx, error):
    pass


# Roll Game
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

        if dado >= 60:
            msg = f"Você tirou {dado} no dado. Parabéns @{ctx.author.name}, você ganhou PogChamp "
            await ctx.channel.send(f"{msg}")
            await ctx.channel.send(f"!addpoints {ctx.author.name} 50")
        else:
            msg = f"Você tirou {dado} no dado. Parabéns @{ctx.author.name}, você perdeu TearGlove "
            await ctx.channel.send(f"{msg}")

        await asyncio.sleep(30)
        timeroll = False


@ bot.command(name='spin')
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

        await asyncio.sleep(30)
        timespin = False


@ bot.command(name='duel')
async def fn_duel(ctx):
    global players, duel

    # Verifica se tem algum duelo rolando
    if len(players) == 0:
        players = [ctx.author.name, ctx.content.split(
            "@" if "@" in ctx.content else None)[1].lower()]
        if players[0] == players[1]:
            await ctx.channel.send("Você não pode duelar com você mesmo :)")
        else:
            msg = f"Olocoo PogChamp {players[0]} chamou o {players[1]} para um duelo. Eae, eu não deixava heim Kappa "
            msg1 = "30 segundos para aceitar !accept ou para recusar !decline"
            await ctx.channel.send(f"{msg} {msg1}")
            await asyncio.sleep(30)
        if not duel:
            players.clear()
        duel = False
        print("Duelo clear")
    else:
        await ctx.content.send("Tem um duelo na fila.")


# Duel accept
@ bot.command(name='accept')
async def fn_accept(ctx):
    global duel

    try:
        if ctx.author.name.lower() == players[1]:
            fight = [randint(0, 100), randint(0, 100)]
            if fight[0] > fight[1]:
                msg = f"@{players[0]} tirou {fight[0]} e o @{players[1]} tirou {fight[1]}. Chamou e ganhou PogChamp "
            elif fight[0] < fight[1]:
                msg = f"@{players[0]} tirou {fight[0]} e o @{players[1]} tirou {fight[1]}. Chamou e perdeu LUL "
            else:
                msg = f"@{players[0]} tirou {fight[0]} e o @{players[1]} tirou {fight[1]}. Ninguem ganhou Kappa "

            await ctx.channel.send(msg)
            players.clear()
            print("Duelo clear")
            duel = True
        else:
            raise NameError
    except IndexError:
        await ctx.channel.send("Não foi encontrado um duelo.")
    except NameError:
        await ctx.channel.send("Não foi encontrado um duelo.")


# Duel decline
@ bot.command(name='decline')
async def fn_decline(ctx):
    global duel
    try:
        if ctx.author.name.lower() == players[1]:
            msg = f"Ihhhh. @{players[1]} arregou e recusou o duelo LUL "
            await ctx.content.send(msg)

            duel = True
            players.clear()
            print("Duelo clear")
        else:
            raise NameError
    except NameError:
        await ctx.channel.send("Não foi encontrado um duelo.")


if __name__ == '__main__':
    bot.run()
