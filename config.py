import json


HOST = "irc.twitch.tv"
PORT = 6667
NICK = "deadlystilebot"
PASS = "oauth:zgav5g0aixr7sfxlqw9w7s9mubi3km"
CHAN = "sevadp_"
RATE = (20/30)


oplist = {}
nations = {"Люди (Альянс)": "humans", "Ночные эльфы (альянс)": "night_elves", "Тролли (орда)": "trolls",
           "Дварфы (альянс)": "dwarfs", "Нежить (орда)": "undead", "Орки (орда)": "orcs"}

leaders = {"Король людей (альянс)": "humans", "Правитель ночных эльфов (альянс)": "night_elves", "Вождь троллей": "trolls",
           "Король дварфов": "dwarfs", "Предводитель нежити": "undead", "Вождь орды": "orcs"}

settings = dict()


def add_user(discord, twitch):
    settings["users"][discord] = twitch


def get_json():
    with open('data.json', 'r') as fp:
        settings = json.load(fp)


def save_json():
    with open('data.json', 'w') as fp:
        json.dump(settings, fp)


def get_nation(author):
    for i in author.roles:
        if str(i) in list(nations.keys()):
            for j in range(len(list(nations.keys()))):
                if list(nations.keys())[j] == str(i):
                    return nations[list(nations.keys())[j]]
    return -1


def get_leaders(author):
    for i in author.roles:
        if str(i) in list(nations.keys()):
            for j in range(len(list(nations.keys()))):
                if list(nations.keys())[j] == str(i):
                    return nations[list(nations.keys())[j]]
    return -1


def check_upgrades(name, now):
    if name == "arsenal" and now >= 300:
        return 1
    elif name == "armor_up_1" and now >= 500:
        return 1
    elif name == "damage_up_1" and now >= 500:
        return 1
    elif name == "t1_squad" and now >= 500:
        return 1
    elif name == "armor_up_2" and now >= 3000:
        return 1
    elif name == "damage_up_2" and now >= 3000:
        return 1
    elif name == "t2_squad" and now >= 3000:
        return 1
    elif name == "armor_up_3" and now >= 12000:
        return 1
    elif name == "damage_up_3" and now >= 12000:
        return 1
    elif name == "t3_squad" and now >= 12000:
        return 1
    elif name == "Library" and now >= 800:
        return 1
    elif name == "Monument" and now >= 800:
        return 1
    elif name == "career" and now >= 800:
        return 1
    elif name == "Cottage" and now >= 2200:
        return 1
    elif name == "Towers" and now >= 2200:
        return 1
    elif name == "Trade" and now >= 2200:
        return 1
    return 0