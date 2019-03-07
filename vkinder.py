import requests
import time
from User.class_User import User
from settings.token import TOKEN


def like_users():
    user = User(USER_ID)
    user.data_user_get()
    if user.sex == 1:
        sex = '2'
    else:
        sex = '1'
    if user.age is not None:
        age_from = str(user.age - 2)
        age_to = str(user.age + 2)
    else:
        age_from = str(0)
        age_to = str(100)
    params = {
        'count': '1000',
        'fields': 'id,first_name,last_name,bdate,city,country,common_count,'
                  'interests,photo_max_orig,sex,books',
        'access_token': TOKEN,
        'v': '5.92',
        'city': str(user.city),
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to,
        'has_photo': '1'
    }
    response = requests.get('https://api.vk.com/method/users.search', params)
    like_users_data = response.json()
    like_users_list = []
    for user in like_users_data['response']['items']:
        like_users_list.append(user['id'])
    return like_users_list


def sort_users(main_user, other_user):
    age_weight = 0.25
    groups_weight = 0.2
    friends_weight = 0.3
    interests_weight = 0.15
    books_weight = 0.1

    user_ratings = []

    if main_user.age is not None and other_user.age is not None:
        age_dif = main_user.age - other_user.age
        if abs(age_dif) == 0:
            user_ratings.append(4 * age_weight)
        elif abs(age_dif) == 1:
            user_ratings.append(3 * age_weight)
        elif abs(age_dif) == 2:
            user_ratings.append(2 * age_weight)
        else:
            user_ratings.append(1 * age_weight)
    else:
        user_ratings.append(0)

    common_groups = main_user.groups_ & other_user.groups_
    if len(common_groups) > 20:
        user_ratings.append(4 * groups_weight)
    elif 15 < len(common_groups) <= 20:
        user_ratings.append(3 * groups_weight)
    elif 10 < len(common_groups) <= 15:
        user_ratings.append(2 * groups_weight)
    elif 0 < len(common_groups) <= 10:
        user_ratings.append(1 * groups_weight)
    else:
        user_ratings.append(0 * groups_weight)

    common_friends = main_user.friends_ & other_user.friends_
    if len(common_friends) > 20:
        user_ratings.append(4 * friends_weight)
    elif 15 < len(common_friends) <= 20:
        user_ratings.append(3 * friends_weight)
    elif 10 < len(common_friends) <= 15:
        user_ratings.append(2 * friends_weight)
    elif 0 < len(common_friends) <= 10:
        user_ratings.append(1 * friends_weight)
    else:
        user_ratings.append(0 * friends_weight)

    common_interests = main_user.interests & other_user.interests
    if len(common_interests) != 0:
        user_ratings.append(4 * interests_weight)
    else:
        user_ratings.append(0 * interests_weight)

    common_books = main_user.books & other_user.books
    if len(common_books) != 0:
        user_ratings.append(4 * books_weight)
    else:
        user_ratings.append(0 * books_weight)

    return sum(user_ratings)


def top10_like_users(main_user):
    users = like_users(main_user)
    like_users_dict = dict()
    for user in users:
        other_user = User(str(user))
        other_user.data_user_get()
        other_user.friends_get()
        other_user.groups_get()
        like_users_dict[user] = sort_users(main_user, other_user)
    like_users_dict = sorted(like_users_dict.items(),
                             key=lambda x: x[1],
                             reverse=True)

    return like_users_dict


def photos_like_users_get(owner_id):
    params = {
        'owner_id': owner_id,
        'album_id': 'profile',
        'extended': '1',
        'access_token': TOKEN,
        'v': '5.92'
    }
    response = requests.get('https://api.vk.com/method/photos.get', params)
    photos = response.json()
    try:
        photos_dict = dict()
        for photo in photos['response']['items']:
            likes = photo['likes']['count']
            for size in photo['sizes']:
                if size['type'] == 'x':
                    link = size['url']
            photos_dict[link] = likes
        photos_top3 = sorted(photos_dict.items(),
                             key=lambda x: x[1],
                             reverse=True)[0:3]
        time.sleep(0.3)
        return photos_top3
    except KeyError:
        return list()


if __name__ == "__main__":
    USER_ID = input('Введите номер вашего id (имя пользователя) для поиска: ')
    print(like_users())
    print(sort_users())
    print(top10_like_users())

