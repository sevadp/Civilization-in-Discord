import discord
import asyncio
import requests
import streamelements
import config
import random
import time
import json
import datetime

DISCORD_BOT_TOKEN = 'NDQyNTYxNTkzMjIyNDk2MjU4.D0H6Zw.H50D_hx6xKPg13Sb-Ch8kCRgle8'

channel = "5abf2d6958a6665863b088c7"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNWFiZjJkNjk1OGE2NjZkOTk4YjA4O" \
        "GM2IiwiY2hhbm5lbCI6IjVhYmYyZDY5NThhNjY2NTg2M2IwODhjNyIsInByb3ZpZGVyIjoidHd" \
        "pdGNoIiwicm9sZSI6Im93bmVyIiwiYXV0aFRva2VuIjoiVENjblc5SWF4MWJKZG1RMkdDVkJmUFVIODdiQ" \
        "1dWNzAwUkxET29SZF9DcjFBajdjIiwiaWF0IjoxNTQxNzc0MjM1LCJpc3MiOiJTdHJlYW1FbGVt" \
        "ZW50cyJ9.JaWB3MC8bNX11LuX9zjukcNRV8pyRhje2wcCvUoDzDc"

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
        # Подгрузка настроек
        with open('data.json', 'r') as fp:
            config.settings = json.load(fp)
        start = 1

    if config.settings["horde_now"][0] != "":
        print("[command]: horde_now")
        d = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")).split()
        b = [int(i) for i in d[0].split("-")]
        c = [int(i) for i in d[1].split(":")]
        k = c[0] * 60 + c[1] + b[1] * 24 * 60 +\
            b[1] * 24 * 30 * 60 + b[2] * 365 * 24 * 60
        config.settings["horde_now"][1] += (k - config.settings["horde_now"][2]) * 3 \
                                           * config.settings["resources_horde"]["science"]
        config.settings["horde_now"][2] = k
        if config.check_upgrades(config.settings["horde_now"][0], config.settings["horde_now"][1]):
            config.settings["upgrades_horde"][config.settings["horde_now"][0]] = 1
            config.settings["horde_now"][0] = ""
            config.settings["horde_now"][1] = 0
            config.settings["horde_now"][2] = 0
        config.save_json()

    if config.settings["alliance_now"][0] != "":
        print("[command]: alliance_now")
        d = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")).split()
        b = [int(i) for i in d[0].split("-")]
        c = [int(i) for i in d[1].split(":")]
        k = c[0] * 60 + c[1] + b[1] * 24 * 60 +\
            b[1] * 24 * 30 * 60 + b[2] * 365 * 24 * 60
        config.settings["alliance_now"][1] += (k - config.settings["alliance_now"][2]) * 3 *\
                                              config.settings["resources_alliance"]["science"]
        config.settings["alliance_now"][2] = k
        if config.check_upgrades(config.settings["alliance_now"][0], config.settings["alliance_now"][1]):
            config.settings["alliance_horde"][config.settings["alliance_now"][0]] = 1
            config.settings["alliance_now"][0] = ""
            config.settings["alliance_now"][1] = 0
            config.settings["alliance_now"][2] = 0
        config.save_json()

    if str(message.author) not in config.settings["users"]:
        # Регистрация
        if message.content.startswith('!register'):
            print("[command]: register")
            a = message.content
            if len(a.split()) != 2:
                await client.send_message(message.channel, "Ввод нарушен! Не 2 элемента ввода.")
            else:
                name = a.split()[1]
                test = 0
                for i in config.settings["users"].values():
                    if i == name:
                        test = 1
                        break
                if test == 0:
                    id_discord = str(message.author)
                    config.add_user(id_discord, name)
                    config.save_json()
                    await client.send_message(message.channel, "Успешная регистрация!")
                else:
                    for k in config.settings["users"].keys():
                        if k == str(message.author):
                            break
                    if i == name and k == str(message.author):
                        await client.send_message(message.channel, "Вы уже зарегистрированы!")
                    else:
                        await client.send_message(message.channel, "Данный никнейм уже используется!")
    else:
        # Список командв
        if message.content.startswith('!smorc'):
            print('[command]: smorc ')
            await client.send_message(message.channel, "1) !listusers - список участников SMORCWORLD")
            time.sleep(0.25)
            await client.send_message(message.channel, "2) !register [twitch name] - Регистрация SMORCWORLD")

        # pp на твиче
        if message.content.startswith('!pp'):
            print("[command]: pp")
            twitch_name = config.settings["users"][str(message.author)]
            await client.send_message(message.channel, streamelements.get_userPoint(token, channel, twitch_name))

        # Фонды орды
        if message.content.startswith('!horde'):
            print("[command]: funds_horde")
            gen = config.settings["horde_funds"]
            undead = config.settings["funds"]["undead"]
            orcs = config.settings["funds"]["orcs"]
            trolls = config.settings["funds"]["trolls"]
            result = "Сумма - " + str(undead + orcs + trolls + gen) + ", Орки - " + str(orcs) + ", Нежить - " + \
                     str(undead) + ", Тролли - " + str(trolls) + ". ФОНД ОРДЫ " + str(gen)
            await client.send_message(message.channel, result)

        # Фонды альянса
        if message.content.startswith('!alliance'):
            print("[command]: funds_alliance")
            gen = config.settings["alliance_funds"]
            humans = config.settings["funds"]["humans"]
            dwarfs = config.settings["funds"]["dwarfs"]
            night_elves = config.settings["funds"]["night_elves"]
            result = "Сумма - " + str(humans + dwarfs + night_elves + gen) + ", Люди - " + str(humans) + ", Дварфы - " + \
                str(dwarfs) + ", Ночные эльфы - " + str(night_elves) + ". ФОНД АЛЬЯНСА " + str(gen)
            await client.send_message(message.channel, result)

        # Доступные апгрейды
        if message.content.startswith('!available'):
            print("[command]: available")

            name = ""
            if config.get_nation(message.author) != -1:
                name = config.get_nation(message.author)

            st = ""

            if name == "humans" or name == "dwarfs" or name == "night_elves":
                st = "alliance"
            elif name == "trolls" or name == "undead" or name == "orcs":
                st = "horde"

            if st != "":
                nation = "upgrades_" + st
                if config.settings[nation]["arsenal"] == 1:

                    war = "Доступные технологии:"

                    count = 0

                    if config.settings[nation]["armor_up_1"] != 0:
                        count += 1
                    else:
                        war += " Armor_UP 1 (500 armor_up_1);"

                    if config.settings[nation]["damage_up_1"] != 0:
                        count += 1
                    else:
                        war += " Damage_UP 1 (500 damage_up_1);"

                    if config.settings[nation]["t1_squad"] != 0:
                        count += 1
                    else:
                        war += " T1 SQUAD (500 t1_squad);"

                    if count == 3:
                        war = "Доступные технологии:"

                        count = 0

                        if config.settings[nation]["armor_up_2"] != 0:
                            count += 1
                        else:
                            war += " Armor_UP 2 (3000 armor_up_2);"

                        if config.settings[nation]["damage_up_2"] != 0:
                            count += 1
                        else:
                            war += " Damage_UP 2 (3000 damage_up_2);"

                        if config.settings[nation]["t2_squad"] != 0:
                            count += 1
                        else:
                            war += " T2 SQUAD (3000 t2_squad);"

                        if count == 3:
                            war = "Доступные технологии:"

                            count = 0

                            if config.settings[nation]["armor_up_3"] != 0:
                                count += 1
                            else:
                                war += " Armor_UP 3 (12000 armor_up_3);"

                            if config.settings[nation]["damage_up_3"] != 0:
                                count += 1
                            else:
                                war += " Damage_UP 3 (12000 damage_up_3);"

                            if config.settings[nation]["t3_squad"] != 0:
                                count += 1
                            else:
                                war += " T3 SQUAD (12000 t3_squad);"

                            if count == 3:
                                war += " В военном направлении отсутствуют."
                                await client.send_message(message.channel, war)
                            else:
                                await client.send_message(message.channel, war)

                        else:
                            await client.send_message(message.channel, war)
                    else:
                        await client.send_message(message.channel, war)

                    war = ""
                    time.sleep(0.25)

                    a = 0
                    b = 0
                    c = 0

                    if config.settings[nation]["Library"] >= 2:
                        a = 2
                    elif config.settings[nation]["Library"] == 0:
                        war += " Библиотека (800 Library);"

                    if config.settings[nation]["Monument"] >= 2:
                        b = 2
                    elif config.settings[nation]["Monument"] == 0:
                        war += " Монумент (800 monument);"

                    if config.settings[nation]["career"] >= 2:
                        c = 2
                    elif config.settings[nation]["career"] == 0:
                        war += " Шахта (800 career);"

                    if a + b + c == 6:
                        if config.settings[nation]["Cottage"] == 0:
                            war += " Коттедж (2200 Cottage);"
                        if config.settings[nation]["Towers"] == 0:
                            war += " Оборона (2200 Towers);"
                        if config.settings[nation]["Trade"] == 0:
                            war += " Торговля (2200 Trade);"

                        if war == "":
                            await client.send_message(message.channel, "В научном направлении изучений нет.")
                        else:
                            await client.send_message(message.channel, war)

                    else:
                        await client.send_message(message.channel, war)

                else:
                    await client.send_message(message.channel, "Доступные технологии - Арсенал. (300 name - arsenal)")

        if message.content.startswith('!up_horde'):
            print("[command]: up_horde")
            a = message.content
            if len(a.split()) != 2:
                await client.send_message(message.channel, "Ошибка ввода.")
            else:
                if a.split()[1] not in list(config.settings["upgrades_horde"].keys()):
                    await client.send_message(message.channel, "Изучение не обнаружено.")
                else:
                    if config.settings["upgrades_horde"][a.split()[1]] != 0:
                        await client.send_message(message.channel, "Уже исследовано.")
                    else:
                        if config.settings["horde_now"][0] == "":
                            d = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")).split()
                            b = [int(i) for i in d[0].split("-")]
                            c = [int(i) for i in d[1].split(":")]
                            config.settings["horde_now"][2] = c[0] * 60 + c[1] + b[1] * 24 * 60 + b[1] * 24 \
                                                              * 30 * 60 + b[2] * 365 * 24 * 60
                            config.settings["horde_now"][1] = 0
                            config.settings["horde_now"][0] = a.split()[1]
                            config.save_json()

        if message.content.startswith('!up_alliance'):
            print("[command]: up_alliance")
            a = message.content
            if len(a.split()) != 2:
                await client.send_message(message.channel, "Ошибка ввода.")
            else:
                if a.split()[1] not in list(config.settings["upgrades_alliance"].keys()):
                    await client.send_message(message.channel, "Изучение не обнаружено.")
                else:
                    if config.settings["upgrades_alliance"][a.split()[1]] != 0:
                        await client.send_message(message.channel, "Уже исследовано.")
                    else:
                        if config.settings["alliance_now"][0] == "":
                            d = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M")).split()
                            b = [int(i) for i in d[0].split("-")]
                            c = [int(i) for i in d[1].split(":")]
                            config.settings["alliance_now"][2] = c[0] * 60 + c[1] + b[1] * 24 * 60 + b[1] * 24 \
                                                              * 30 * 60 + b[2] * 365 * 24 * 60
                            config.settings["alliance_now"][1] = 0
                            config.settings["alliance_now"][0] = a.split()[1]
                            config.save_json()

        # Перевод в общий фонд.
        if message.content.startswith('!translate'):
            name = ""
            print("[command]: translate")
            if config.get_leaders(message.author) != -1:
                name = config.get_leaders(message.author)
                lead = config.settings["funds"][config.get_leaders(message.author)]
            else:
                lead = 0
            if name == "humans" or name == "dwarfs" or name == "night_elves":
                a = message.content
                if len(a.split()) != 2:
                    await client.send_message(message.channel, "Ввод нарушен! Не 2 элемента ввода.")
                else:
                    try:
                        c = int(a.split()[1])
                        if 0 < c <= lead:
                            config.settings["alliance_funds"] += c
                            config.settings["funds"][config.get_leaders(message.author)] -= c
                            await client.send_message(message.channel, "Выполнено!")
                            config.save_json()
                        else:
                            await client.send_message(message.channel, "Недостаточно PP")

                    except Exception as f:
                        await client.send_message(message.channel, "2 значение нарушено")
                        print(f)

            if name == "trolls" or name == "undead" or name == "orcs":
                a = message.content
                if len(a.split()) != 2:
                    await client.send_message(message.channel, "Ввод нарушен! Не 2 элемента ввода.")
                else:
                    try:
                        c = int(a.split()[1])
                        if 0 < c <= lead:
                            config.settings["horde_funds"] += lead
                            config.settings["funds"][config.leaders(message.author)] -= lead
                            await client.send_message(message.channel, "Выполнено!")
                            config.save_json()
                        else:
                            await client.send_message(message.channel, "Недостаточно PP")

                    except Exception as f:
                        await client.send_message(message.channel, "2 значение нарушено")
                        print(f)

        # status в фонд своей расы
        if message.content.startswith('!status'):
            print("[command]: status")
            a = config.settings["funds"][config.get_nation(message.author)]
            if a != "":
                a = "Фонд Расы: " + str(a)
                lead = config.get_nation(message.author)
                if lead == "humans" or lead == "dwarfs" or lead == "night_elves":
                    a = a + "; Исследование: " + config.settings["alliance_now"][0] +\
                        "  и набрано молоточков: " + str(config.settings["alliance_now"][1])
                else:
                    a = a + "; Исследование: " + config.settings["horde_now"][0] +\
                        " и набрано молоточков: " + str(config.settings["horde_now"][1])
                await client.send_message(message.channel, a)


            # put в фонд своей расы
        if message.content.startswith('!put'):
            print("[command]: put")
            a = message.content
            b = str(message.author)
            if len(a.split()) != 2:
                await client.send_message(message.channel, "Ввод нарушен! Не 2 элемента ввода.")
            else:
                try:
                    c = int(a.split()[1])
                    twitch_name = config.settings["users"][b]
                    count = streamelements.get_userPoint(token, channel, twitch_name)
                    if 0 < c <= count:
                            config.settings["funds"][config.get_nation(message.author)] += c
                            streamelements.change_userPoint(token, channel, twitch_name, -c)
                            await client.send_message(message.channel, "Выполнено!")
                            config.save_json()
                    else:
                        await client.send_message(message.channel, "Недостаточно PP")

                except Exception as f:
                    await client.send_message(message.channel, "2 значение нарушено")
                    print(f)

        # Dict из юзеров
        if message.content.startswith('!listusers'):
            print('[command]: listusers ')
            await client.send_message(message.channel, config.settings["users"])

        # Сохрание юзеров
        if message.content.startswith('!save_json'):
            print("[command]: save_json")
            config.save_json()
            await client.send_message(message.channel, "Выполнено.")

        # Принадлежность к фракции, тесты
        if message.content.startswith('!what_frac'):
            print("[command]: what_frac")
            await client.send_message(message.channel, config.get_nation(message.author))

client.run(DISCORD_BOT_TOKEN)