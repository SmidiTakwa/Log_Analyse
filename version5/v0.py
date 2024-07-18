# -*- coding: utf-8 -
import re #Importe le module re qui fournit des fonctions pour travailler avec des expressions régulières en Python.
import json #Importe le module json qui permet de travailler avec des données au format JSON (JavaScript Object Notation).

log_file_path="/home/g800336/Desktop/Source /LOGS/322246032589_2024-04-23T07%3A09%3A33_device-logs_1713877773/messages"
output_file_path="data.json"  

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

# Exemple d'utilisation
logs = analyze_logs(log_file_path)
# Écrire les logs analysés dans un fichier JSON
with open(output_file_path, 'w') as json_file:
    json.dump(logs, json_file, indent=4)
output_logs = []
i=0 
j=0
for entry in logs:
    formatted_entry = {
        "month": entry['month'],
        "day": entry['day'],
        "time": entry['time'],
        "host": entry['host'],
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
        j+=1 
        print("Date:", entry['month'], entry['day'])
        print("Heure:", entry['time'])
        print("Hote:", entry['host'])
        print("Origine:", entry['origine'])
        print("Trace:", entry['trace'])
        print("Message:", entry['message'].strip())
        print("-" * 50)
print (i)
print(j)