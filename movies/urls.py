from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>', views.single_movie, name='single_movie'),
    path('parse', views.parse, name='parse'),
]
