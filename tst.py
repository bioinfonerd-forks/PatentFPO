from FetchPatents import *

if __name__ == '__main__':
    r = requests.get('http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&'
                     'query_txt=AN%2F%22nintendo%22&submit=&patents=on')
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.find_all('tr', 'rowalt')

    tds = str(text[0].find_all('td')[-1].text).strip()

    print(tds)
