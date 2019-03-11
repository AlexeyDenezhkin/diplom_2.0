from User.class_User import User, MainUser
from database.database import DataBase
from pprint import pprint


def top10_users(main_user):
    database = DataBase()
    like_users = main_user.like_users_get()
    like_users_dict = dict()
    like_users_photos = dict()
    for user in like_users:
        if database.check(user):
            other_user = User(str(user))
            other_user.data_user_get()
            other_user.groups_get()
            other_user.friends_get()
            like_users_photos[user] = other_user.photos_get()
            like_users_dict[user] = main_user.compare_user_with(other_user)
            print('...')
        else:
            continue
    like_users_dict = sorted(like_users_dict.items(),
                             key=lambda x: x[1],
                             reverse=True)

    data_to_db = list()
    for user in like_users_dict[0:10]:
        top10_users_dict = dict()
        user_photos = like_users_photos[user[0]]
        photos_list = list()
        for photo in user_photos:
            photos_list.append(photo[0])
        top10_users_dict['user_id'] = user[0]
        top10_users_dict['user_page'] = 'https://vk.com/id' + str(user[0])
        top10_users_dict['photos'] = photos_list
        data_to_db.append(top10_users_dict)
    database.add(data_to_db)
    return data_to_db


if __name__ == "__main__":
    main_user = MainUser('eshmargunov')
    main_user.data_user_get()
    main_user.friends_get()
    main_user.groups_get()
    top_10 = top10_users(main_user)
    pprint(top_10)
