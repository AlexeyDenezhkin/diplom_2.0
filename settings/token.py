TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


from urllib.parse import urlencode
AUTH_URL = 'https://oauth.vk.com/authorize?'


def get_token():
    auth_data = {
        'client_id': '6778118',
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'page',
        'response_type': 'token',
        'scope': 'notify,friends,photos,audio,'
                 'video,pages,status,wall,groups',
        'v': '5.92'
    }
    auth_link = AUTH_URL + urlencode(auth_data)
    print(auth_link)
    token = input(str('Перейдите по ссылке, разрешите приложению доступ к Вашему аккаунту, '
                      'скопируйте и вставьте access_token\n'))
    return token
