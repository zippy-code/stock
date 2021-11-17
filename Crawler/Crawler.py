import lxml
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = "https://m.naver.com"
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'lxml')
    print(s)