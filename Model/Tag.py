from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tag.db'  
db = SQLAlchemy(app)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Integer)
    etat = db.Column(db.Boolean)

    def __init__(self, nom, etat):
        self.nom = nom
        self.etat = etat

#on crée la base de données
with app.app_context():
    db.create_all()
