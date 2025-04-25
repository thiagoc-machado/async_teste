from celery import shared_task
import requests

@shared_task
def get_pokemon(pokemon_name):
    if not pokemon_name:
        return {'error': 'No Pokemon name provided'}
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if response.status_code == 200:
        return response.json()
    return {'error': 'Pokemon not found'}
