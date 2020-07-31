import asyncio
from random import randint
from twitchio.ext import commands

# Dados do canal do bot
oauth_key = 'oauth:'
client_key = 'KEY'

# Mensagens para lembrar de tomar água
agua = "Bora todo mundo beber água DrinkPurple "
water = "Let's go everyone drink water DrinkPurple "

# Emotions do game SPIN
spin = ['EarthDay', 'PurpleStar', 'PraiseIt',
        'duDudu', 'ItsBoshyTime', "PorscheWIN"]

# Váriavel para fazer as interações e conectar com os canais
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
    await ws.send_privmsg(bot.initial_channels[0], f"Let's go, @{bot.nick} is online now.")

    while True:
        await ws.send_privmsg(bot.initial_channels[0], f"{agua}")
        await ws.send_privmsg(bot.initial_channels[0], f"{water}")
        await asyncio.sleep(1800)


# Recebe uma mensagem e responde quem o chamou
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
    from random import randint

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
        msg = ". A sua sorte está em dia, você ganhou CoolCat"
        # Seleciona os 3 emotions + mensagem
        ret = f"{spin[sort[0]]} {spin[sort[1]]} {spin[sort[2]]} {msg}"
    else:
        msg = ". A sua sorte está em falta, você perdeu TearGlove"
        # Seleciona os 3 emotions + mensagem
        ret = f"{spin[sort[0]]} {spin[sort[1]]} {spin[sort[2]]} {msg}"

    await ctx.channel.send(ret)


if __name__ == '__main__':
    bot.run()
