from django.db import models
from django.utils import timezone


class Provider(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Movie(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)

    title = models.CharField(max_length=255)
    movie_page_url = models.CharField(max_length=1024)
    image_url = models.CharField(max_length=1024)
    duration = models.CharField(max_length=255)
    rating = models.CharField(max_length=255)
    year = models.IntegerField()
    country = models.CharField(max_length=255)
    additional_info = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
