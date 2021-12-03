import asyncio
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

pth = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(pth)
os.environ["DJANGO_SETTINGS_MODULE"] = "scrapping_service.settings"
import django


django.setup()


from scraping.work import *
# import codecs
from scraping.models import Vacancy, City, Language, Error, Url


user = get_user_model()

parsers = ((hh, 'hh'),
           (superjob, 'superjob'))
jobs, errors = [], []


def get_settings():
    qs = user.objects.filter(send_email = True).values()
    settings_ls = set((q['city_id'], q['language_id']) for q in qs)
    return settings_ls


def get_url(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.append(err)
    jobs.extend(job)

settings = get_settings()
url_list = get_url(settings)

#city = City.objects.filter(slug='moskva').first()
#language = Language.objects.filter(slug='python').first()



#loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
            for data in url_list
            for func, key in parsers
            ]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])


#for data in url_list:
#    for func, key in parsers:
#        url = data['url_data'][key]
#        j, e = func(url, city=data['city'], language=data['language'])
#        jobs += j
#        errors += e

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# if __name__ == '__main__':
#    with codecs.open('work.txt', 'w', 'utf-8') as h:
#        for jb in jobs:
#            h.write(str(jb) + "\n")
