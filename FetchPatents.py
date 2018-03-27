import requests
from bs4 import BeautifulSoup
import sqlite3
import re
from OperateDatabase import *
import socket
import random
import time
from multiprocessing import Lock, Process
import multiprocessing

socket.setdefaulttimeout(1000)

base_url = 'http://www.freepatentsonline.com'

additional_url = ['/result.html?p=',
                  '&sort=relevance&srch=top&query_txt=AN%2F%22',
                  '%22&patents=on']

# cx = sqlite3.connect('patents.db')

# company_list = ['microsoft']
company_list1 = ['google', 'nintendo', 'IBM', 'amazon', 'intel']
company_list2 = ['microsoft', 'lenovo', 'apple', 'facebook', 'tencent']
company_list3 = ['alibaba', 'hp', 'sony', 'baidu', 'huawei', 'amd']

utils = {'Title': 'title',
         'Inventors': 'inventor',
         'Application Number': 'app_num',
         'Abstract': 'abstract',
         'Publication Date': 'pub_date',
         'Filing Date': 'fil_date',
         'Assignee': 'assignee',
         }

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36',
]


def make_up(page, assignee_name):
    return base_url + additional_url[0] \
           + str(page) + additional_url[1] \
           + assignee_name + additional_url[2]


def lets_rock(companies):
    for ic in companies:
        try:
            company_url = make_up(1, ic)
            r = requests.get(company_url,
                             headers={'User-Agent': random.choice(user_agents)})
            soup = BeautifulSoup(r.text, 'lxml')
            patents_count = int(str(soup.find_all(text=re.compile('Matches'))[0]).strip().split(' ')[-1])
            print(patents_count)
            print('let\'s rock')
            with open('patents_cnt.txt', 'w+') as file:
                file.write('Company: ' + str(ic) + ' Number of patents: ' + str(patents_count) + '\n')
            # for i in range(1, page_count // 50 + 1):
            for i in range(1, min(201, patents_count // 50 + 1)):
                # damn FPO, you can only get 200 pages of patents
                # for i in range(1, 3):
                print('fetching page' + str(i))
                fetch_page(make_up(i, ic))
        except:
            with open('error_report.txt', 'w+') as f:
                f.write('fail fetching company ' + ic + '\n')
        else:
            time.sleep(random.randint(0, 3) / 10)


def fetch_page(company_url):
    r = requests.get(company_url,
                     headers={'User-Agent': random.choice(user_agents)})
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.find_all('table', class_='listing_table')[0].find_all('tr')[1:]

    for it in text:
        url = str(it.select('a')[0]['href']).strip()
        doc_number = str(it.select('td')[1].text).strip()
        score = str(it.find_all('td')[-1].text).strip()
        try:
            fetch_detail(base_url + url, doc_number, score)
        except:
            with open('error_report.txt', 'w+') as f:
                f.write('fail fetching ' + url + '\n')
        else:
            time.sleep(random.randint(0, 3) / 10)


def fetch_detail(detail_url, doc_number, score):
    # print(detail_url)
    # print(doc_number)
    print('fetching patent: ' + str(doc_number))
    r = requests.get(detail_url,
                     headers={'User-Agent': random.choice(user_agents)})
    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.find_all('div', 'disp_doc2')

    data_dict = {}

    for it in text:
        title = it.find('div', 'disp_elm_title')
        t = it.find('div', 'disp_elm_text')

        if title is not None and t is not None:
            title_text = str(title.text).strip().replace(':', '')
            t_text = str(t.text) \
                .strip() \
                .replace('\t', '') \
                .replace('  ', '')
            if title_text in utils:
                data_dict[utils[title_text]] = t_text
        data_dict['app_num'] = doc_number
        data_dict['score'] = score
    insert_data(data_dict)


if __name__ == '__main__':
    # fetch_detail('http://www.freepatentsonline.com/y2017/0346746.html', 'D1234567')
    p1 = Process(target=lets_rock, args=(company_list1, ))
    p2 = Process(target=lets_rock, args=(company_list2, ))
    p3 = Process(target=lets_rock, args=(company_list3, ))
    #
    p1.start()
    p2.start()
    p3.start()
    #
    p1.join()
    p2.join()
    p3.join()
    # lets_rock(company_list)
