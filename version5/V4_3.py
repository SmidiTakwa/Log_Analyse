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
log_file_path="/home/g800336/Desktop/Work/version2/version1/Hi"
output_file_path="data.json"  
log_pattern = re.compile(r"^(?P<month>\w{3})\s+(?P<day>\s?\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>\S+) (?P<service>\S+)\s+(?P<message>.+)$")# Définition de l'expression régulière pour extraire les champs
tar_gz_file_path="/home/g800336/Desktop/Source /LOGS/621240000578_2024-06-27T06_58_33_device-logs_1719493113.tar.gz" # alert + debug : 322270039358_2024-07-08T08_20_06_device-logs_1720448406
Folder_gz_file_destination="./Destination_Directory"
destination_file='/home/g800336/Desktop/Work/version2/version1/new_file'
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                           Fonctions                                                                                                           #        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

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
def nbr_occurrence_module(logs, trace,b) : 
    c=[]
    i=0
    d=[]
    for log in logs :
        if log['trace'] == trace :
            x = log['message'].split(":") 
            c.append(x[0])
    for  i in range(0,len(b)) :   
        d.append(c.count(b[i]))  
        print(d[i])
        print(b[i])
        i+=1
    print(d)      

def determination_origine_de_log_de_type_erreur(logs, trace ) : 
    b=[]
    j=0
    i=0
    c=[]
    d=[]
    for log in logs :
        x = log['message'].split(":") 
        if log['trace'] == trace :
            i+=1
            if x[0] not in b :
                b.append(x[0])             
    return(b)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def detremination_champs_des_message_des_trace_de_type_erreur(logs, trace) :
    i = 0
    b = determination_origine_de_log_de_type_erreur(logs, trace)
    
    for log in logs: 
        x=log['message']
        if log['trace'] == trace : 
            if trace == 'alert' :
                y=x.replace(":","",1)
                l = log['message'].split(":") 
                print ("origine  :  {}    -     message  :  {}".format(l[0], y))
            elif '' in b :
                y=x.replace(":","",1)
                l = log['message'].split(":") 
                print ("origine  :  {}    -     message  :  {}".format(l[0], y))                
            else :
                t = x.split(":")  
                #print(log['message'])
                if t[0] == 'kernel' :
                    o= x.replace("kernel:","")
                    print ("origine  :  {}    -     message  :  {}".format(t[0],o))
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
    k=0
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
        k+=1
        l=0
        name_with_quotes = Folder_gz_file_destination+"/"+name_file[0]
        with open(name_with_quotes,'r') as f :
            logs=Extraction_champs(name_with_quotes, name_file[0])
            i+=1
            j=0
            b=[]
        for log in logs:
            l+=1
            if log['trace'] == trace:
                j+=1
                #print("Mois : {} - Jour : {} - Heure : {} - Hote : {} - Origine : {} - Trace  : {} - Message : {}".format(log['month'],log['day'],log['time'],log['host'],log['origine'],log['trace'],log['message']))
        b=determination_origine_de_log_de_type_erreur(logs, trace)
        detremination_champs_des_message_des_trace_de_type_erreur(logs, trace)
        print("le nombre totale des logs est   {} ".format(l))
        print("le nombre des logs de type  {} dans le fichier   {}  est : {}".format(trace, name_file[0], j))
        nbr_occurrence_module(logs, trace,b)
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
        p =float((float(i) / len(logs) ) ) *100
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

def Extaraction_des_champs_fitrage(file_path) : 
    l=0
    print("Filter les traces de type : ")
    print("1- Erreur ")
    print("2- Alerte ")
    print("3- Warning ")
    print("4- Info ")
    print("5- Debug")
    choix = input("Entrez  votre choix : ")
    trace = recuperation_choix(choix)
    logs=Extraction_champs(file_path, "file")
    j=0
    b=[]
    for log in logs:
        l+=1
        if log['trace'] == trace:
            j+=1
            #print("Mois : {} - Jour : {} - Heure : {} - Hote : {} - Origine : {} - Trace  : {} - Message : {}".format(log['month'],log['day'],log['time'],log['host'],log['origine'],log['trace'],log['message']))
    b=determination_origine_de_log_de_type_erreur(logs, trace)
    detremination_champs_des_message_des_trace_de_type_erreur(logs, trace)
    nbr_occurrence_module(logs, trace,b)
    print("le nombre totale des logs est   {} ".format(l))
    print("le nombre des logs de type  {}   est : {}".format(trace, j))
    print ("les origines des logs de type {} sont : {} ".format(trace,b))
    print("-" * 100)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def Top_3_logs(log_file_path) :
    print("Afficher top 3 des traces de type : ")
    print("1- erreur ")
    print("2- alerte ")
    print("3- warning ")
    print("4- info ")
    print("5- Debug")
    choix = input("Entrez  votre choix : ")
    trace = recuperation_choix(choix)
    logs=Extraction_champs(log_file_path,'file')
    a=affichage_top_trois_message_erreur_reccurrents(logs, 'file', trace)
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
    print("-" * 100)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def statistiques(log_file_path)  :
    print("1-Des nombres ")
    print("2-Des details ")
    choix = input("Votre choix   : ")
    while choix not in range(1,3): 
        choix = input("vous devez 1 un choix validé, reessayez : ")
    if choix == 2 :
        print("Afficher les details des logs de type : ")
        print("1- erreur ")
        print("2- alerte ")
        print("3- warning ")
        print("4- info ")
        c = input("Entrez  votre choix : ")
        trace = recuperation_choix(c)
    logs=Extraction_champs(log_file_path, 'file')
    if choix == 1 :
        nombre(logs, 'file')
    else :
        details(logs,'file',trace)
    print("-" * 100)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def trace_recurente_connue_dans_tous_les_logs(log_file_path):
    i=0
    logs = Extraction_champs(log_file_path, 'file_name')
    test = raw_input('donner la trace à tester sa presence dans le fichier : ')
    log_test = {}
    text="la trace donnée n'existe pas dans le fichier "
    match = log_pattern.match(test) # Recherche des correspondances avec l'expression régulière
    if match:
        log_test = match.groupdict() # Convertir le match en dictionnaire de groupes nommés
        if '.' in log_test['service']: # Diviser le champ service en origine et trace
            log_test['origine'], log_test['trace'] = log_test['service'].split('.')
        else:
            log_test['origine'] = log_test['service']
            log_test['trace'] = ''
        print("log test est validé " )
        for log in logs : 
            i+=1
            if log['trace'] == log_test['trace'] and log['trace'] == log_test['trace'] and log['origine'] == log_test['origine'] and log['host'] == log_test['host'] : 
                x1=log['message']
                y1=re.sub(r"\[\d+:\d+\]","",x1).strip()
                x2=log_test['message']
                y2=re.sub(r"\[\d+:\d+\]","",x2).strip()
                if y1 == y2 :
                    print ("existe dans le fichier et au niveau de la ligne numero : {}".format(i))
    else : 
        print(text)


        
    

 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                Main                                                                                                           #
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
print("Donner le path exacte  du dosier .tar.gz :  ")
#dossier_path = input("Ecrire :")
#test = verification_existance(dossier_path)
test = True
print ("1- fichier .txt")
print ("2- dosier .tar.gz")
p = input ("choisir :  ")
while p not in range(1,3) :
    p = input("Enter un choix validé : ")
if test == True : 
    print("1-Filtrage des logs ")
    print("2-Extaction top 3 logs reccurrentes  ")
    print("3-Des statistiques sur les logs   ")
    print("4-Reconnaitre si la trace est récurrente et connue dans tous les logs.   ")
    choix = input("Choisir une opreration : ")
    while choix not in range(1,5): 
        choix = input("vous devez entrer un choix validé, reessayez : ")
    if p == 2 :
        if choix == 1 :
            Dezip_file_tar_gz_et_Extaraction_des_champs_fitrage(tar_gz_file_path) 
        if choix == 2 :
            Dezip_file_tar_gz_Top_3_logs(tar_gz_file_path)
        elif choix == 3 :
            Dezip_file_tar_gz_statistiques(tar_gz_file_path)
 
    else :
        if choix == 1 :
            Extaraction_des_champs_fitrage(log_file_path) 
        if choix == 2 :
            Top_3_logs(log_file_path)
        elif choix == 3 :
            statistiques(log_file_path) 
        else :
            trace_recurente_connue_dans_tous_les_logs(log_file_path)