
from django.contrib import admin
from django.urls import path
from .views import PokemonService

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PokemonService.as_view(), name='pokemon_service'),
]
