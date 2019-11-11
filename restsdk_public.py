##Intended for python3.6 on linux, probably won't work on Windows
##This software is distributed without any warranty. It will probably brick your computer.
#DO NOT ADD SLASHES TO END OF DIRECTORIES
db='/restsdk/data/db/index.db' #where the file DB is stored example: /data/db/index.db
filedir='/restsdk/data/files' #where the files are stored example: /restsdk/data/files
dumpdir='/location/to/dump/files/to' #where you want the new files dumped example:/EXTERNAL/FILES
#NOTHING AFTER THIS LINE NEEDS TO BE EDITED
skipnames=[filedir] #remove these strings from the final file/path name. Don't edit this.
import sqlite3
import pprint
import copy
import os
from shutil import copyfile
    
def findNextParent(fileID):
    #finds the next parent db item in a chain
    for key,value in fileDIC.items():
        if key==fileID:
            return value['Parent']
def hasAnotherParent(fileID):
    #checks to see if a db item has another parent
    if fileDIC[fileID]['Parent']!=None:
        return True
    else:
        return False
def findTree(fileID,name,parent):
    #turn a file ID into an original path
    path=fileDIC[parent]['Name']+"/"+name
    while hasAnotherParent(fileID)==True:
        fileID=findNextParent(fileID)
        path=fileDIC[fileID]['Name']+'/'+path
    return path

def idToPath2(fileID):
    #turn a file ID into an original path
    value=fileDIC[fileID]
    if value['Parent']!=None:
        #print("Found file " + value['Name'] + 'searching for parents')
        #print('Totalpath is ' + path)
        path=findTree(fileID,value['Name'],value['Parent'])
    else:
        #print("Found file " + value['Name'] + 'no parent search needed')
        path=fileDIC[fileID]['Name']
    return path

def filenameToID(filename):
    #turn a filename from filesystem into a db id
    for keys,values in fileDIC.items():
        if values['contentID']==filename:
            #print('Found filename ' + filename + ' in DBkey ' + str(keys) +' with name ' + values['Name'])
            return str(keys)
    #print('Unable to find filename' + filename)
    return None

def getRootDirs():
    #quick function to find annoying "auth folder" name for filtering purposes
    for keys,values in fileDIC.items():
        if 'auth' in values['Name'] and '|' in values['Name']:
            return str(values['Name'])

#open the sqlite database
print('Opening database...',end="/r")
try:
    con = sqlite3.connect(db)
except:
    print('Error opening database at ' + db)
    quit()
print('Querying database...',end="/r")
cur = con.cursor()
cur.execute("SELECT id,name,parentID,mimeType,contentID FROM files")
files = cur.fetchall()
#SQlite has a table named "FILES", the filename in the file structure is found in ContentID, with the parent directory being called ParentID
fileDIC={}

for file in files:
    fileID=file[0]
    fileName=file[1]
    fileParent=file[2]
    mimeType=file[3]
    contentID=file[4]
    fileDIC[fileID]={'Name':fileName,'Parent':fileParent,'contentID':contentID,'Type':mimeType,'fileContentID':''}

skipnames.append(getRootDirs()) #remove obnoxious root dir names
for root,dirs,files in os.walk(filedir): #find all files in original directory structure
    for file in files:
        filename=str(file)
        print('FOUND FILE ' + filename + ' SEARCHING......',end="\r")
        fileID=filenameToID(str(file))
        fullpath=None
        if fileID!=None:
            fullpath=idToPath2(fileID)
        if fullpath!=None:
            #print('FILE RESOLVED TO ' + fullpath)
            for paths in skipnames:
                newpath=fullpath.replace(paths,'')
            newpath=dumpdir+newpath
            fullpath=str(os.path.join(root,file))
            #print('Copying ' + fullpath + ' to ' + newpath,end="\r")
            print('Copying ' + newpath)
            try:
                os.makedirs(os.path.dirname(newpath), exist_ok=True)
                copyfile(fullpath,newpath)
            except:
                print('Error copying file ' + fullpath + ' to ' + newpath)
print("Did this script help you recover your data? Or make you some money recovering somebody else's data?")
print("Consider sending us some bitcoin as a way of saying thanks!")
print("1DqSLNR8kTgwq5rvveUFDSbYQnJp9D5gfR")
