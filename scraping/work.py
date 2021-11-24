import requests
import codecs
from bs4 import BeautifulSoup as bs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,applicaition/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }
url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python'


def hh(uri):
    resp = requests.get(uri, headers=headers)
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
                ds = div.find_all('div', attrs={"class": ""})
                if len(ds) == 4 in ds:
                    description = ds[2].get_text() + " " + ds[3].get_text()
                else:
                    description = ds[2].get_text()
                company_name = div.find('a', attrs={"class": "bloko-link_secondary"}).contents[0]
                company_logo = "No logo"
                im = div.find('img')
                if im:
                    company_logo = im.attrs['src']
                    company_name = im.attrs['alt']
                jobs.append({"title": title,
                            "url": href,
                             "descrition": description,
                             "company": company_name,
                             "company_logo": company_logo})
        else:
            errors.append({'url': url, 'title': 'Div do not exists'})
    else:
        errors.append({'url': url,
                       'title': f'Page does not response. Status code: {resp.status_code}'})
    return jobs, errors


def superjob(uri):
    resp = requests.get(uri, headers=headers)
    jobs = []
    errors = []
    domain = 'https://www.superjob.ru'
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
                company_logo = "No logo"
                im = div.find('img')
                if im:
                    company_logo = im.attrs['src']
                    company_name = im.attrs['alt']
                jobs.append({"title": title,
                            "url": domain + href,
                             "descrition": description,
                             "company": company_name,
                             "company_logo": company_logo})
        else:
            errors.append({'url': url, 'title': 'Div do not exists'})
    else:
        errors.append({'url': url,
                       'title': f'Page does not response. Status code: {resp.status_code}'})
    return jobs, errors


if __name__ == '__main__':
    uri = 'https://www.superjob.ru/vacancy/search/?keywords=Python'
    jobs, errors = superjob(uri)
    with codecs.open('work.txt', 'w', 'utf-8') as h:
        for jb in jobs:
            h.write(str(jb) + "\n")
