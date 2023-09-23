from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(255), nullable=False)  # Renamed 'name' to 'plant_name'
    image = db.Column(db.String(255))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    
