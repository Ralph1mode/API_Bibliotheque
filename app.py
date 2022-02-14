from asyncio import Task
from logging import exception
from warnings import catch_warnings
from click import Abort
from flask_cors import CORS, cross_origin
import os
from os import abort
from requests import get
import unicodedata
import psycopg2
# importer Flask
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy  # importer SQLAlchemy
#import urllib.parse
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import ForeignKey, PrimaryKeyConstraint, null  # permet d'importer les variables d'environnement
load_dotenv()
#from flask_migrate import Migrate
# Define the create_app function
#def create_app(test_config=None):
# Create and configure the app
# Include the first parameter: Here, __name__is the name of the current Python module.
app = Flask(__name__)
motdepasse = os.getenv('pgpswrd')
db = SQLAlchemy(app)
try:
    

    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bhceeviwjcmfuq:9182a080516ae80750fb23906eec3887fe90778e537efe0736d289a4c81caccb@ec2-54-83-21-198.compute-1.amazonaws.com:5432/ddiel034eulo7q"
# connexion à la base de données
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    class Categorie(db.Model):
        __tablename__ = 'categorie'
        id_cat = db.Column(db.Integer, primary_key=True)
        libelle_cat = db.Column(db.String(200))
        livres = db.relationship('Livre', backref='categorie', lazy=True)
 
        def __init__(self,libelle_cat):
            self.libelle_cat = libelle_cat

        def insert(self):
            db.session.add(self)
            db.session.commit()
    
        def update(self):
            db.session.commit()

        def delete(self):
            db.session.delete(self)
            db.session.commit()

        def format(self):
            return {
                'id_cat': self.id_cat,
                'libelle_cat': self.libelle_cat,
             
            }
        
    db.create_all()



    class Livre(db.Model):
        __tablename__ = 'livres'
        id = db.Column(db.Integer, primary_key=True)
        isnb = db.Column(db.String(10), nullable=False)
        titre = db.Column(db.String(200), nullable=False)
        nom_aut = db.Column(db.String(50))
        date_pub = db.Column(db.Date())
        editeur = db.Column(db.String(60), nullable=False)
        categorie_id = db.Column(db.Integer, ForeignKey("categorie.id_cat"), nullable=False)
        
        def __init__(self,titre, nom_aut, date_pub, categorie_id, editeur,isnb):
            self.isnb = isnb
            self.titre = titre
            self.nom_aut = nom_aut
            self.date_pub = date_pub
            self.categorie_id = categorie_id
            self.editeur = editeur

        def insert(self):
            db.session.add(self)
            db.session.commit()
    
        def update(self):
            db.session.commit()

        def delete(self):
            db.session.delete(self)
            db.session.commit()
        
        
        def format(self):
            return {
                'id': self.id,
                'isbn': self.isnb,
                'titre': self.titre,
                'editeur':self.editeur,
                'nom_aut': self.nom_aut,
                'date_pub': self.date_pub,
                'categorie_id':self.categorie_id,
            }
    db.create_all()


    @app.route('/')
    def index():
        return "Bienvenu sur LIBRARY notre API de gestion de bibliothèque" #render_template("index.html")

    #################################################
    #           Liste des livres
    #################################################
    def paginate(request):
        items = [item.format() for item in request]
        return items
    
    @app.route('/livres')
    def get_all_livre():
        livres = Livre.query.all()
        livres =  paginate(livres)
        return jsonify(
            {
                'success': True,
                'Livres': livres,
                'nombre': len(livres)
            })

    #################################################
    #           Liste des Categories
    #################################################
    @app.route('/categorie')
    def get_all_categorie():
        categorie = Categorie.query.all()
        categorie = paginate(categorie)
        return jsonify(
            {
                'success': True,
                #'Identifiant': id_cat,
                'Catégorie':categorie,
                'nombre': len(categorie)}
        )

    #################################################
    #           selectioner un livre par id
    #################################################

    @app.route('/livre/<int:id>')
    def get_one_livre(id):
        try:
            
            livre = Livre.query.get(id)
            if livre is None:
                abort(404)
            else:
                return livre.format()                 

        except: abort(400)

    #################################################
    #           selectioner une catégorie par id
    #################################################
    @app.route('/categorie/<int:id_cat>')
    def get_one_categorie(id_cat):
        try: 
            categorie = Categorie.query.get(id_cat)
            if categorie is None:
                abort(404)
            else:
                return jsonify({
                    'success':True,
                    'Numero':id_cat,
                    'Categorie':categorie.format()
                })
        except: abort(400)
 
    #################################################
    #     livres par categorie
    #################################################
    @app.route('/livre/cat/<int:id>')
    def livre_par_catego(id):
        try:
                categorie = Categorie.query.get(id)
                livre = Livre.query.filter_by(categorie_id=id).all()
                livre =  paginate(livre)
            
                return jsonify({
                            'success':True,
                            'Statut code':200,
                            'class': categorie.format(),
                            'livre':livre
                        })
        except: abort(400)
        finally:
            db.session.close()


    ############################
    # Supprimer un livre
    ############################

    @app.route('/suppr_livre/<int:id>', methods=['DELETE'])
    def supp_livre(id):
        try:
            livre = Livre.query.get(id)
            #if livre in None:
             #   abort(404)
            #else:
            livre.delete()
            return jsonify({
                    'success': True,
                    'id': id,
                    'Livre':livre.format(),
                    'new_total': Livre.query.count()
                })
        except:
            abort(404)
        finally:
            db.session.close()


    ################################
    # Supprimer une categorie 
    ################################

    @app.route('/suppr_cat/<int:id_cat>', methods=['DELETE'])
    def suppr_categorie(id_cat):
        try:
            categorie = Categorie.query.get(id_cat)
            categorie.delete()
            return jsonify({
                    'success': True,
                    'id_livre': id_cat,
                    'Categorie':categorie.format(),
                    'new_total': Categorie.query.count()
                })
        except:
            abort(404)
        finally:
            db.session.close()
        

    ##################################################
    # Rechercher un livre par son auteur
    ##################################################
    @app.route('/rech_livre/<string:titre>')
    def search_book(titre):
        mot = '%'+titre+'%'
        titre = Livre.query.filter(Livre.nom_aut.like(mot)).all()
        titre = paginate(titre)
        return jsonify({
            'Livres': titre
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Ressource non disponible"
        }), 404


        #return app
    ###########################################
    # Modifier les informations d'un livre
    ###########################################

    @app.route('/livre/<int:id>', methods=['PATCH'])
    def change_book(id):
        body = request.get_json()
        livres = Livre.query.get(id)
        try:
            if 'titre' in body and 'nom_aut' in body and 'editeur' in body:
                livres.titre = body['titre']
                livres.nom_aut = body['nom_aut']
                livres.editeur = body['editeur']
            livres.update()
            return livres.format()
        except:
            abort(404)
            
       
    ##########################################################################
    ##           Ajouter Une nouvelle catégorie 
    ##########################################################################
    @app.route('/categorie',methods=['POST'])
    def add_catgeory():
        recup=request.get_json()
        try:
            newlibelle=recup.get('libelle_cat',None)
            ca=Categorie(libelle_cat=newlibelle)
            try:
                ca.insert()
                categorie=Categorie.query.all()
                categorie=[d.formatage() for d in categorie]
                return jsonify({
                    'success':True,
                    'Categories':categorie,
                    'Count': len(categorie)}
                )
            except:abort(404)
        except:abort(400)

    #################################################################
    ##          Pour Ajouter Un Livre aux livres déjà existants.
    #################################################################
    @app.route('/livre',methods=['POST'])
    def add_book():
        aj=request.get_json()
        try:
            new_isbn=aj.get('isbn',None)
            new_datepublication=aj.get('date_pub',None)
            new_titre=aj.get('titre',None)
            new_editeur=aj.get('editeur',None)
            new_auteur=aj.get('nom_aut',None)
            new_categorie_id=aj.get('categorie_id',None)
            maxcat=Categorie.query.count()
            if new_categorie_id >  maxcat:
                abort(500)
            else:
                livvre=Livre(isbn=new_isbn, auteur=new_auteur, date_publication=new_datepublication,
                editeur=new_editeur,titre=new_titre,categories_id=new_categorie_id)
                livvre.insert()
                books=Livre.query.all()
                books=[l.format() for l in books]

            return jsonify({
                'success':True,
                'Livres':books,
                'Compte':len(books)}
            )
        except:
            abort(404)

    
    ########################################
    # Modifier le libellé d'une categorie
    ########################################

    @app.route('/categorie/<int:id>', methods=['PATCH'])
    def change_name(id):
        body = request.get_json() 
        categorie = Categorie.query.get(id)
        try:
            if 'libelle_cat' in body:
                categorie.libelle_cat = body['libelle_cat']
            categorie.update()
            return categorie.format()
        except:
            abort(404)

    #ici on fait un get et la ressource 
    #n'existe pas http://localhost:5000/persons/200
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404
        
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal server error"
            }), 500
        
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad Request"
            }), 400

    if __name__ == '__main__':
        app.run(debug=True)
        print("API START")
        
except(Exception, psycopg2.Error) as error:
    print("Erreur : ", error) 

