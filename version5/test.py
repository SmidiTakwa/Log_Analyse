#-----------------------------------------------------------------------Imports--------------------------------------------------------------------------------------------#
# -*- coding: utf-8 -*
import re #Importe le module re qui fournit des fonctions pour travailler avec des expressions régulières en Python.
import json #Importe le module json qui permet de travailler avec des données au format JSON (JavaScript Object Notation).
import sys, os

#----------------------------------------------------------------------Declarations----------------------------------------------------------------------------------------#

log_file_path="/home/g800336/Desktop/Source /LOGS/TOTLAPLAY_anytime/323319011037_2024-06-27T09_39_02_device-logs_1719502742/messages"
output_file_path="data.json"  

#-----------------------------------------------------------------------Fonctions------------------------------------------------------------------------------------------#

# Définition de l'expression régulière pour extraire les champs
log_pattern = re.compile(r"^(?P<month>\w{3}) (?P<day>\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<service>\S+)\s+(?P<message>.+)$")

def analyze_logs(file_path):
    log_entries = []

    # Lecture du fichier de logs
    with open(file_path, 'r') as file:
        for line in file:
            # Recherche des correspondances avec l'expression régulière
            match = log_pattern.match(line)
            if match:
                # Convertir le match en dictionnaire de groupes nommés
                log_entry = match.groupdict()
                
                # Diviser le champ service en origine et trace
                if '.' in log_entry['service']:
                    log_entry['origine'], log_entry['trace'] = log_entry['service'].split('.')
                else:
                    log_entry['origine'] = log_entry['service']
                    log_entry['trace'] = ''
                
                # Ajouter l'entrée de log à la liste log_entries
                log_entries.append(log_entry)

    return log_entries

def Filtrage_Logs():
    print("§!!!!!!!!!§§!")
def Statistiques():
    print("staaaaaaat")
def Recherche_messages_Logs():
    print("recheeeeerche ")
def Agregation_temporelle_Logs():
    print("Agggre")
def Extaction_Visualisation_Logs():
    print ("vuuuuuuuue")
#-----------------------------------------------------------------------Main--------------------------------------------------------------------------------------------#

print("1-Filtrage des logs ")
print("2-Statistiques des logs ")
print("3-Recherche des messages des logs")
print("4-Agrégation temporelle")
print("5-Extaction et visualisation des données des logs")
choix = input("Choisir une opreration : ")
while choix not in range(1,6): 
    choix = input("vous devez entrer un choix validé, reessayez : ")

if choix == 1 :
    Filtrage_Logs()
elif choix == 2 :
    Statistiques_Logs()
elif choix == 3 :
    Recherche_messages_Logs()
elif choix == 4 :
    Agregation_temporelle_Logs()
else :
    Extaction_Visualisation_Logs()

logs = analyze_logs(log_file_path)
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
        "origine": entry['origine'],
        "message": entry['message'].strip(),
        "origine": entry['origine'],
        "trace": entry['trace']
    }
    i+=1 
    output_logs.append(formatted_entry)
# Affichage du résultat au format JSON
#print(json.dumps(output_logs, indent=4))





















# Affichage des champs extraits pour chaque entrée de log
for entry in logs:
    if entry['trace'] == 'err' :
        i+=1 
        print("Date:", entry['month'], entry['day'])
        print("Heure:", entry['time'])
        print("Hote:", entry['host'])
        print("Origine:", entry['origine'])
        print("Trace:", entry['trace'])
        print("Message:", entry['message'].strip())
        print("-" * 50)
print (i)