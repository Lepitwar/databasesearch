# Assignment:           Mini Project 2
# Due Date:             November 24, 2015
# Name:                 Dylan Waters, 
# Unix ID:              dwaters, 
# StudentID:            1343144, 
# Lecture Section:      B1
# Instructor:           Davood Rafiei
# Group:                20
#---------------------------------------------------------------
#
# library import
import subprocess
import os
from bsddb3 import db

def review():   
    db_reviews = db.DB()
    database = 'rw.idx'
    
    db_reviews.open(database, None, db.DB_HASH, db.DB_CREATE)
    
    try:
        file= open("reviews.txt","r")
        new_file = open("reviews_new.txt", "w")
    except IOError:
        print("Error opening file")
    else:
        for line in file:
            line= line.split(",",1)  
            new_file.write(line[0] + "\n" + line[1])
            
    file.close()
    new_file.close()
            
    cursor = db_reviews.cursor()    
    subprocess.call(["db_load -T -t hash -f reviews_new.txt rw.idx"], shell=True)
    
    
    cursor.close()
    db_reviews.close()
    return

def pterm():
    db_pterms = db.DB()
    database = 'pt.idx'
    db_pterms.set_flags(db.DB_DUPSORT) 
    
    db_pterms.open(database, None, db.DB_BTREE, db.DB_CREATE)
    
    try:
        file= open("pterms.txt","r")
        new_file = open("pterms_new.txt", "w")
    except IOError:
        print("Error opening file")
    else:
        for line in file:
            line= line.split(",",1) 
            new_file.write(line[0] + "\n" + line[1])
            
    file.close()
    new_file.close()    
    
    #cursor = db_pterms.cursor()    
    subprocess.call(["db_load -T -t btree -f pterms_new.txt pt.idx"], shell=True)    
    
    #iter = cursor.first()
    #while iter:
        #print (iter)
        #iter = cursor.next()
    
    db_pterms.close()
    
def rterm():
    db_rterms = db.DB()
    database = 'rt.idx'
    db_rterms.set_flags(db.DB_DUPSORT) 
    db_rterms.open(database, None, db.DB_BTREE, db.DB_CREATE)
    
    try:
        file= open("rterms.txt","r")
        new_file = open("rterms_new.txt", "w")
    except IOError:
        print("Error opening file")
    else:
        for line in file:
            line= line.split(",",1)  
            new_file.write(line[0] + "\n" + line[1])
            
    file.close()
    new_file.close()    
    
    cursor = db_rterms.cursor()    
    subprocess.call(["db_load -T -t btree -f rterms_new.txt rt.idx"], shell=True)    
    
    #iter = cursor.first()
    #while iter:
        #print (iter)
        #iter = cursor.next()
    
            
    db_rterms.close()
    
    
def scores():
    db_scores = db.DB()
    database = 'sc.idx'
    db_scores.set_flags(db.DB_DUPSORT)   
    
    db_scores.open(database, None, db.DB_BTREE, db.DB_CREATE)   
    
    try:
        file= open("scores.txt","r")
        new_file = open("scores_new.txt", "w")
    except IOError:
        print("Error opening file")
    else:
        for line in file:
            line= line.split(",",1)   
            new_file.write(line[0] + "\n" + line[1])
            
    file.close()
    new_file.close()    
    
    
    #cursor = db_scores.cursor() 
    subprocess.call(["db_load -T -f scores_new.txt -t btree sc.idx"], shell=True)
    
    #iter=cursor.first()    
    #while iter:
    #    print(iter)
    #    iter = cursor.next()
    
    #cursor.close()
    db_scores.close()      
    
    return   
def removing():
    try:
        os.remove("sc.idx")
        os.remove("pt.idx")
        os.remove("rw.idx")
        os.remove("rt.idx")
    except:
        return

def main():
    print("-----Beginning Phase 2-----\n")
    
    removing()
        
    #Create sorted files
    subprocess.call(["sort -u -o pterms.txt pterms.txt"], shell=True)
    subprocess.call(["sort -u -o rterms.txt rterms.txt"], shell=True)
    subprocess.call(["sort -u -o scores.txt scores.txt"], shell=True)
        
    review()
    print("rw.idx created.")    
    pterm()
    print("pt.idx created.")    
    rterm()
    print("rt.idx created.")    
    scores()
    print("sc.idx created.")    
    
    print("-----Complete Phase 2-----")
    
main()