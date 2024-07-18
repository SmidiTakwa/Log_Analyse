# -*- coding: utf-8 -
#--------------------------------------------------------------------------------------------------------------------------------------#
#                                                       Libreries                                                                      #
#--------------------------------------------------------------------------------------------------------------------------------------#

import re #Importe le module re qui fournit des fonctions pour travailler avec des expressions régulières en Python.
import json #Importe le module json qui permet de travailler avec des données au format JSON (JavaScript Object Notation).
import tarfile 
import os
import shutil
from collections import Counter
#--------------------------------------------------------------------------------------------------------------------------------------#
#                                                       Declarations                                                                   #
#--------------------------------------------------------------------------------------------------------------------------------------#
log_file_path="E:/Stage2/Work/Source/LOGS/621240008129_2024-07-08T08_24_02_device-logs_1720448642/messages"
output_file_path="data.json"  
log_pattern = re.compile(r"^(?P<month>\w{3})\s+(?P<day>\s?\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<service>\S+)\s+(?P<message>.+)$")# Définition de l'expression régulière pour extraire les champs
tar_gz_file_path="/home/g800336/Desktop/Source /LOGS/621240007568_2024-07-08T08_23_56_device-logs_1720448636.tar.gz"
Folder_gz_file_destination="./Destination_Directory"

#--------------------------------------------------------------------------------------------------------------------------------------#
#                                                       Fonctions                                                                      #
#--------------------------------------------------------------------------------------------------------------------------------------#
def Extraction_champs(file_path, name):
    log_entries = []
    i=0
    # Lecture du fichier de logs
    with open(file_path, 'r') as file:
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
        message = "le nombre des logs de fichier " + name + "  est :"
        #print(message, end=" ")
        print(message)
        print(i)
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
    print("le nombre des logs est :" )
    print(i)


def Affichage_des_logs(logs, name) :
    # Affichage des champs extraits pour chaque entrée de log
    j=0
    for entry in logs:
         if entry['trace'] == 'err' :
             j+=1 
    #         print("Date:", entry['month'], entry['day'])
    #         print("Heure:", entry['time'])
    #         print("Hote:", entry['host'])
    #         print("Origine:", entry['origine'])
    #         print("Trace:", entry['trace'])
    #         print("Message:", entry['message'].strip())
    #         print("-" * 50)
    message = "le nombre des logs de type erreur dans le fichier  "+ name + "  est :"
    #print (message, end=" ")
    print (message)
    print(j)

def Dezip_file_tar_gz(tar_gz_file_path):
    j=0
    file = tarfile.open(tar_gz_file_path) # open file  
    file_names=file.getnames() # liste de file names
    file.extractall(Folder_gz_file_destination) # extract files 
    for name in file_names:
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            Affichage_des_logs(logs, name_file[0]) 
            a=affichage_top_trois_message_erreur_reccurrents(logs, name_file[0])
            print(a)
            #content = f.read()
            print("-" * 100)
        j+=1
    shutil.rmtree(Folder_gz_file_destination) 
    # close files 
    file.close()
    f.close()
    #print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : ", end=' ')
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : ")
    print(j)

def affichage_top_trois_message_erreur_reccurrents(logs,name) :
    error_logs = [log for log in logs if log['trace'] == 'err']  # Filtrer les logs avec une trace "erreur"
    message_counts = Counter(log['message'] for log in error_logs) # Compter les occurrences des messages
    top_3_messages = message_counts.most_common(3) # Trouver les 3 messages les plus récurrents
    return top_3_messages

#--------------------------------------------------------------------------------------------------------------------------------------#
#                                                       Main                                                                           #
#--------------------------------------------------------------------------------------------------------------------------------------#   
#logs = Extraction_champs(log_file_path)
#Affectation_champs_au_Json_et_affichage(logs)
#Affichage_des_logs(logs)
Dezip_file_tar_gz(tar_gz_file_path)