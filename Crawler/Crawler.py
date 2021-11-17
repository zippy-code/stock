import lxml
import requests
from bs4 import BeautifulSoup

# 여기에 융통성있는 크롤러 만들어봅시다

if __name__ == '__main__':
    url = "https://m.naver.com"
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'lxml')
    print(s)