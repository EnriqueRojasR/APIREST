from flask import Flask 
from flask_pymongo import PyMongo


app = Flask (__name__)

#Conectamos a la base de datos
app.config['MONGO_URI']='mongodb://localhost/Pokemon'

mongo = PyMongo(app)

@app.route('/pokemons', methods=['POST'])
def create_pokemon():
    #Receiving data
     
    return {'message': 'received'}



if __name__ == "_main_":
    app.run(debug= True)
