'''
Created on Sep 12, 2013

@author: keyvi_000
'''

#main data structure 
   # {directory:{file:[modified_date, md5hash]}}


import os
import hashlib 
import shutil

class snapshot():
    def __init__(self):
        self.directories = {}
#add the list to the files dict with the key directories
#iterate through folders and subfolders to build a collection of all files    
    def add_dir(self, directory):
        self.directories[directory] = {}
        for path, subdirs,  files in os.walk(directory):
            for filename in files:
                s = open(os.path.join(path,filename), 'rb',).read()
                #s = s.encode('utf_8')
                self.directories[directory][os.path.join(path,filename)] = [os.path.getmtime(os.path.join(path,filename)), hashlib.md5(s)]
        
        
     
#returns two dicts, one of files to copy from self to othersnap, another with files 
#that need to be copied from othersnap to the self directory 
#returns {file:[prefix, mtime, md5]
    def comp(self, othersnap):
        fromself = {}
        toself = {}
        set1 = {}
        for i in self.directories.keys():
            currentset = self.directories[i]
            prefix = i
            for file in currentset.keys():
                set1[file[len(prefix):]] = [prefix] + currentset[file] #strip the directory prefix 
        set2 = {}    
        for j in othersnap.directories.keys():
            currentset = othersnap.directories[j]
            prefix = j
            for file in currentset.keys():
                set2[file[len(prefix):]] = [prefix] + currentset[file]
                
        for file in set1.keys():
            if file in set2:
                if set2[file][2] != set1[file][2]:
                    #md5 sums do not match!
                    if set1[file][1] > set2[file][1]:  #compare mtimes
                        fromself[file] = set1[file]         
                    elif set1[file][1] < set2[file][1]:
                        toself[file] =  set2[file]
                    else:
                        pass
                        #code something to freak out about the files having the same mtime
                        #but have different md5sums
            else:
                #file doesn't exist in othersnap
                fromself[file] = set1[file]
                
            #At this point we have checked for overlap in set1 and set2, and everything in set 1 that isn't in set 2 will be returned
        for file in set2.keys():
            if file in set1:
                pass
            else:
                toself[file] = set2[file]
        return fromself, toself
     
     
def sync(snap1, snap2):
    fromsnap1, tosnap1 = snap1.comp(snap2)     
    for file in fromsnap1.keys():
        targetdir = list(snap2.directories.keys())[0]
        #check if its a sub directory
        path = make_sub_dirs(file, targetdir)
        if path!='':
            shutil.copy2(fromsnap1[file][0]+file, path)
        else:
            shutil.copy2(fromsnap1[file][0]+file, targetdir)
    
    for file in tosnap1.keys():
        targetdir = list(snap1.directories.keys())[0]
        #shutil.copy2(tosnap1[file][0]+file, targetdir)
        #cp tosnap1[file][0] + file to targetdir(snap1)
        path = make_sub_dirs(file, targetdir)
        if path != '':
            shutil.copy2(tosnap1[file][0]+file, path)
        else:
            shutil.copy2(tosnap1[file][0]+file, targetdir)
                  
#checks if all directories in path exist, if not create them and return path
def make_sub_dirs(file, targetdir):
    dirs = file.split(os.path.sep)[1:-1]
    path = ''
    if len(dirs) > 0:
        path = targetdir   #was a sub directory. Iteratively create all sub directories
        for direct in dirs:
            if os.path.isdir(path + os.path.sep + direct):
                path = path + os.path.sep + direct
            else:
                os.mkdir(path + os.path.sep + direct)
                path = path + os.path.sep + direct
    return path


#first = snapshot()
#first.add_dir(r'\file1')
#second = snapshot()
#second.add_dir(r'\file2')
#first.comp(second)
#sync(first,second)
