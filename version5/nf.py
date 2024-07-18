def details(logs, name)
    l.append[log['trace']]
    for log in logs :
        if lod[trace] not in l :
            l.append[log['trace']]
    print("les type des logs disponibles dans ce dosier est : ")
    print (l)



def copy_file_line_by_line(source_file, destination_file):
    try:
        with open(source_file, 'r') as src:
            with open(destination_file, 'w') as dest:
                for line in src:
                    dest.write(line)
        print(f"Le fichier {source_file} a été copié avec succès vers {destination_file}.")
    except FileNotFoundError:
        print(f"Le fichier {source_file} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


import re

# Fonction pour extraire et afficher les champs
def extract_and_print_fields(log_lines):
    for log_line in log_lines:
        # Supprimer les parties entre crochets
        cleaned_log = re.sub(r"\[.*?\]", "", log_line).strip()
        
        # Expression régulière pour extraire les champs
        pattern = re.compile(r'(?P<timestamp>\d{6,}\.\d{3})?\s*(?P<level>\w+):?\s*(?P<code>0x[\da-f]+)?\s*(?P<module>.*?\:)?\s*(?P<message>.*)', re.IGNORECASE)
        match = pattern.match(cleaned_log)
        
        if match:
            timestamp = match.group('timestamp')
            level = match.group('level')
            code = match.group('code')
            module = match.group('module')
            message = match.group('message')
        else:
            timestamp, level, code, module, message = None, None, None, None, cleaned_log
        
        # Affichage des résultats
        print(f"Timestamp: {timestamp}, Level: {level}, Code: {code}, Module: {module}, Message: {message}")

# Nom du fichier contenant les lignes de log
file_name = "nom_du_fichier.log"

# Lecture des lignes de log à partir du fichier
with open(file_name, 'r') as file:
    log_lines = file.readlines()

# Appeler la fonction avec les lignes de log lues depuis le fichier
extract_and_print_fields(log_lines)

















def details(logs, name ,trace ) :
    print("le sdetails liés au fichier {}".format(name))
    extract_and_print_fields(logs,trace) 
               
    


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
    print("Afficher les details des logs de type : ")
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
        j+=1
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            j+=1
            logs=Extraction_champs(name_with_quotes, name_file[0])
            if choix == 1 :
                nombre(logs, name_file[0])
            else :
                if j== 0 :
                    details(logs, name_file[0],trace)
            print("-" * 100)
    shutil.rmtree(Folder_gz_file_destination) 
    file.close()
    f.close()
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : {} ".format(j))
