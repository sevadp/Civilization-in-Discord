import requests
import json


def get_userList(channel):
    users = []
    session = requests.session()
    response = session.get('https://tmi.twitch.tv/group/user/%s/chatters' % channel).text
    data = json.loads(response)
    users = data['chatters']['moderators']
    users.extend(data['chatters']['viewers'])
    return users


def get_userPoint(token, channel, user):
    session = requests.session()
    headers = {'Authorization': 'Bearer %s' % token}
    response = session.get('https://api.streamelements.com/kappa/v2/points/' + channel + "/" + user,
                           headers=headers).text
    data = json.loads(response)
    return data['points']


def change_userPoint(token, channel, user, value):
    session = requests.session()
    headers = {'Authorization': 'Bearer %s' % token}
    session.put('https://api.streamelements.com/kappa/v2/points/' + channel + "/" + user + "/" + str(value), headers=headers)

channel = "5abf2d6958a6665863b088c7"

