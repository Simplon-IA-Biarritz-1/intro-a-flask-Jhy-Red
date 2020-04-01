#! usr/bin/python3

#region # Import 
from flask import Flask, render_template, request,jsonify
# from flask_mysqldb import MySQL #TODO trouver pourquoi l'installation ne fonctionne pas
from pymongo import MongoClient
from flask_pymongo import PyMongo 
import mysql.connector
import random
from pandas import read_csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

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
            titre ="Mme"
        else :
            titre = "The Appache Helicoptere"
    elif "M" in sexe:
        titre = 'Mr'
    elif "F" in sexe:
        titre ="Mme"
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
        titre = "Mme"
    else :
        titre = "The Appache Helicoptere"
    
    prenom = request.form['prenom']
    nom = request.form['nom']
    pseudo = request.form['pseudo']
    #TODO Vérifier que l'username est libre

    pseudo_take = mongo.db.users.posts.find_one({"_id": pseudo})

    try :
        if pseudo_take is None :
            reg_id = mongo.db.users.insert_one(
                {
                    '_id': pseudo,
                    'Genre': sexe,
                    'Nom': nom,
                    'Prenom': prenom,
                })

    except :
        return "Ce nom d'utilisateur est déja pris !"

    return render_template("formulaire database.html",titre=titre, prenom=prenom,nom=nom,pseudo=pseudo)
    client.close()

@app.route('/formulaire-SQL')
def formulaire_SQL():
#TODO inserer version SQL
    myConnection = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database ) #SQL
    myConnection.close()
    return render_template("formulaire database.html")

@app.route('/formulaire-SQL',methods=['POST'])
def formulaire_post_SQL():

    sexe = request.form['sexe_list']
    if sexe == "Homme":
        titre = "Mr"
    elif sexe =="Femme":
        titre = "Mme"
    else :
        titre = "The Appache Helicoptere"
    
    prenom = request.form['prenom']
    nom = request.form['nom']
    pseudo = request.form['pseudo']

    return render_template("formulaire database.html",titre=titre, prenom=prenom,nom=nom,pseudo=pseudo)

@app.route('/database',methods=['GET'])
def database_list():
    database = db.users.find({})
    liste = []

    for x in database :
        liste.append(x)
    
    databaselight = db.users.distinct('_id')
    listlight = []

    for x in databaselight :
        listlight.append(x)

    client.close()
    return render_template("database.html",database=liste,databaselight=listlight)

@app.route('/liste_utilisateur',methods=['GET'])
def utilisateurs_list():
    database = db.users.distinct('_id')
    userlist = []

    for x in database :
        userlist.append(x)
    
    client.close()
    return render_template("database.html",database=userlist, databaselight="")

@app.route('/statistique',methods=['GET'])
def statistique():
    longueur = len(list(db.users.distinct('_id')))

    cpt_homme = 0
    cpt_femme = 0

    cursor = db.users.find({})
    for document in cursor: 
        if document['Genre'] == "Homme":
            cpt_homme += 1
        else :
            cpt_femme += 1
    try :
        parite_homme = round(((longueur / cpt_homme) *100))
    except :
        parite_homme = 0
    try :
        parite_femme = round(((longueur / cpt_femme) *100))
    except :
        parite_femme = 0
    parite = (parite_homme,parite_femme)
    
    client.close()
    return render_template("stats.html",longueur=longueur,homme=parite_homme,femme=parite_femme)


@app.route('/mnist')
def mnist():
    online_path="http://www.math.univ-toulouse.fr/~besse/Wikistat/data/"
    data=read_csv(online_path+"mnist_train.csv",header=None)
    Y=data.iloc[:,784] 
    X= data.drop(data.columns[[784]], axis=1,inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X,Y,random=5)

    return "nope, c'était pas pret"
#endregion#

#region# Launch APP

if __name__ == '__main__':
    app.run(debug=True)