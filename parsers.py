from warnings import resetwarnings
from bs4 import BeautifulSoup
import requests

url = 'https://www.google.com/search?q='
new_url = 'https://yandex.ru/search/?lr=213&text='
ozon_url = 'https://www.ozon.ru/category/igrushki-antistress-7181/?from_global=true&text='
avito_url = 'https://www.avito.ru/?q='
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
}

def main(question):
    response = requests.get(avito_url+question)
    if response.status_code == 200:
        print("Успешно")
        soup = BeautifulSoup(response.text,"lxml")
        temp = soup.find('span', class_='page-title-count-1oJOc').text.strip()
        return temp
