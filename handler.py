from bs4 import BeautifulSoup
import requests


# Получение n случайных стихотворений
def poem(n=1):
    poem_url = 'http://russian-poetry.ru/Random.php'
    # Создаем текст стихотворения
    text = ''

    # Цикл из n стихов
    for i in range(n):
        # Выполняем запрос к странице со стихами
        response = requests.get(poem_url)
        # Получаем текст страницы
        soup = BeautifulSoup(response.text, 'lxml')

        # Вначале ищем на странице информацию об авторе
        # Проверяем все теги а
        for q in soup.find_all('a'):
            # Ищем непустой атрибут title
            if q.get('title') is not None:
                # Добавляем к тексту
                text += f"<b>{q.get('title')}</b>"
        # Делаем отступ
        text += '\n\n'

        # Ищем тег pre
        q = soup.find_all('pre')
        # Добавляем текст стихотворения
        text += str(q)
        # Удаляем из текста теги pre
        text = text.replace('[<pre>', '').replace('</pre>]', '')
        # Удаляем из текста теги i
        text = text.replace('<i>', '').replace('</i>', '')
        # Делаем отступ
        text += '\n\n'

    return text