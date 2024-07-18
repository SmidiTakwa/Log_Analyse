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
tar_gz_file_path="/home/g800336/Desktop/Source /LOGS/322270039074_2024-07-02T02_55_48_device-logs_1719910548.tar.gz"
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
            match = log_pattern.match(line) # Recherche des correspondances avec l'expression régulière
            if match:
                log_entry = match.groupdict() # Convertir le match en dictionnaire de groupes nommés
                i+=1
                if '.' in log_entry['service']: # Diviser le champ service en origine et trace
                    log_entry['origine'], log_entry['trace'] = log_entry['service'].split('.')
                else:
                    log_entry['origine'] = log_entry['service']
                    log_entry['trace'] = ''
                log_entries.append(log_entry) # Ajouter l'entrée de log à la liste log_entries
        print("le nombre des logs de fichier {} est : {} ".format(name,i))
    return log_entries

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def liste_des_traces(logs):
    a=[]
    for log in logs : 
        if log['trace'] not in a :
            a.append(log['trace']) 
    return (a)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def Dezip_file_tar_gz_et_Extaraction_des_champs_fitrage(tar_gz_file_path) :
    file = tarfile.open(tar_gz_file_path)  
    file_names=file.getnames()
    file.extractall(Folder_gz_file_destination) # extract files 
    filtrage_logs(file_names , Folder_gz_file_destination)
    shutil.rmtree(Folder_gz_file_destination) 
    file.close()  

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def recuperation_choix(choix) : 
    while choix not in range(1,6): 
        choix = input("vous devez entrer un choix validé, reessayez : ")
    if choix == 1 : 
        trace = 'err'
    elif choix == 2 :
        trace = 'alert'
    elif choix == 3 : 
        trace = 'warn'
    elif choix == 5 : 
        trace = 'debug'
    else :
        trace = 'info'
    print(trace)
    return(trace)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def determination_origine_de_log_de_type_erreur(logs, trace ) : 
    b=[]
    j=0
    i=0
    for log in logs :
        if log['trace'] == trace :
            x = log['message'].split(":") 
            i+=1
            if x[0] not in b :
                b.append(x[0])             
    return(b)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def detremination_champs_des_message_des_trace_de_type_erreur(logs, trace) :
    i = 0
    b = determination_origine_de_log_de_type_erreur(logs, trace)
    for log in logs: 
        if log['trace'] == trace :
            x=log['message']
            t = x.split(":")  
            #print(log['message'])
            if t[0] == 'kernel' :
                o= x.replace("kernel:","")
                print("Origine :   {}  ".format(t[0]))
                print("message :  {}  ".format(o))
            else :
                v= log['message'].split(":")
                y=re.sub(r"\[\d+:\d+\]","",x).strip()
                #print (y)
                h = log['message'].split(":") 
                m=h[0]+": "
                n=y.replace(m," ")
                m=n.replace("["," ")
                k=m.replace("]"," ")
                g=k.split()
                #print(y)
                f=g[3:]
                h=""
                for i in  range (0,len(f)) :
                    h+= f[i] +" "
                print("Origine :   {}  ".format(v[0]))
                print("Module  :   {}  ".format(g[0]))
                print("Fichier :   {}  ".format(g[1]))
                print("Fonction:   {}  ".format(g[2]))
                print("Message :   {}  ".format(h))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def filtrage_logs(file_names, Folder_gz_file_destination) :
    i=0
    print("Filter les traces de type : ")
    print("1- Erreur ")
    print("2- Alerte ")
    print("3- Warning ")
    print("4- Info ")
    print("5- Debug")
    choix = input("Entrez  votre choix : ")
    trace = recuperation_choix(choix)
    for name in file_names:
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            i+=1
            j=0
            b=[]
        for log in logs:
            if log['trace'] == trace:
                j+=1
                #print("Mois : {} - Jour : {} - Heure : {} - Hote : {} - Origine : {} - Trace  : {} - Message : {}".format(log['month'],log['day'],log['time'],log['host'],log['origine'],log['trace'],log['message']))
        b=determination_origine_de_log_de_type_erreur(logs, trace)
        detremination_champs_des_message_des_trace_de_type_erreur(logs, trace)
        print("le nombre des logs de type  {} dans le fichier   {}  est : {}".format(trace, name_file[0], j))
        print ("les origines des logs de type {} sont : {} ".format(trace,b))
        print("-" * 100)
        f.close()
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : ")
    print(i)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def affichage_top_trois_message_erreur_reccurrents(logs,name ,trace) :
    for log in logs :
        if log['trace'] == trace :
            x=log['message']
            y=re.sub(r"\[\d+:\d+\]","",x).strip()
            log['message']=y
    error_logs = [log for log in logs if log['trace'] == trace ]  # Filtrer les logs selon trace donné 
    #for log in error_logs :
    #    print (log['message'])
    #x = log['message'].split(':')
    message_counts = Counter(log['message'] for log in error_logs) # Compter les occurrences des messages
    top_3_messages = message_counts.most_common(3) # Trouver les 3 messages les plus récurrents
    return top_3_messages

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def Dezip_file_tar_gz_Top_3_logs(tar_gz_file_path) :
    print("Afficher top 3 des traces de type : ")
    print("1- erreur ")
    print("2- alerte ")
    print("3- warning ")
    print("4- info ")
    print("5- Debug")
    choix = input("Entrez  votre choix : ")
    trace = recuperation_choix(choix)
    j=0
    file = tarfile.open(tar_gz_file_path)  
    file_names=file.getnames() 
    file.extractall(Folder_gz_file_destination) 
    for name in file_names:
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def details(logs, name , trace ) :
    print("les details liés au fichier {}   : ".format(name))
    extract_and_print_fields(logs,trace) 

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def extract_and_print_fields(logs, trace):
    i=0
    for log in logs:
        # Supprimer les parties entre crochets
        if log['trace'] == trace :
            x= log['message']
            cleaned_log = re.sub(r"\[.*?\]", "", x).strip()
        
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
            print ("time stamp : {}, level : {}, code : {}, module : {}, messages : {}".format(timestamp,level,code,module,message))
        
            # match = log_pattern.match(y)
            # if match:
            #     # Convertir le match en dictionnaire de groupes nommés
            #     message_log = match.groupdict()
            #     print ("time stamp : {}, level : {}, code : {}, module : {}, messages : {}".format(message_log['timestamp'],message_log['level'],message_log['code'],message_log['module'],message_log['message']))
    print("le nombre des logs de type {} est : {} ".format(trace,i))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def Dezip_file_tar_gz_statistiques(tar_gz_file_path) :
    print("1-Des nombres ")
    print("2-Des details ")
    choix = input("Votre choix   : ")
    while choix not in range(1,3): 
        choix = input("vous devez 1 un choix validé, reessayez : ")
    j=0
    file = tarfile.open(tar_gz_file_path) # open file  
    file_names=file.getnames() # liste de file names
    file.extractall(Folder_gz_file_destination) # extract files 
    if choix == 2 :
        print("Afficher les details des logs de type : ")
        print("1- erreur ")
        print("2- alerte ")
        print("3- warning ")
        print("4- info ")
        c = input("Entrez  votre choix : ")
        trace = recuperation_choix(c)
    for name in file_names:
        j+=1
        name_file=name.split('"')
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            
            if choix == 1 :
                nombre(logs, name_file[0])
            else :
                if j==1 :
                    details(logs, name_file[0],trace)
            print("-" * 100)
    shutil.rmtree(Folder_gz_file_destination) 
    file.close()
    f.close()
    print("le nombre de files dans ce fichier d'extention .tar.gz il y'a : {} ".format(j))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                Main                                                                                                           #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
print("Donner le path exacte  du dosier .tar.gz :  ")
#dossier_path = input("Ecrire :")
#test = verification_existance(dossier_path)
test = True
if test  == True : 
    print("1-Filtrage des logs ")
    print("2-Extaction top 3 logs reccurrentes  ")
    print("3-Des statistiques sur les logs   ")
    print("4-Affichage   ")
    choix = input("Choisir une opreration : ")
    while choix not in range(1,5): 
        choix = input("vous devez entrer un choix validé, reessayez : ")
    if choix == 1 :
        Dezip_file_tar_gz_et_Extaraction_des_champs_fitrage(tar_gz_file_path) 
    if choix == 2 :
        Dezip_file_tar_gz_Top_3_logs(tar_gz_file_path)
    elif choix == 3 :
        Dezip_file_tar_gz_statistiques(tar_gz_file_path)