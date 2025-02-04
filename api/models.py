from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from movies.models import Provider, Genre, Movie
from .authentication import CustomAuthentication


class ProviderResource(ModelResource):
    class Meta:
        queryset = Provider.objects.all()
        resource_name = 'providers'
        allowed_methods = ['get']
        # authentication = ApiKeyAuthentication()
        # authorization = Authorization()


class GenreResource(ModelResource):
    class Meta:
        queryset = Genre.objects.all()
        resource_name = 'genres'
        allowed_methods = ['get']


class MovieResource(ModelResource):
    class Meta:
        queryset = Movie.objects.all()
        resource_name = 'movies'
        allowed_methods = ['get', 'post', 'delete']
        excludes = ['created', 'movie_page_url']
        authentication = CustomAuthentication()
        authorization = Authorization()

    def hydrate(self, bundle):
        bundle.obj.provider_id = bundle.data['provider_id']
        return bundle
        # return super().hydrate(bundle)

    def dehydrate(self, bundle):
        bundle.data['provider_name'] = bundle.obj.provider
        bundle.data['genres'] = [
            genre.name for genre in bundle.obj.genre.all()]
        return bundle
        # return super().dehydrate(bundle)

    def dehydrate_country(self, bundle):
        return bundle.data['country'].upper()
