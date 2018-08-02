import os
from builtins import OSError

import requests


# API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
API_KEY = 'trnsl.1.1.20180801T160940Z.cb1c7bacc53f5e1c.6222e7c1ec7a313b9a1f9952f5339605b7d9257f'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(text, from_lang, to_lang='ru'):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param to_lang:
    :return:
    """

    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}-{}'.format(from_lang, to_lang)
    }

    response = requests.get(URL, params=params)
    json_ = response.json()

    return ''.join(json_['text'])


def read_file(path):
    try:
        with open(path) as f:
            text = f.read()
            return text
    except OSError:
        print('Ошибка чтения файла! {}'.format(path))
        return ''


def write_file(path, text):
    # пытаемся записать результат перевода текста
    try:
        with open(path, mode='w') as f:
            f.write(text)
        return True # успешное сохранение файла
    except OSError:
        print('Ошибка записи файла! {}'.format(path))
        return False # не успешное сохранение файла

def main():
    # определяем текущую дерикторию
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # определяем список файлов в директории
    file_list = os.listdir(current_dir)

    for path in file_list:
        # пропускаем возможные вложенные директории
        if os.path.isdir(path):
            continue

        # обрабатываем только файлы txt
        if not path.endswith('.txt'):
            continue

        # разделяем на имя файла и расширение, для формирования имени результирующего файла
        file_name, file_extension = os.path.splitext(path)

        # построим пути читаемого и сохраняемого файла
        original_file = os.path.join(current_dir, path)
        result_file = os.path.join(current_dir, file_name + '_result' + file_extension)

        print('Переводим файл {}...'.format(original_file))

        # пытаемся прочитать текст из файла
        text = read_file(original_file)

        # ошибка чтения файла
        if not text:
            continue

        # пытаемся выполнить перевод текста
        result = translate_it(text, file_name.lower())

        # вызываем функцию перевода файла
        result = write_file(result_file, result)

        if result:
            print('Результат перевода сохранен в файл: {}'.format(result_file))

        print('')

    print('Перевод файлов завершен')


if __name__ == '__main__':
    main()

# requests.post('http://requestb.in/10vc0zh1', json=dict(a='goo', b='foo'))
