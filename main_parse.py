from providers import kinogo
import time
import data_store
import requests


print('qwerty'.replace('qwe', ''))


data_store.init()


def data_call_back(film_info, page_number, counter):
    data_store.insert(**film_info)
    print(f'{page_number}:{counter}: {film_info['title']}')


start_time = time.time()
# kinogo.parse_movies(data_call_back, 4)
res_movies = data_store.find_by_title('', 3, 3)
print(res_movies)

print()
print(f'Elapsed time: {(time.time() - start_time):.2f} sec')


print('Done...')
