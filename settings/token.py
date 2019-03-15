TOKEN = 'c67fa7da119d456f129f4d33ba923b0f481de71f6002f395f0f12ea9b4f877943f4286750e7acdc4dfa98'


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


get_token()
