from django.contrib import admin
from . import models

admin.site.site_header = "Панель администратора"
admin.site.site_title = "Администратор"
admin.site.index_title = "Редактор таблиц"


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    exclude = ['created']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    exclude = ['created']


class MoviesAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'duration', 'country')
    exclude = ['created']


admin.site.register(models.Provider, ProviderAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Movie, MoviesAdmin)
