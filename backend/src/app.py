from flask import Flask, request, jsonify
from flask_pymongo import pymongo, ObjectId
from flask_cors import CORS

app= Flask(__name__)

CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0-ofrwn.mongodb.net/test?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('reactmongo')
user_collection = pymongo.collection.Collection(db, 'persona')

CORS(app)

@app.route('/')
def index():
    return "flask mongodb atlas!"

@app.route("/users", methods=["POST"])
def createUser():
    id = db.users.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    print(str(ObjectId(id)))
    #respuesta con el ID creado
    return jsonify(str(ObjectId(id)))

@app.route("/users", methods=["GET"])
def getUsers():
    users = []
    for doc in db.users.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route("/users/<id>", methods=["GET"])
def getUser(id):
    user = db.users.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']

    })

@app.route("/users/<id>", methods=["DELETE"])
def deleteUser(id):
    user = db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({
        'msg': 'el usuario ha sido eliminado'
    })

    return "Connected to the data base!"

@app.route("/users/<id>", methods=["PUT"])
def updateUser(id):
    user = db.users.update_one({'_id': ObjectId(id)},
    {'$set':{
            'name': request.json['name'],
            'email': request.json['email'],
            'password': request.json['password']        
    }})
    return "Usuario actualizado"

if __name__ == '__main__': 
    app.run(debug=True)

