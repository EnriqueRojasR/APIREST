from flask import Flask, jsonify, request
from pymongo import MongoClient
import requests

app = Flask(__name__)

# Conexión con MongoDB Atlas
client = MongoClient("mongodb+srv://EnriqueRojas:EnriqueRojas12@apipokemon.zlp2gxc.mongodb.net/?retryWrites=true&w=majority")
db = client["pokedex"]
collection = db["pokemon"]

# Obtener los nombres y ids de todos los Pokémon
@app.route("/pokemon", methods=["GET"])
def get_pokemon():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100")
    if response.ok:
        data = response.json()["results"]
        return jsonify(data)
    else:
        return jsonify({"error": "No se pudo obtener la información de PokéAPI"}), 500

# Obtener la data completa de los Pokémon pasándole como parámetro un id
@app.route("/pokemon/<int:pokemon_id>", methods=["GET"])
def get_pokemon_by_id(pokemon_id):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if response.ok:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "No se pudo obtener la información de PokéAPI"}), 500

# Crear un nuevo Pokémon con toda su información
@app.route("/pokemon", methods=["POST"])
def create_pokemon():
    pokemon = request.json
    result = collection.insert_one(pokemon)
    if result.acknowledged:
        return jsonify({"_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"error": "No se pudo crear el Pokémon"}), 500

# Modificar los atributos de los Pokémon guardados
@app.route("/pokemon/<string:pokemon_id>", methods=["PUT"])
def update_pokemon(pokemon_id):
    pokemon = request.json
    result = collection.update_one({"_id": pokemon_id}, {"$set": pokemon})
    if result.modified_count == 1:
        return jsonify({"message": "Pokémon actualizado correctamente"}), 200
    elif result.matched_count == 1 and result.modified_count == 0:
        return jsonify({"message": "No se realizaron cambios en el Pokémon"}), 200
    else:
        return jsonify({"error": "No se pudo actualizar el Pokémon"}), 500

# Eliminar algún Pokémon
@app.route("/pokemon/<string:pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id):
    result = collection.delete_one({"_id": pokemon_id})
    if result.deleted_count == 1:
        return jsonify({"message": "Pokémon eliminado correctamente"}), 200
    else:
        return jsonify({"error": "No se pudo eliminar el Pokémon"}), 500

if __name__ == "__main__":
    app.run(debug=True) 