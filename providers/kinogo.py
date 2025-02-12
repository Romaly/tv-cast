from bs4 import BeautifulSoup
import requests
import random
from providers import user_agents
import traceback

PROVIDER_NAME = 'kinogo.online'
BASE_URL = 'https://kinogo.online'
MAX_PAGE = 8369

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '__ddg1_=aEwkxf6yvUT3C9y3JaoK; PHPSESSID=f213d2f792c2d2012420fb4b8272bda2',
    'priority': 'u=0, i',
    'referer': 'https://kinogo.online/page/4/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}


def parse_movies(data_call_back, maxPage=MAX_PAGE):
    counter = 0
    for page_number in range(1, maxPage+1):
        random_user_agent = random.choice(user_agents.user_agents_list)
        print(random_user_agent)

        url_to_parse = f"{BASE_URL}/page/{page_number}"

        headers['User-Agent'] = random_user_agent
        headers['referer'] = url_to_parse  # f"{BASE_URL}/page/{page_number}"

        resp = requests.get(url_to_parse, headers=headers).text

        page = BeautifulSoup(resp, 'lxml')

        for el in page.find_all('article', class_='shortStory'):
            try:
                film_info = {'provider': PROVIDER_NAME}

                title_node = el.find('div', class_='hTitle').find('a')
                title = title_node['title']

                year = title[-6: len(title)]
                if (year.count('(') and year.count(')')):
                    title = title.replace(year, '').strip()

                film_info['title'] = title
                film_info['movie_page_url'] = title_node['href']

                try:
                    rating = el.find('span', class_='ratingStats')
                    film_info['rating'] = rating.text
                except:
                    film_info['rating'] = ''

                poster = el.find('div', class_='sPoster').find('a').find('img')
                film_info['image_url'] = BASE_URL + poster['data-src']

                info = el.find('div', class_='sInfo')

                try:
                    film_info['year'] = info.find(
                        lambda tag: tag.name == "span" and 'Год выпуска:' in tag.text).find('a').text
                except:
                    film_info['year'] = ''

                try:
                    film_info['country'] = info.find(
                        lambda tag: tag.name == "span" and 'Страна:' in tag.text).find('a').text
                except:
                    film_info['country'] = ''

                try:
                    film_info['genre'] = [item.text.strip() for item in info.find(
                        lambda tag: tag.name == "span" and 'Жанр:' in tag.text).find_all('a')]
                except:
                    film_info['genre'] = ''

                try:
                    duration = info.find(
                        lambda tag: tag.name == "span" and 'Продолжительность:' in tag.text).text
                    film_info['duration'] = duration.replace(
                        'Продолжительность:', '').strip()

                except:
                    film_info['duration'] = ''

                try:
                    film_info['additional_info'] = info.find(
                        lambda tag: tag.name == "span" and 'Премьера (РФ):' in tag.text).text
                except:
                    film_info['additional_info'] = ''

                info_item = el.find('p', class_='excerpt')
                film_info['description'] = info_item.text

                counter += 1
                # print(f'{page_number+1}:{counter}: {film_info['title']}')

                data_call_back(film_info, page_number, counter)

            except Exception as ex:
                ex.with_traceback = True
                print(ex)
                traceback.print_exc()
