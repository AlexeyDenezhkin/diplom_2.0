import requests
import string
from datetime import datetime
import time
from settings.token import TOKEN


class User:
    sex = None
    bdate = None
    age = None
    city = None
    interests = set()
    friends_ = set()
    groups_ = set()
    books = set()

    def __init__(self, user_id):
        if str(user_id).isdigit():
            self.user_id = user_id
        else:
            params = {
                'user_ids': user_id,
                'access_token': TOKEN,
                'v': '5.92',
            }
            response = requests.get('https://api.vk.com/method/users.get', params)
            user_info = response.json()
            self.user_id = user_info['response'][0]['id']

    def data_user_get(self):
        params = {
            'user_ids': self.user_id,
            'fields': 'id,first_name,last_name,bdate,city,country,common_count,'
                      'interests,photo_max_orig,sex,books',
            'access_token': TOKEN,
            'v': '5.92'
        }
        response = requests.get('https://api.vk.com/method/users.get', params)
        user_info = response.json()
        try:
            if 'bdate' in user_info['response'][0]:
                try:
                    bdate = datetime.strptime(user_info['response'][0]['bdate'], '%d.%m.%Y').date()
                    self.bdate = bdate
                    age = datetime.today().year - bdate.year \
                          - ((datetime.today().month, datetime.today().day)
                             < (bdate.month, bdate.day))
                    self.age = age
                except ValueError:
                    self.bdate = self.bdate
                    self.age = self.age
            else:
                self.bdate = self.bdate

            if 'city' in user_info['response'][0]:
                self.city = int(user_info['response'][0]['city']['id'])
            else:
                self.city = self.city

            if 'sex' in user_info['response'][0]:
                self.sex = int(user_info['response'][0]['sex'])
            else:
                self.sex = self.sex

            if 'interests' in user_info['response'][0]:
                interests = user_info['response'][0]['interests']
                interests = ''.join(l for l in interests if l not in string.punctuation)
                self.interests = set(interests.lower().split())
            else:
                self.interests = set()

        except KeyError:
            pass
        time.sleep(0.3)
        return user_info

    def friends_get(self):
        params = {
            'user_id': self.user_id,
            'access_token': TOKEN,
            'v': '5.92',
            'fields': 'domain'
        }
        response = requests.get('https://api.vk.com/method/friends.get', params)
        friends_info = response.json()
        friends_set = set()
        for friend in friends_info['response']['items']:
            friends_set.add(friend['id'])
        return friends_set

    def groups_get(self):
        params = {
            'user_id': self.user_id,
            'extended': '1',
            'access_token': TOKEN,
            'v': '5.92',
            'fields': 'members_count'
        }
        response = requests.get('https://api.vk.com/method/groups.get', params)
        groups_info = response.json()
        groups_set = set()
        for group in groups_info['response']['items']:
            groups_set.add(group['id'])
        return groups_set
