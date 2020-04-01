#! usr/bin/python3

#region # Import 
from flask import Flask, render_template, request,jsonify
# from flask_mysqldb import MySQL #TODO trouver pourquoi l'installation ne fonctionne pas
from pymongo import MongoClient
from flask_pymongo import PyMongo 
import mysql.connector
import random

#endregion#

#region # Database information

hostname = 'localhost'
username = 'root'
password = 'root'
database = 'flask_DB'
collection = "users"
#endregion#

#region # APP

app = Flask(__name__,template_folder="templates")
app.config["MONGO_URI"] = "mongodb://localhost:27017/{db}".format(db=database)
app.config['MONGO_DBNAME'] = collection
app.config['SECRET_KEY'] = 'secret_key'

client = MongoClient() #NOSQL
mongo = PyMongo(app)

db=client[database]
db = mongo.db
col = mongo.db[collection]

#region# Fonction APP
@app.route('/')
def hello_World():
    hello = "Hello World !"
    message = "Voici un exercice demander par Louis Kuhn"
    return render_template("home.html", 
        hello = hello,
        message = message,
        signature="Produit par Jhy",
        link ="Intro Flask/templates/cv.html",cv="cv")

@app.route('/CV')
def CV():
    return render_template('cv.html')

@app.route('/formulaire')
def formulaire():
    return render_template("formulaire.html")

@app.route('/formulaire',methods=['POST'])
def formulaire_post():
    
    sexe = request.form['sexe'].upper() #TODO ne dois pas tomber sur un vicieux ... doit retravailler et comparer directement sexe et sexe_list
    if sexe == "":
        sexe = request.form['sexe_list'].upper()
        if "H" in sexe:
            titre = 'Mr'
        elif "F" in sexe:
            titre ="Ms"
        else :
            titre = "The Appache Helicoptere"
    elif "M" in sexe:
        titre = 'Mr'
    elif "F" in sexe:
        titre ="Ms"
    else :
        titre = "The Appache Helicoptere"

    prenom = request.form['prenom']
    nom = request.form['nom']
    pseudo = request.form['pseudo']
    
    return render_template("formulaire.html",titre=titre, prenom=prenom,nom=nom,pseudo=pseudo)


@app.route('/formulaire-NOSQL')
def formulaire_NOSQL():
    return render_template("formulaire database.html")

@app.route('/formulaire-NOSQL',methods=['POST'])
def formulaire_post_NOSQL():

    sexe = request.form['sexe_list']
    if sexe == "Homme":
        titre = "Mr"
    elif sexe =="Femme":
        titre = "Ms"
    else :
        titre = "The Appache Helicoptere"
    
    prenom = request.form['prenom']
    nom = request.form['nom']
    pseudo = request.form['pseudo']
    #TODO Vérifier que l'username est libre

    pseudo_take = mongo.db.users.posts.find_one({"_id": pseudo})

    if pseudo_take is None :
        reg_id = mongo.db.users.insert(
            {
                '_id': pseudo,
                'Genre': titre,
                'Nom': nom,
                'Prenom': prenom,
            })
    else : 
        pseudo = pseudo +'0'
        reg_id = mongo.db.users.insert(
            {
                '_id': pseudo,
                'Genre': titre,
                'Nom': nom,
                'Prenom': prenom,
            })
    
    return render_template("formulaire database.html",titre=titre, prenom=prenom,nom=nom,pseudo=pseudo)
    client.close()

@app.route('/formulaire-SQL')
def formulaire_SQL():
#TODO inserer version SQL
    return render_template("formulaire database.html")
    #myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database ) #SQL
    #myConnection.close()

@app.route('/formulaire-SQL',methods=['POST'])
def formulaire_post_SQL():

    sexe = request.form['sexe_list']
    if sexe == "Homme":
        titre = "Mr"
    elif sexe =="Femme":
        titre = "Ms"
    else :
        titre = "The Appache Helicoptere"
    
    prenom = request.form['prenom']
    nom = request.form['nom']
    pseudo = request.form['pseudo']

    return render_template("formulaire database.html",titre=titre, prenom=prenom,nom=nom,pseudo=pseudo)

#endregion#

#region# Launch APP

if __name__ == '__main__':
    app.run(debug=True)

"""
    research = users.find_one({'_id':reg_id})
    output = ({
            'Nom':nom,
            'Prenom':prenom,
            'Genre':titre,
            'Pseudo':pseudo
            })
"""