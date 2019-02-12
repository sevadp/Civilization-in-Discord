import discord
import asyncio
import requests
import streamelements
import config
import random
import time
import json

DISCORD_BOT_TOKEN = 'NDQyNTYxNTkzMjIyNDk2MjU4.D0H6Zw.H50D_hx6xKPg13Sb-Ch8kCRgle8'

BTC_PRICE_URL_coinmarketcap = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=RUB'

channel = "5abf2d6958a6665863b088c7"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNWFiZjJkNjk1OGE2NjZkOTk4YjA4OGM2IiwiY2hhbm5lbCI6IjVhYmYyZDY5NThhNjY2NTg2M2IwODhjNyIsInByb3ZpZGVyIjoidHdpdGNoIiwicm9sZSI6Im93bmVyIiwiYXV0aFRva2VuIjoiVENjblc5SWF4MWJKZG1RMkdDVkJmUFVIODdiQ1dWNzAwUkxET29SZF9DcjFBajdjIiwiaWF0IjoxNTQxNzc0MjM1LCJpc3MiOiJTdHJlYW1FbGVtZW50cyJ9.JaWB3MC8bNX11LuX9zjukcNRV8pyRhje2wcCvUoDzDc"
duel = []
global start
start = 0

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    global start
    start = 0
    print('------')


@client.event
async def on_message(message):
    global start
    if start == 0:
        with open('data.json', 'r') as fp:
            config.users = json.load(fp)
        start = 1
    if message.content.startswith('!smorc') and str(message.author) in config.users:
        print('[command]: smorc ')
        await client.send_message(message.channel, "1) !listusers - список участников SMORCWORLD")
        time.sleep(0.25)
        await client.send_message(message.channel, "2) !register [twitch name] - Регистрация SMORCWORLD")
        time.sleep(0.25)
        await client.send_message(message.channel, "3) !checkduel - Участники, находящиеся в очереди на дуэль!")
        time.sleep(0.25)
        await client.send_message(message.channel, "4) !duel - Регистрация на дуэль!")
        time.sleep(0.25)
        await client.send_message(message.channel, "5) !cancel - Отменить регистрацию на дуэль!")
    elif message.content.startswith('!smorc'):
        await client.send_message(message.channel, "Пожалуйста, пройдите регистрацию. !register [twitch name]")

    if message.content.startswith('!listusers') and str(message.author) in config.users:
        print('[command]: listusers ')
        await client.send_message(message.channel, config.users)
    elif message.content.startswith('!listusers'):
        await client.send_message(message.channel, "Пожалуйста, пройдите регистрацию. !register [twitch name]")

    if message.content.startswith('!register'):
        print("[command]: register")
        a = message.content
        if len(a.split()) != 2:
            await client.send_message(message.channel, "Ввод нарушен! Не 2 элемента ввода.")
        else:
            name = a.split()[1]
            test = 0
            for i in config.users.values():
                if i == name:
                    test = 1
                    break
            if test == 0:
                id_discord = str(message.author)
                config.add_user(id_discord, name)
                config.save_users()
                await client.send_message(message.channel, "Успешная регистрация!")
            else:
                find = 0
                for k in config.users.keys():
                    if k == str(message.author):
                        find = 1
                        ds_name = k
                        break
                if i == name and k == str(message.author):
                    await client.send_message(message.channel, "Вы уже зарегистрированы!")
                else:
                    await client.send_message(message.channel, "Данный никнейм уже используется!")

    if message.content.startswith('!checkduel') and str(message.author) in config.users:
        print("[command]: checkduel")
        if len(duel) == 0:
            await client.send_message(message.channel, "Никто не участвует!")
        else:
            await client.send_message(message.channel, "Участвует только {}".format(duel[0]))
    elif message.content.startswith("checkduel"):
        await client.send_message(message.channel, "Пожалуйста, пройдите регистрацию. !register [twitch name]")

    if message.content.startswith('!duel') and str(message.author) in config.users:
        print("[command]: duel")
        a = str(message.author)
        if a in config.users and a not in duel:
            twitch_name = config.users[a]
            count = streamelements.get_userPoint(token, channel, twitch_name)
            if count >= 100:
                await client.send_message(message.channel, "Вы добавлены в очередь. Ожидайте!")
                duel.append(a)
            else:
                await client.send_message(message.channel, "Не хватает ППШЕК!")
        if len(duel) == 2:
            winner = random.randint(0, 1)
            winner_name = duel[winner]
            twitch_name = config.users[winner_name]
            await client.send_message(message.channel, "Победитель найден! Это {}".format(twitch_name))
            streamelements.change_userPoint(token, channel, twitch_name, 100)
            twitch_loser = abs(winner - 1)
            twitch_loser_name = duel[twitch_loser]
            twitch_loser_name_second = config.users[twitch_loser_name]
            streamelements.change_userPoint(token, channel, twitch_loser_name_second, -100)
            points = streamelements.get_userPoint(token, channel, twitch_name)
            await client.send_message(message.channel, "Ваше состояние: {}".format(str(points)) )
            duel.clear()
    elif message.content.startswith("!duel"):
        await client.send_message(message.channel, "Пожалуйста, пройдите регистрацию. !register [twitch name]")

    if message.content.startswith('!cancel') and str(message.author) in config.users:
        print("[command]: cancel")
        a = message.author
        if a in duel:
            duel.clear()
            await client.send_message(message.channel, "Вы больше не участник!")

    if message.content.startswith('!save_users') and str(message.author) in config.users:
        print("[command]: save_users")
        config.save_users()


def get_btc_price():
    r = requests.get(BTC_PRICE_URL_coinmarketcap)
    response_json = r.json()
    usd_price = response_json[0]['price_usd']
    rub_rpice = response_json[0]['price_rub']
    return usd_price, rub_rpice


client.run(DISCORD_BOT_TOKEN)