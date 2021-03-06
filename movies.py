import pymongo  
from tkinter import * 
import os

"""
Importation du jeu de données dans MongoDB sur le port par défaut 27017
"""
#os.system('cd "C:\\Program Files\\MongoDB\\Server\\4.0\\bin\\" ; mongoimport --db movies --collection set "C:\\Users\\SEBASTIEN\\Desktop\\movies_mongodb.json" ; mongod ')

"""
Etablissement d'un lien entre python et la base
"""

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["movies"]
mycol = mydb["set"]


# Construction de la fenetre principale

fenetre = Tk()
fenetre.title("Projet MongoDB/Python sur une base de données json de films")
fenetre.geometry("480x720")

#fenetre.resizable(width=0,height=0)


Label(fenetre, text="Déscriptif des films s'appelant:").pack()


entree = Entry(fenetre, width=50)
entree.pack()


liste = Listbox(fenetre)
liste.pack(side="top",fill="x", expand=True)

def generate():
    liste1=[]
    liste.delete(0,liste.size())
    
    
    myquery= { "fields.title": {"$regex" : "", "$options" : "i"} }
    myquery["fields.title"]["$regex"]=(str(entree.get()))    
    #myquery = { "fields.title": "" }
    #myquery["fields.title"]=str(entree.get())

    myproj= {"fields.title" : 1, "fields.plot" : 1 , "_id" : 0 }

    mydoc = mycol.find(myquery, myproj)
    for x in mydoc:
        try: 
            if myquery["fields.title"]["$regex"]=="" :
                break
            else:
                liste1.append(x["fields"]["title"]+" : "+x["fields"]["plot"])
        except:
            print()
    for i in range(len(liste1)):
        liste.insert(i+1, liste1[i])


Button(text="Generer", command=generate).pack()

Label(fenetre, text="Nom des films avec cet(te) acteur(-trice):").pack()

entree2 = Entry(fenetre, textvariable="", width=50)
entree2.pack()

liste2 = Listbox(fenetre)
liste2.pack(side="top",fill="x", expand=True)

def generate2():
    liste1=[]
    liste2.delete(0,liste2.size())

    myquery = { "fields.actors": "Tom Cruise" } 
    myquery["fields.actors"]=str(entree2.get())
    myproj= {"fields.title" : 1 , "_id" : 0 }
    mydoc = mycol.find(myquery, myproj)

    for x in mydoc:
        liste1.append(x["fields"]["title"])
    for i in range(len(liste1)):
        liste2.insert(i+1, liste1[i])

def generate2beta():
    liste1=[]
    liste2.delete(0,liste2.size())
    
    myquery= { "fields.actors": {"$regex" : "", "$options" : "i"} }
    myquery["fields.actors"]["$regex"]=(str(entree2.get()))    
   
    myproj= {"fields.actors" : 1, "fields.title" : 1 , "_id" : 0 }
    mydoc = mycol.find(myquery, myproj)

    for x in mydoc:
        try: 
            if myquery["fields.actors"]["$regex"]=="" :
                break
            else:
                liste1.append(str(x["fields"]["actors"])+" joue(nt) dans le film : "+str(x["fields"]["title"]))
        except:
            print()
    for i in range(len(liste1)):
        liste2.insert(i+1, liste1[i])

Button(text="Generer", command=generate2beta).pack()

Label(fenetre, text="Films récents avec une note sur 10 supérieure à:").pack()
Label(fenetre, text="(triés par date de sortie du plus récent au plus vieux)").pack()

StringVar().set("")
rat_min = Entry(fenetre, textvariable="", width=50)
rat_min.pack()

lstrat = Listbox(fenetre)
lstrat.pack(side="top",fill="x", expand=True)

def strtofloat(str):
    try:
        float(str)
        return float(str)
    except:
        return 0

def recent_good_films():
    liste1=[]

    lstrat.delete(0,lstrat.size())

    varMatch = { "$match" : { "fields.rating" : {"$gte" : 0}}}
    varMatch["$match"]["fields.rating"]["$gte"]=strtofloat(rat_min.get())

    varProject = { "$project" : {"fields.title" : 1 , "_id" : 0 }}
    varSort = { "$sort" : {"fields.year" : -1}}
    
    output = mycol.aggregate( [ varMatch, varProject, varSort ] )

    for elem in output:
        liste1.append(elem["fields"]["title"])
    for i in range(len(liste1)):
        lstrat.insert(i+1, liste1[i])


Button(text="Generer", command=recent_good_films).pack()

bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
bouton.pack()



fenetre.mainloop()