from flask import Flask, request, jsonify
import requests
import random
import logging

from autenticacao import Autenticador

autenticador = Autenticador()

app = Flask(__name__)


# Obtener el tipo de un Pokémon (fuego, agua, tierra, aire, etc…) según su nombre.
@app.route('/pokemon/tipo/<nome>', methods=['GET'])
def obter_tipo_pokemon(nome):

    #  Llamada a la API de Poké para obtener detalles de Pokémon
    url = f'https://pokeapi.co/api/v2/pokemon/{nome.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        tipo_pokemon = response.json()['types'][0]['type']['name']
        logging.warning('Tipo Pokemón ok')
        return jsonify({'nome': nome, 'tipo': tipo_pokemon})
    else:
        return jsonify({'erro': 'Pokemon no encontrado'}), 404


# Obtener un Pokémon al azar de un tipo en específico
@app.route('/pokemon/aleatorio/<tipo>', methods=['GET'])
def obter_pokemon_aleatorio(tipo):

    # Fazer uma chamada à API Poké para obter um Pokémon aleatório do tipo especificado
    url = f'https://pokeapi.co/api/v2/type/{tipo.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        pokemons_do_tipo = response.json()['pokemon']
        pokemon_aleatorio = pokemons_do_tipo[0]['pokemon']['name']
        return jsonify({'tipo': tipo, 'pokemon_aleatorio': pokemon_aleatorio})
    else:
        return jsonify({'erro': 'Tipo de Pokémon não encontrado'}), 404


# Obtener el Pokémon con nombre más largo de cierto tipo
@app.route('/pokemon/mais-longo/<tipo>', methods=['GET'])
def obter_pokemon_mais_longo(tipo):
    #  Llamada a la API de Poké para obtener detalles de Pokémon del tipo especificado
    url = f'https://pokeapi.co/api/v2/type/{tipo.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        pokemons_do_tipo = response.json()['pokemon']
        pokemon_mais_longo = max(pokemons_do_tipo, key=lambda x: len(x['pokemon']['name']))
        return jsonify({'tipo': tipo, 'pokemon_mais_longo': pokemon_mais_longo['pokemon']['name']})
    else:
        return jsonify({'erro': 'Tipo de Pokémon no encontrado'}), 404


# Endpoint para obter um Pokémon aleatório com letras específicas e tipo mais forte com base no clima
@app.route('/pokemon/letras-e-clima/<int:temperatura_atual>', methods=['GET'])
def obter_pokemon_letras_e_clima(temperatura_atual):

    # Lógica para identificar qué tipo de Pokémon se basa en la temperatura
    if temperatura_atual >= 30:
        tipo_mais_forte = 'fire'
    elif 20 <= temperatura_atual < 30:
        tipo_mais_forte = 'ground'
    elif 10 <= temperatura_atual < 20:
        tipo_mais_forte = 'normal'
    elif temperatura_atual < 0:
        tipo_mais_forte = 'ice'
    else:
        tipo_mais_forte = 'water'

    # Fazer uma chamada à API Poké para obter um Pokémon aleatório com letras específicas e tipo mais forte
    url = f'https://pokeapi.co/api/v2/type/{tipo_mais_forte.lower()}'
    response = requests.get(url)

    if response.status_code == 200:
        pokemons_do_tipo = response.json()['pokemon']

        # Filtrar Pokémon que contenham a letra especificada em seu nome
        pokemons_filtrados = [p['pokemon']['name'] for p in pokemons_do_tipo
                              if any(letra in p['pokemon']['name'].lower() for letra in ['i', 'a', 'm'])]

        if pokemons_filtrados:
            # Selecionar aleatoriamente um Pokémon da lista filtrada
            pokemon_aleatorio = random.choice(pokemons_filtrados)
            return jsonify({'tipo_mais_forte': tipo_mais_forte, 'pokemon_aleatorio': pokemon_aleatorio})
        else:
            return jsonify({'erro': 'Nenhum Pokémon encontrado com a letra especificada'}), 404
    else:
        return jsonify({'erro': 'Tipo de Pokémon mais forte não encontrado'}), 404


# Middleware para la autenticación
@app.before_request
def autenticar():
    if request.endpoint not in ['verificar_autenticacao']:
        if not autenticador.verificar_autenticacao():
            return jsonify({'erro': 'Error de autenticación'}), 401


# Ejecutar aplicación con debug
if __name__ == '__main__':
    app.run(debug=True)
