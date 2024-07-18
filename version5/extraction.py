
# importing the "tarfile" module 
import tarfile 
import os
import shutil


# open file 
file = tarfile.open('/home/g800336/Desktop/Work/version1/Extracion_Directory/t.tar.gz') 
  
# print file names 
print(file.getnames()) 
  
# extract files 
file.extractall('./Destination_FolderName') 
with open('./Destination_FolderName/messages','r') as f :
        content = f.read()
        print(content) 

shutil.rmtree('./Destination_FolderName') 
#os.rmdir("./Destination_FolderName")
# close files 
file.close() 
f.close()




