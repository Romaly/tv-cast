from api.models import ProviderResource, GenreResource, MovieResource
from tastypie.api import Api
from django.urls import path, include

# Headers
# key:   'Authorization'
# value: 'ApiKey admin:qwerty123456'

api = Api(api_name='v1')
api.register(ProviderResource())
api.register(GenreResource())
api.register(MovieResource())

urlpatterns = [
    path('', include(api.urls), name='index')
]
