
from django.shortcuts import render
from django.http import JsonResponse
from .service import get_pokemon as get_pokemon_service
from django.views import View
from django.http import HttpResponse

class PokemonService(View):
    def get(self, request):
        pokemon_name = request.GET.get('name')  # ex: ?name=pikachu
        get_pokemon_service.delay(pokemon_name)

        return HttpResponse(
            f"Pokemon {pokemon_name} is being fetched asynchronously."
        )