# Projeto Django + Celery + RabbitMQ

## Sobre o Projeto
Este projeto utiliza Django para a aplicação principal, Celery para tarefas assíncronas e RabbitMQ como broker de mensagens.

A aplicação consome a API de forma assíncrona para buscar informações nessa api.

---

## Requisitos
- Python 3.10+
- Django 4+
- Celery 5+
- Docker
- RabbitMQ

---

## Instalação

1. **Clone o projeto:**
```bash
https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados e o Django (se necessário):**
```bash
python manage.py migrate
```

---

## Configuração do RabbitMQ com Docker

Para rodar o RabbitMQ usando Docker:

```bash
# RabbitMQ com interface de gerenciamento
# Ports:
# - 5672: Porta de comunicação AMQP (usada pelo Celery)
# - 15672: Interface web para gerenciar RabbitMQ

docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

Acesse a interface do RabbitMQ via navegador:

```
http://localhost:15672/
```
Usuário padrão: `guest`  
Senha padrão: `guest`

---

## Configuração do Celery no Projeto

1. **Crie o arquivo `async_test/celery.py`:**

```python
from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_test.settings')

app = Celery('async_test', broker='pyamqp://guest@localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

2. **Modifique `async_test/__init__.py` para incluir:**

```python
from .celery import app as celery_app

__all__ = ['celery_app']
```

3. **Crie um `tasks.py` no seu app Django (ex: `myapp/tasks.py`):**

```python
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
```

---

## Como Rodar o Projeto

1. **Suba o container do RabbitMQ:**
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4-management
```

2. **Rode o servidor Django:**
```bash
python manage.py runserver
```

3. **Inicie o worker do Celery:**
```bash
celery -A async_test worker --loglevel=info
```

4. **Testar no navegador ou Postman:**

Exemplo de chamada GET:
```
http://localhost:8000/?name=pikachu
```

---

## Observações
- Certifique-se que o Celery está conectado ao RabbitMQ antes de enviar tarefas.
- A versão do RabbitMQ utilizada é a `4-management` para disponibilizar painel de controle web.
- Todas as respostas da busca são processadas de forma assíncrona.

---

## Autor
Thiago Machado

