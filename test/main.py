import requests
import openpyxl
from bs4 import BeautifulSoup
import math
import pandas
import re
from konlpy.tag import Hannanum

Han = Hannanum()  

query = input('검색 키워드를 입력하세요 : ') 
news_num = int(input('필요한 뉴스기사의 수를 입력하세요(숫자만 입력) : '))
sort = int(input('관련도순(0), 최신순(1), 오래된순(2)(숫자만 입력) : '))
url = "https://search.naver.com/search.naver?"
#url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort="+sort+"&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(page)

params = {
    "where": 'news',

    # 네이버 기사 검색 값
    "query": query,
    
    "sort": sort,

    # 페이지네이션 값
    "start": 0,

    # "nso": 'so:r,p:1y,a:all'
}

# nso: so: r, p: 1y, a: all -> 최근 1년
# nso: so: r, p: 6m, a: all -> 최근 6개월
# nso: so: r, p: 1d, a: all -> 1일
# 없으면 전체 검색

# headers={'User-Agent': 'Mozilla/5.0'} -> 안티 크롤링 회피
raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
html = BeautifulSoup(raw.text, "html.parser")

print('크롤링 중...')
idx = 0
news_dict = {}
cur_page = 1

while idx < news_num:
    table = html.find('ul', {'class' : 'list_news'})
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
    a_list = [area.find('a', {'class' : 'news_tit'}) for area in area_list]
    txt_list = [txt.find('a', {'class' : 'api_txt_lines dsc_txt_wrap'}) for txt in area_list]
    
    idx_in = 0
    for n in a_list[:min(len(a_list), news_num-idx)]:
        news_dict[idx] = {'title'   : n.get('title'),
                          'desc'    : txt_list[idx_in].text, #beautifulsoup4 4.6.0을 사용할 때는 find 함수 호출 후 .text 로 문자열만 뽑아내야 한다.
                          'token'   : Han.nouns(txt_list[idx_in].text),
                          #'desc' : area_list[idx_in].select_one('div.news_wrap.api_ani_send > div.news_area > div.news_dsc > div.dsc_wrap > a').text, #konlpy는 beautifulsoup4 4.10.0 지원하지 않음. 
                          'url'     : n.get('href'), }
        idx_in += 1
        idx += 1

    cur_page += 1
    next_page_url = ""
    pages = html.find('div', {'class' : 'sc_page_inner'})
    for p in pages.find_all('a'):
        if p.text == str(cur_page):
            next_page_url = [p][0].get('href')
        else:
            continue
    if next_page_url != '':
        req = requests.get('https://search.naver.com/search.naver' + next_page_url)
        html = BeautifulSoup(req.text, 'html.parser')
    else:
        break


print('크롤링 완료')

print('데이터프레임 변환')
news_df = pandas.DataFrame(news_dict).T

news_df.to_csv('blockChain_articles.csv')
news_df.to_excel('blockChain_articles.xlsx')