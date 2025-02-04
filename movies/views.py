from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from providers import kinogo
import time
from .models import Provider, Genre, Movie

# Create your views here.


def index(request):
    movies = Movie.objects.all()
    # print([m.title for m in Movie.objects.all()])
    # return HttpResponse([f'{m.title}<br>' for m in Movie.objects.all()])

    return render(request, 'movies/movies_list.html', {'movies': movies})


def single_movie(request, movie_id):
    # try:
    #     movie = Movie.objects.get(pk=movie_id)
    #     return render(request, 'movie_info.html', {'movie': movie})
    # except Movie.DoesNotExist:
    #     raise Http404()

    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movies/movie_info.html', {'movie': movie})


def parse(request):
    kinogo_provider = Provider.objects.get(name='kinogo.online')

    def data_call_back(film_info, page_number, counter):
        if Movie.objects.filter(title=film_info['title'], year=film_info['year'], provider=kinogo_provider).first():
            return

        genres_list = []
        for g in film_info['genre']:
            genre = Genre.objects.filter(name=g.strip()).first()
            if not genre:
                genre = Genre(name=g)
                genre.save()
            genres_list.append(genre)

        film_info['provider'] = kinogo_provider
        del film_info['genre']
        print(f'{page_number}:{counter}: {film_info['title']} {genres_list}')

        movie = Movie(**film_info)
        movie.save()

        for genre in genres_list:
            movie.genre.add(genre)

    start_time = time.time()
    kinogo.parse_movies(data_call_back, 10)

    return HttpResponse(f'Parese finished, elapsed time: {(time.time() - start_time):.2f} sec')
