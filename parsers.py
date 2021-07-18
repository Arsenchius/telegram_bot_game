from hashlib import new
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
            return temp.replace(u'\xa0', u'')
        except:
            return 500
    else:
        return randint(1,10000)

def pairs(arr):
    new_pack = []
    a = []
    sz = int(len(arr) / 2)
    for i in range(sz):
        a = []
        a.append(arr[i])
        a.append(arr[sz + i])
        new_pack.append(a)
    return new_pack
        

def complite_pack(num):
    pack = take_words(num)

    total = []

    for i in pack:
        count = main(i.encode('cp1251').decode('utf8'))
        total.append(object(i,int(count)))
    
    return pairs(total)

