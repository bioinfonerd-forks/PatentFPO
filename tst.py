from FetchPatents import *

if __name__ == '__main__':
    r = requests.get('http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&'
                     'query_txt=AN%2F%22nintendo%22&submit=&patents=on')
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.find_all('table', class_='listing_table')[0].find_all('tr')[1:]

    # tds1 = str(text[0].find_all('td')[-1].text).strip()
    # tds2 = str(text[1].find_all('td')[-1].text).strip()
    # tds3 = str(text[2].find_all('td')[-1].text).strip()
    #
    # print(tds1)
    # print(tds2)
    # print(tds3)
    print(len(text))
