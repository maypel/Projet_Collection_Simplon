#!/usr/bin/env python

import pymongo
import subprocess
import json
from pymongo import MongoClient

def test(filename):

    ### transforme liste en dictionnaire
    input_file = filename
    exe = "C:/Exiftool/exiftool.exe"
    process = subprocess.Popen([exe, input_file], stdout=subprocess.PIPE, stderr= subprocess.STDOUT, universal_newlines=True)
    metadata2 = {}
    for output in process.stdout:
        line = (output.strip().split(":",1))
        metadata2[line[0].strip()] = line[1].strip()

    print(metadata2)


    #permet la création du client qui va se connecter à MongoDB
    client = MongoClient()

    #Préparation à la création de la base de données Floupics_MBDD.
    db = client.metadonneesrl

    collection = db.metas_repertoire

    result = collection.insert_one(metadata2)

    #permet de vérifier la liste des collections créées :
    db.list_collection_names()

# Lorsque le fichier est appelé directement on exécute la fonction de test
if __name__ == "__main__":
    test()