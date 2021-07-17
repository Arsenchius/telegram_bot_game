from warnings import resetwarnings
from bs4 import BeautifulSoup
import requests

avito_url = 'https://www.avito.ru/?q='

def main(question):
    response = requests.get(avito_url+question)
    if response.status_code == 200:
        print("Успешно")
        soup = BeautifulSoup(response.text,"lxml")
        temp = soup.find('span', class_='page-title-count-1oJOc').text.strip()
        return temp
