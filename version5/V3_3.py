# -*- coding: utf-8 -
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                           Libreries                                                                                                           #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

import re #Importe le module re qui fournit des fonctions pour travailler avec des expressions régulières en Python.
import json #Importe le module json qui permet de travailler avec des données au format JSON (JavaScript Object Notation).
import tarfile 
import os
import shutil
from collections import Counter
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                          Declarations                                                                                                         #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
log_file_path="E:/Stage2/Work/Source/LOGS/621240008129_2024-07-08T08_24_02_device-logs_1720448642/messages"
output_file_path="data.json"  
log_pattern = re.compile(r"^(?P<month>\w{3})\s+(?P<day>\s?\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<service>\S+)\s+(?P<message>.+)$")# Définition de l'expression régulière pour extraire les champs
tar_gz_file_path="/home/g800336/Desktop/Source /LOGS/322280027968_2024-07-08T08_20_31_device-logs_1720448431.tar.gz"
Folder_gz_file_destination="./Destination_Directory"

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                           Fonctions                                                                                                           #        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def Extraction_champs(file_path, name):
    log_entries = []
    
    # Lecture du fichier de logs
    with open(file_path, 'r') as file:
        i=0
        for line in file:
            # Recherche des correspondances avec l'expression régulière
            match = log_pattern.match(line)
            if match:
                # Convertir le match en dictionnaire de groupes nommés
                log_entry = match.groupdict()
                i+=1

                # Diviser le champ service en origine et trace
                if '.' in log_entry['service']:
                    log_entry['origine'], log_entry['trace'] = log_entry['service'].split('.')
                else:
                    log_entry['origine'] = log_entry['service']
                    log_entry['trace'] = ''
                
                # Ajouter l'entrée de log à la liste log_entries
                log_entries.append(log_entry)
        print("le nombre des logs de fichier {} est : {} ".format(name,i))
    return log_entries


def Affectation_champs_au_Json_et_affichage(logs):
    # Écrire les logs analysés dans un fichier JSON
    with open(output_file_path, 'w') as json_file:
        json.dump(logs, json_file, indent=4)
    output_logs = []
    i=0 
    for entry in logs:
        formatted_entry = {
            "month": entry['month'],
            "day": entry['day'],
            "time": entry['time'],
            "host": entry['host'],
            #"service": f"{entry['origine']}.{entry['trace']}",
            "message": entry['message'].strip(),
            "origine": entry['origine'],
            "trace": entry['trace']
        }
        i+=1 
    output_logs.append(formatted_entry)
    # Affichage du résultat au format JSON
    #print(json.dumps(output_logs, indent=4))   
    #print("le nombre des logs est :" , end=" ")
    #print("le nombre des logs  dans Ce fichier  : {}  est : {}".format( name_file[0], j))



def Affichage_des_logs(logs, name, trace) :
    # Affichage des champs extraits pour chaque entrée de log
    j=0
    for entry in logs:
         if entry['trace'] == trace :
             j+=1 
    #         print("Date:", entry['month'], entry['day'])
    #         print("Heure:", entry['time'])
    #         print("Hote:", entry['host'])
    #         print("Origine:", entry['origine'])
    #         print("Trace:", entry['trace'])
    #         print("Message:", entry['message'].strip())
    #         print("-" * 50)

    print("le nombre des logs de type  {} dans le fichier  : {}  est : {}".format(trace, name, j))

def Dezip_file_tar_gz_filtarge(tar_gz_file_path):
    file = tarfile.open(tar_gz_file_path) # open file  
    file_names=file.getnames() # liste de file names
    file.extractall(Folder_gz_file_destination) # extract files 
    filtrage_logs(file_names , Folder_gz_file_destination)
    shutil.rmtree(Folder_gz_file_destination) 
    # close files 
    file.close()

def affichage_top_trois_message_erreur_reccurrents(logs,name , trace) :
    for log in logs :
        if log['trace'] == trace :
            x=log['message']
            y=re.sub(r"\[\d+:\d+\]","",x).strip()
            log['message']=y
    error_logs = [log for log in logs if log['trace'] == trace ]  # Filtrer les logs avec une trace "erreur"
    #for log in error_logs :
    #    print (log['message'])
    #x = log['message'].split(':')
    
    message_counts = Counter(log['message'] for log in error_logs) # Compter les occurrences des messages
    top_3_messages = message_counts.most_common(3) # Trouver les 3 messages les plus récurrents
    return top_3_messages

def Dezip_file_tar_gz_Top_3_logs(tar_gz_file_path) :
    print("Afficher top 3 des traces de type : ")
    print("1- erreur ")
    print("2- alerte ")
    print("3- warning ")
    print("4- info ")
    choix = input("Entrez  votre choix : ")
    while choix not in range(1,5): 
        choix = input("vous devez entrer un choix validé, reessayez : ")
    if choix == 1 : 
        trace = 'err'
    elif choix == 2 :
        trace = 'alert'
    elif choix == 3 : 
        trace = 'warn'
    else :
        trace = 'info'
    j=0
    file = tarfile.open(tar_gz_file_path) # open file  
    file_names=file.getnames() # liste de file names
    file.extractall(Folder_gz_file_destination) # extract files 
    for name in file_names:
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            Affichage_des_logs(logs, name_file[0], trace) 
            a=affichage_top_trois_message_erreur_reccurrents(logs, name_file[0], trace)
            k= len(a) 
            if k == 0 :
                print("Pas de log de tyoe alerte pour le moment dans ce fichier  ")
            elif k == 1 :
                print("numero 1 est : {}".format(a[0]))
            elif k == 2 :
                print("numero 1 est : {}".format(a[0]))
                print("numero 2 est : {}".format(a[1]))
            else : 
                print("numero 1 est : {}".format(a[0]))
                print("numero 2 est : {}".format(a[1]))
                print("numero 3 est : {}".format(a[2]))     
            #content = f.read()
            print("-" * 100)
        j+=1
    shutil.rmtree(Folder_gz_file_destination) 
    # close files 
    file.close()
    f.close()
    #print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : ", end=' ')
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : {} ".format(j))



def filtrage_logs(file_names, Folder_gz_file_destination) :
    i=0
    print("Afficher les traces de type : ")
    print("1- erreur ")
    print("2- alerte ")
    print("3- warning ")
    print("4- info ")
    choix = input("Entrez  votre choix : ")
    while choix not in range(1,5): 
        choix = input("vous devez entrer un choix validé, reessayez : ")
    if choix == 1 : 
        trace = 'err'
    elif choix == 2 :
        trace = 'alert'
    elif choix == 3 : 
        trace = 'warn'
    else :
        trace = 'info'

    for name in file_names:
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            i+=1
            j=0
        for entry in logs:
            if entry['trace'] == trace:
                j+=1 

        message = "le nombre des logs de type  :  " + trace + "  dans le fichier  :"+ name_file[0] + "  est :"
        print("le nombre des logs de type  {} dans le fichier   {}  est : {}".format(trace, name_file[0], j))
        print("-" * 100)
        f.close()
    #print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : ", end=' ')
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : ")
    print(i)

def nombre(logs, name) :
    print("le nombre totale des logs du fichier   {}  est : {}".format( name,len(logs)))
    l=[]
    i=0
    p=0
    for log in logs :
        if log['trace'] not in l :
            l.append(log['trace'])
    print("les type des logs disponibles dans ce dosier est :  {}".format(l))
    for trace in l :

        for log in logs :
            if log['trace'] == trace :
                i+=1
        p =float((float(i) % len(logs) ) ) / 100
        print("le nombre des logs de type {} est   {} ce qui prsente la pourcentage suivante {} %  ".format(trace, i, p) )
        i=0
        p=0
        


def details(logs, name) :
    print("hi")

def Dezip_file_tar_gz_statistiques(tar_gz_file_path) :
    print("1-Des nombres ")
    print("2-Des details ")
    choix = input("Votre choix   : ")
    while choix not in range(1,3): 
        choix = input("vous devez entrer un choix validé, reessayez : ")
    j=0
    file = tarfile.open(tar_gz_file_path) # open file  
    file_names=file.getnames() # liste de file names
    file.extractall(Folder_gz_file_destination) # extract files 
    for name in file_names:
        j+=1
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            if choix == 1 :
                nombre(logs, name_file[0])
            else :
                details(logs, name_file[0])

            print("-" * 100)
    shutil.rmtree(Folder_gz_file_destination) 
    file.close()
    f.close()
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : {} ".format(j))

        
def Dezip_file_tar_gz_Affichage(tar_gz_file_path):
    j=0
    file = tarfile.open(tar_gz_file_path) # open file  
    file_names=file.getnames() # liste de file names
    file.extractall(Folder_gz_file_destination) # extract files 
    for name in file_names:
        j+=1
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            if choix == 1 :
                nombre(logs, name_file[0])
            else :
                details(logs, name_file[0])

            print("-" * 100)
    shutil.rmtree(Folder_gz_file_destination) 
    file.close()
    f.close()
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : {} ".format(j))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                Main                                                                                                           #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#logs = Extraction_champs(log_file_path)
#Affectation_champs_au_Json_et_affichage(logs)
#Affichage_des_logs(logs)
print("1-Filtrage des logs ")
print("2-Extaction top 3 logs reccurrentes  ")
print("3-Des statistiques sur les logs   ")
print("4-Affichage   ")
choix = input("Choisir une opreration : ")
while choix not in range(1,5): 
    choix = input("vous devez entrer un choix validé, reessayez : ")
if choix == 1 :
    Dezip_file_tar_gz_filtarge(tar_gz_file_path)
elif choix == 3 :
    Dezip_file_tar_gz_statistiques(tar_gz_file_path)
elif choix == 4 :
    Dezip_file_tar_gz_Affichage(tar_gz_file_path)
else :
    Dezip_file_tar_gz_Top_3_logs(tar_gz_file_path)