import os
import requests

#API_KEY = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
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


def translate_file(original_file, result_file, from_lang, to_lang='ru'):
    # пытаемся прочитать текст из файла
    try:
        with open(original_file) as f:
            text = f.read()
    except OSError:
        print('Ошибка чтения файла: {}'.format(result_file))
        return

    print('Перевод файла... {}'.format(result_file))

    # пытаемся выполнить перевод текста
    try:
        result = translate_it(text, from_lang, to_lang)
    except OSError:
        print('Ошибка перевода файла!')
        return

    # пытаемся записать результат перевода текста
    try:
        with open(result_file, mode='w') as f:
            f.write(result)
        print('Результат перевода сохранен в файл: {}'.format(result_file))
    except OSError:
        print('Ошибка записи файла: {}'.format(result_file))


def main():
    # определяем текущую дерикторию
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # определяем список файлов в директории
    file_list = os.listdir(current_dir)

    for path in file_list:
        # пропускаем возможные вложенные директории
        if os.path.isdir(path):
            continue

        # разделяем имя файла и расширение
        file_name, file_extension = os.path.splitext(path)

        # обрабатываем только файлы txt
        if file_extension.lower() != '.txt':
            continue

        # построим пути читаемого и сохраняемого файла
        original_file = os.path.join(current_dir, path)
        result_file = os.path.join(current_dir, file_name + '_result' + file_extension)

        # вызываем функцию перевода файла
        translate_file(original_file, result_file, file_name.lower())

        print('')


if __name__ == '__main__':
    main()

# requests.post('http://requestb.in/10vc0zh1', json=dict(a='goo', b='foo'))
