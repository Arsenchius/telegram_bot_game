from bs4 import BeautifulSoup
import requests

avito_url = 'https://www.avito.ru/?q='


# коды ответов
# 500 - не смог получить цифры
# 400 - Ошибка в запросе


def main(question):
    response = requests.get(avito_url+question)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"lxml")
        try:
            temp = soup.find('span', class_='page-title-count-1oJOc').text.strip()
        except:
            return 500
        return temp
    else:
        return 400 
