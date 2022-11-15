import requests
from Token import token
from tqdm import tqdm
import json


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        res = response.json()
        if response.status_code == 200:
            for user in res['response']:
                if user['is_closed']:
                    print('Профиль закрыт')
                    exit(0)
            print('Профиль доступен')
            return user['id']
        return 'ошибка'

    def get_foto_data(self):
        id = VK.users_info(self)
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': id,
            'album_id': 'profile',
            'count': '5', 'extended': '1'}
        response = requests.get(URL, params={**self.params, **params})
        res = response.json()
        if response.status_code == 200:
            return res['response']['items']

    def get_foto_dict(self):
        data = VK.get_foto_data(self)
        fotos_data = {}
        try:
            for comp in tqdm(data, desc="Progress"):
                type = comp['sizes'][-1]['type']
                data = comp['date']
                name = comp['likes']['count']
                file = comp['sizes'][-1]['url']
                if name in fotos_data:
                    fotos_data[f'{name}_{data}'] = [file, type]
                else:
                    fotos_data[name] = [file, type]
            print('Файлы готовы к загрузке')
            return fotos_data
        except:
            print('ошибка')


class YandexDisk:
    URL_FILE = 'https://cloud-api.yandex.net/v1/disk/resources'
    URL_UPLOAD = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def __init__(self, token):
        self.token = token_1

    @property
    def header(self):
        return {'Content-Type': 'Application/json',
                'Accept': 'application/json',
                'Authorization': f'OAuth {self.token}'}

    def get_folder(self):
        params = {'path': 'VKfoto'}
        res = requests.put(self.URL_FILE, headers=self.header, params=params)
        if res.status_code == 201:
            print('Создаём папку VKfoto')
        if res.status_code == 409:
            print('Папка VKfoto уже была, загружаем в неё')

    def upload_file(self, dict):
        self.get_folder()
        list = []
        for key, value in tqdm(dict.items(), desc="Progress"):
            params = {'path': f'VKfoto/{key}.jpg', 'url': value[0]}
            response = requests.post(self.URL_UPLOAD, headers=self.header, params=params)
            list.append({'file_name': f'{key}.jpg', 'size': value[1]})
        if response.status_code == 202:
            print('Фотографии уже на Яндекс диске в папке')
            return list
        return 'ошибка'

    def json_file(self, list):
        res = json.dumps(list)
        with open('Json_file.json', 'w') as f:
            f.write(res)
        print(res)


if __name__ == '__main__':
    access_token = token
    user_id = input('Введите Id или никнейм:\n')
    token_1 = input('Введите Яндекс токен:\n')
    vk = VK(access_token, user_id)
    foto_dict = vk.get_foto_dict()
    instance = YandexDisk(token_1)
    file_list = instance.upload_file(foto_dict)
    print()
    YandexDisk.json_file(file_list, file_list)