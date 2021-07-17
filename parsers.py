from bs4 import BeautifulSoup
import requests
from random import randint
 
avito_url = 'https://www.avito.ru/?q='

# коды ответов
# 500 - не смог получить цифры
# 400 - Ошибка в запросе

# Лист со всеми словами
class object:
    def __init__(self,name,count):
        self.name = name
        self.count = count

def take_words(num):
    file = open("word_rus.txt")
    pack = []
    for i in file:
        pack.append(i.replace("\n",""))

    total_pack = []

    for i in range(1,num):
        num = randint(0,len(pack))
        total_pack.append(pack[num])
    
    return total_pack


def main(question):
    response = requests.get(avito_url+question)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,"lxml")
        try:
            temp = soup.find('span', class_='page-title-count-1oJOc').text.strip()
            return temp
        except:
            return 500
    else:
        return 400 


def complite_pack(num):
    pack = take_words(num)

    total = []

    for i in pack:
        count = main(i)
        total.append(object(i,count))
    
    return total

