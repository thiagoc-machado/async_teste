from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from celery import Celery

# Initialize Celery
app = Celery(
    main='tasks', 
    broker='pyamqp://guest@localhost//',
)

@app.task
def get_pokemon(pokemon_name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    if response.status_code == 200:
        return response.json()