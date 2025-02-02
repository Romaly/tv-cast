from pathlib import Path
import shutil
from bs4 import BeautifulSoup
import requests
import random
import json
import os
import time

timer_start = time.time()


MAX_PAGE = 8369

img_dir = Path('images')
if not img_dir.exists():
    img_dir.mkdir()

# url = 'https://kinogo.online//uploads/mini/shortstory/a3/4eaebfaa490072f7cdf82a3ac9c9c5.jpg'
# response = requests.get(url, stream=True)
# with open('img.jpg', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)
# del response


def downloadImage(url):
    response = requests.get(url, stream=True)
    with open(img_dir / os.path.basename(url), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


user_agents_list = [
    # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/62.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.1; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 YaBrowser/20.12.2.105 Yowser/2.5 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
]

counter = 0
movies_list = []
for page_number in range(MAX_PAGE):
    random_user_agent = random.choice(user_agents_list)
    print(random_user_agent)

    headers = {
        'User-Agent': random_user_agent
    }

    base_url = 'https://kinogo.online'
    url_to_parse = f"{base_url}/page/{page_number+1}"

    resp = requests.get(url_to_parse, headers=headers).text

    page = BeautifulSoup(resp, 'lxml')

    for el in page.find_all('article', class_='shortStory'):
        try:
            film_info = {}

            title = el.find('div', class_='hTitle').find('a')
            film_info['number'] = counter
            film_info['page'] = page_number
            film_info['title'] = title['title']
            film_info['href_movie'] = title['href']

            rating = el.find('span', class_='ratingStats')
            film_info['rating'] = rating.text

            poster = el.find('div', class_='sPoster').find('a').find('img')
            film_info['image_url'] = url_to_parse + poster['data-src']
            downloadImage(base_url + poster['data-src'])

            info_item = el.find('div', class_='sInfo').find_all('span')
            film_info['year'] = info_item[0].find('a').text
            film_info['country'] = info_item[1].find('a').text
            film_info['genre'] = [item.text.strip()
                                  for item in info_item[2].find_all('a')]
            film_info['duration'] = info_item[3].text
            film_info['additional_info'] = info_item[4].text

            info_item = el.find('p', class_='excerpt')
            film_info['description'] = info_item.text

            movies_list.append(film_info)
            # print(film_info)

            counter += 1
            print(f'{page_number+1}:{counter}: {film_info['title']}')

        except Exception as ex:
            print(ex)

    elapsed_time = time.time() - timer_start
    print(f'Elapsed: {elapsed_time:.2f} sec.')

    try:
        json_str = json.dumps(movies_list, indent=3)

        with open('movies.json', 'w') as file:
            file.write(json_str)
    except ex:
        print(ex)

print('Done...')
