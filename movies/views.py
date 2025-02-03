from django.shortcuts import render
from django.http import HttpResponse
from providers import kinogo
import time
from .models import Provider, Movie

# Create your views here.


def index(request):
    print('test')
    return HttpResponse("test appp")


def list(request):
    m = Movie.objects.all()
    # print([m.title for m in Movie.objects.all()])
    # return HttpResponse([f'{m.title}<br>' for m in Movie.objects.all()])

    return render(request, 'movies_list.html', {'movies': m})


def parse(request):
    def data_call_back(film_info, page_number, counter):
        film_info['provider'] = Provider.objects.get(name='kinogo.online')
        print(f'{page_number}:{counter}: {film_info['title']}')
        Movie(**film_info).save()

    start_time = time.time()
    kinogo.parse_movies(data_call_back, 4)

    return HttpResponse(f'Parese finished, elapsed time: {(time.time() - start_time):.2f} sec')
