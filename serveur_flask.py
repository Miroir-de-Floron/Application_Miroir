from flask import Flask, request
from Model.models import db, Tag

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Tag.db'
db.init_app(app)

@app.route('/recevoir', methods=['GET'])

#fonction qui reçoit les données de l'arduino et les enregistre dans la base de données ou change l'état d"une ligne si elle existe déja
def recu_de_donnee():
    nom = int(request.args.get('nom'))
    etat = True
    print("Données reçues depuis Arduino - Nom : {}, État : {}".format(nom, etat))

    #si il y'a un nom identique dans la base de données, on ne crée pas de nouvelle ligne 
    if Tag.query.filter_by(nom=nom).first() is not None:
        print("deja dans la base de données")
        Tag.query.filter_by(nom=nom).update(dict(etat=etat))
        #on comitte sans ajouter de ligne
        db.session.commit()
        return "Données enregistrées : Nom={}, État={}".format(nom, etat)
    
    #sinon on ajoute une nouvelle ligne
    tag = Tag(nom=nom, etat=etat)
    db.session.add(tag)
    db.session.commit()

    return "Données enregistrées : Nom={}, État={}".format(nom, etat)

if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0", debug=True)

