#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        # Index Route - GET /plants
        plants = Plant.query.all()
        plant_list = [{
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": float(plant.price)
        } for plant in plants]
        return jsonify(plant_list)

    def post(self):
        # Create Route - POST /plants
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if name is None or price is None:
            return jsonify({"error": "Missing name or price"}), 400

        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()

        return jsonify({
            "id": plant.id,
            "name": plant.name,
            "image": plant.image,
            "price": float(plant.price)
        }), 201

class PlantByID(Resource):
    def get(self, id):
        # Show Route - GET /plants/:id
        plant = Plant.query.get(id)
        if plant:
            return jsonify({
                "id": plant.id,
                "name": plant.name,
                "image": plant.image,
                "price": float(plant.price)
            })
        else:
            return jsonify({"error": "Plant not found"}), 404

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
