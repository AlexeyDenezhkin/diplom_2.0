import requests
import string
from datetime import datetime
import time
from pprint import pprint
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

            if 'city' in user_info['response'][0]:
                self.city = int(user_info['response'][0]['city']['id'])

            if 'sex' in user_info['response'][0]:
                self.sex = int(user_info['response'][0]['sex'])

            if 'relation' in user_info['response'][0]:
                self.relation = int(user_info['response'][0]['relation'])

            if 'interests' in user_info['response'][0]:
                interests = user_info['response'][0]['interests']
                interests = ''.join(l for l in interests if l not in string.punctuation)
                self.interests = set(interests.lower().split())

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
        try:
            response = requests.get('https://api.vk.com/method/friends.get', params)
            friends_info = response.json()
            friends_set = set()
            for friend in friends_info['response']['items']:
                friends_set.add(friend['id'])
            return friends_set
        except KeyError:
            return set()

    def groups_get(self):
        params = {
            'user_id': self.user_id,
            'extended': '1',
            'access_token': TOKEN,
            'v': '5.92',
            'fields': 'members_count'
        }
        try:
            response = requests.get('https://api.vk.com/method/groups.get', params)
            groups_info = response.json()
            groups_set = set()
            for group in groups_info['response']['items']:
                groups_set.add(group['id'])
            return groups_set
        except KeyError:
            return set()

    def photos_get(self):
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': '1',
            'access_token': TOKEN,
            'v': '5.92'
        }
        response = requests.get('https://api.vk.com/method/photos.get', params)
        owner_photos = response.json()
        try:
            photos_dict = dict()
            for photo in owner_photos['response']['items']:
                likes = photo['likes']['count']
                for size in photo['sizes']:
                    if size['type'] == 'x':
                        link = size['url']
                photos_dict[link] = likes

            top3_photos = sorted(photos_dict.items(),
                                 key=lambda x: x[1],
                                 reverse=True)[0:3]
            time.sleep(0.3)
            return top3_photos
        except KeyError:
            return list()


class MainUser(User):
    friends_weight = 0.3
    age_weight = 0.25
    groups_weight = 0.2
    interests_weight = 0.15
    books_weight = 0.1
    like_users = list()

    def compare_user_with(self, other):
        user_ratings = []
        if self.age is not None and other.age is not None:
            age_dif = self.age - other.age
            if abs(age_dif) == 0:
                user_ratings.append(4 * self.age_weight)
            elif abs(age_dif) == 1:
                user_ratings.append(3 * self.age_weight)
            elif abs(age_dif) == 2:
                user_ratings.append(2 * self.age_weight)
            else:
                user_ratings.append(1 * self.age_weight)
        else:
            user_ratings.append(0)

        common_friends = self.friends_ & other.friends_
        if len(common_friends) > 20:
            user_ratings.append(4 * self.friends_weight)
        elif 15 < len(common_friends) <= 20:
            user_ratings.append(3 * self.friends_weight)
        elif 10 < len(common_friends) <= 15:
            user_ratings.append(2 * self.friends_weight)
        elif 0 < len(common_friends) <= 10:
            user_ratings.append(1 * self.friends_weight)
        else:
            user_ratings.append(0 * self.friends_weight)

        common_groups = self.groups_ & other.groups_
        if len(common_groups) > 20:
            user_ratings.append(4 * self.groups_weight)
        elif 15 < len(common_groups) <= 20:
            user_ratings.append(3 * self.groups_weight)
        elif 10 < len(common_groups) <= 15:
            user_ratings.append(2 * self.groups_weight)
        elif 0 < len(common_groups) <= 10:
            user_ratings.append(1 * self.groups_weight)
        else:
            user_ratings.append(0 * self.groups_weight)

        common_interests = self.interests & other.interests
        if len(common_interests) != 0:
            user_ratings.append(4 * self.interests_weight)
        else:
            user_ratings.append(0 * self.interests_weight)

        common_books = self.books & other.books
        if len(common_books) != 0:
            user_ratings.append(4 * self.books_weight)
        else:
            user_ratings.append(0 * self.books_weight)

        return sum(user_ratings)

    def like_users_get(self):
        if self.sex == 2:
            sex = '1'
        else:
            sex = '2'

        age_from = str(input('Введите диапазон возраста для поиска: \n'
                             'от: '))
        age_to = str(input('до: '))

        params = {
            'count': '50',
            'fields': 'id,first_name,last_name,bdate,city,country,common_count,'
                      'interests,photo_max_orig,sex,books,status',
            'access_token': TOKEN,
            'v': '5.92',
            'city': str(self.city),
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
            'has_photo': '1',
            'status': '6'
        }
        response = requests.get('https://api.vk.com/method/users.search', params)
        like_users_data = response.json()
        like_users_list = []
        for user in like_users_data['response']['items']:
            like_users_list.append(user['id'])
        self.like_users = like_users_list
        return like_users_list


if __name__ == "__main__":
    User = User('eshmargunov')
    User.friends_get()
    User.groups_get()
    pprint(User.data_user_get())
    pprint(User.__dict__)
