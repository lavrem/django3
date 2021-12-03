import requests
import codecs
from bs4 import BeautifulSoup as bs
from random import randint

__all__ = ('hh', 'superjob')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def hh(uri, city=None, language=None):
    if uri:
        resp = requests.get(uri, headers=headers[randint(0,2)])
        jobs = []
        errors = []
        if resp.status_code == 200:
            soup = bs(resp.content, "html.parser")
            main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
            if main_div:
                div_list = main_div.find_all('div', attrs={"class": "vacancy-serp-item"})
                for div in div_list:
                    title = div.find('a', attrs={"class": "bloko-link"}).contents[0]
                    href = div.a['href']
                    description = div.find('div', attrs={"class": "bloko-text_no-top-indent"}).text
                    company_name = div.find('a', attrs={"class": "bloko-link_secondary"}).contents[0]
                    im = div.find('img')
                    if im:
                        company_name = im.attrs['alt']
                    jobs.append({"url": href,
                                 "title": title,
                                 "company": company_name,
                                 "description": description,
                                 "city_id": city,
                                 "language_id": language})
            else:
                errors.append({'url': uri, 'title': 'Div do not exists'})
        else:
            errors.append({'url': uri,
                           'title': f'Page does not response. Status code: {resp.status_code}'})
    return jobs, errors


def superjob(uri, city=None, language=None):
    if uri:
        resp = requests.get(uri, headers=headers[randint(0,2)])
        jobs = []
        errors = []
        domain = 'https://www.superjob.ru/'
        if resp.status_code == 200:
            soup = bs(resp.content, "html.parser")
            main_div = soup.find('div', attrs={'class': '_1ID8B'})
            if main_div:
                div_list = main_div.find_all('div', attrs={"class": "Fo44F"})
                for div in div_list:
                    href = div.a['href']
                    title = div.find('a', attrs={"class": "icMQ_"}).text
                    description = div.find('span', attrs={"class": "_38T7m"}).text

                    if div.find('a', attrs={"class": "_205Zx"}):
                        company_name = div.find('a', attrs={"class": "_205Zx"}).text
                    else:
                        company_name = "No name"
                    im = div.find('img')
                    if im:
                        company_name = im.attrs['alt']
                    jobs.append({"url": domain+href,
                                 "title": title,
                                 "company": company_name,
                                 "description": description,
                                 "city_id": city,
                                 "language_id": language})
            else:
                errors.append({'url': uri, 'title': 'Div do not exists'})
        else:
            errors.append({'url': uri,
                           'title': f'Page does not response. Status code: {resp.status_code}'})
    return jobs, errors


if __name__ == '__main__':
    uri = 'https://www.superjob.ru/vacancy/search/?keywords=Python'
    jobs, errors = superjob(uri)
    with codecs.open('work.txt', 'w', 'utf-8') as h:
        for jb in jobs:
            h.write(str(jb) + "\n")
