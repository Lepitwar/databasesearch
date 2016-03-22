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
from bsddb3 import db 
import os
import datetime
import time
import sys

#Takes and formats user input
def inputs():    
    cmd= []
    grt=[]
    less=[]
    col=[]
    word=[]
    i= -1
    user= input("Enter query: ")
    user= user.strip()
    user= user.split(" ")
    #formatting input
    for item in user:
        if item != '':
            taken=False
            for k,j in enumerate(item):
                if j =='>' or j =='<' or j ==':':
                    taken=True
                    if item[:k]!='':
                        cmd.append(item[:k].lower())
                    cmd.append(item[k].lower())
                    if item[k+1:]!='':
                        cmd.append(item[k+1:].lower()) 
            if not taken:
                cmd.append(item.lower())              
    nex=False 
    for item in cmd:
        i+=1
        if item== '>':                
            grt.append(cmd[i-1])
            grt.append(cmd[i+1])
            word.pop()
            cmd[i+1]=''
        elif item== '<':
            less.append(cmd[i-1])
            less.append(cmd[i+1])
            word.pop()
            cmd[i+1]=''
        elif item== ':':
            col.append(cmd[i-1])
            col.append(cmd[i+1])
            word.pop()
            cmd[i+1]=''
        elif item!='':
            word.append(item)
    return grt, less, col, word

#Finds words in product title/review summary/text
def searching(word,index, wild):
    ItemList=[]
    partial=False
    results=[]
    Missing=[]
    database = db.DB() 
    database.open(index)
    cursor=database.cursor()
    for i in word:
        if '%' in i:
            partial=True
            i=i[:-1]            
        if not partial:
            var=bytes(i, 'utf-8')
            if var in database:
                results=cursor.get(var, db.DB_SET)
                ItemList.append(results[1].decode("utf-8"))
                for x  in range(cursor.count()-1):
                    ItemList.append(cursor.next_dup()[1].decode("utf-8"))
            else:
                if wild:
                    Missing.append(i)
                else:
                    print("No results were found")
                    cursor.close()
                    database.close()
                    sys.exit
        else:
            var=bytes(i, 'utf-8')
            item= cursor.get( var, db.DB_SET_RANGE)
            results.append(item[1].decode("utf-8"))
            Stopping=False
            while not Stopping:
                item = cursor.next()
                if var in item[0]:
                    if item[1].decode("utf-8") not in results:
                        results.append(item[1].decode("utf-8"))
                else:
                    Stopping=True
                    ItemList=results
    
    cursor.close()
    database.close()
    if wild:
        return ItemList, Missing
    else:
        return ItemList

#Prints results
def returnReveiws(ItemList):
    print("~~~~~~~~~~~~~~~~~~~~")
    print("Your search results:")
    database = db.DB() 
    database.open('rw.idx')
    cursor = database.cursor()
    i=1
    for item in ItemList:
        var=bytes(item, 'utf-8')
        if var in database:
            print(i,database[var].decode("utf-8"))
        else:
            print(i,cursor.last()[1].decode("utf-8"))
        i+=1
    cursor.close()
    database.close()
    return

#Finds results of operator queries
def Separator(Items,X):
    if X=='<':
        less=True
    else:
        less=False
        
    rscore=[]
    rdate=[]
    pprice=[]
    ItemSet=[]
    count=0 
    #the current modifier
    currentRS=''
    currentRD=''
    currentPP=''
    #Checks all the modifies
    while count < len(Items):
        contin=False       
        #RSCORE
        if Items[count]=='rscore':            
            if currentRS=='':
                contin=True
                currentRS=Items[count+1]
            #checking to replace
            if not contin:
                if less:
                    if Items[count+1] < currentRS:  
                        contin=True
                        currentRS=Items[count+1]
                else:
                    if Items[count+1] > currentRS:  
                        contin=True
                        currentRS=Items[count+1]
            #if replacement if a go-ahead
            if contin:   
                #rscore.append(Items[count+1])
                if less:
                    rscore=lesser(currentRS,'sc.idx')
                else:
                    rscore=greater(currentRS,'sc.idx')
        #RDATE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
        elif Items[count]=='rdate':
            if currentRD=='':
                contin=True
                currentRD=Items[count+1]
            #checking to replace
            if not contin:
                if less:
                    if Items[count+1] < currentRD:  
                        contin=True
                        currentRD=Items[count+1]
                else:
                    if Items[count+1] > currentRD:  
                        contin=True
                        currentRD=Items[count+1]
            #if replacement if a go-ahead
            if contin:               
                if less:
                    database = db.DB() 
                    database.open('rw.idx', None, db.DB_HASH, db.DB_RDONLY)                    
                    curs = database.cursor()                    
                    iter = curs.first()
                    i=1
                    while iter:
                        gate= (iter[1].decode("utf-8")).split('"')  
                        gate= (gate[4].split(','))
                        if currentRD> datetime.datetime.fromtimestamp(int(gate[3])).strftime('%Y/%m/%d'):                            
                            rdate.append(iter[0].decode("utf-8"))                     
                            i+=1
                        iter=curs.next()   
                    gate= curs.last()[1].decode("utf-8").split('"')   
                    gate= (gate[4].split(','))       
                    if currentRD> datetime.datetime.fromtimestamp(int(gate[3])).strftime('%Y/%m/%d'):
                        rdate.append(curs.last()[0].decode("utf-8"))  
                else:                    
                    database = db.DB() 
                    database.open('rw.idx', None, db.DB_HASH, db.DB_RDONLY)                    
                    curs = database.cursor()
                    
                    iter = curs.first()
                    i=1
                    while iter:
                        gate= (iter[1].decode("utf-8")).split('"')  
                        gate= (gate[4].split(','))
                        if currentRD< datetime.datetime.fromtimestamp(int(gate[3])).strftime('%Y/%m/%d'):
                            rdate.append(iter[0].decode("utf-8"))  
                            i+=1
                        iter=curs.next() 
                    gate= curs.last()[1].decode("utf-8").split('"')   
                    gate= (gate[4].split(','))       
                    if currentRD< datetime.datetime.fromtimestamp(int(gate[3])).strftime('%Y/%m/%d'):
                        rdate.append(curs.last()[0].decode("utf-8"))                         
                                        
        #PPRICE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`   
        elif Items[count]=='pprice':            
            if currentPP=='':
                contin=True
                currentPP=Items[count+1]
            #checking to replace
            if not contin:
                if less:
                    if Items[count+1] < currentPP:  
                        contin=True
                        currentPP=Items[count+1]
                else:
                    if Items[count+1] > currentPP:  
                        contin=True
                        currentPP=Items[count+1]
            #if replacement if a go-ahead
            if contin:    
                if less:
                    database = db.DB() 
                    database.open('rw.idx', None, db.DB_HASH, db.DB_RDONLY)                    
                    curs = database.cursor()                    
                    iter = curs.first()
                    i=1
                    z=0
                    while iter:
                        gate= (iter[1].decode("utf-8")).split('"')  
                        gate= (gate[2].split(','))
                        if gate[1]!= 'unknown' and currentPP>= gate[1]:
                            pprice.append(iter[0].decode("utf-8"))
                            i+=1        
                        iter=curs.next()
                    gate= curs.last()[1].decode("utf-8").split('"')   
                    gate= (gate[2].split(','))       
                    if gate[1]!= 'unknown' and currentPP>= gate[1]:
                        pprice.append(curs.last()[0].decode("utf-8"))  
                else:
                    database = db.DB() 
                    database.open('rw.idx', None, db.DB_HASH, db.DB_RDONLY)                    
                    curs = database.cursor()                    
                    iter = curs.first()
                    i=1
                    while iter:
                        gate= (iter[1].decode("utf-8")).split('"')  
                        gate= (gate[2].split(','))
                        if gate[1]!= 'unknown' and currentPP< gate[1]:   
                            pprice.append(iter[0].decode("utf-8"))
                            i+=1        
                        iter=curs.next()                 
                    gate= curs.last()[1].decode("utf-8").split('"')   
                    gate= (gate[2].split(','))       
                    if gate[1]!= 'unknown' and currentPP< gate[1]:
                        pprice.append(curs.last()[0].decode("utf-8"))                       
        count+=2
    
    return rscore, rdate, pprice

#Finds values greater for rscore
def greater(Items,index):
    valid=False
    if index=='NONE':
        return      
    ItemSet=[]
    database = db.DB() 
    database.open(index)
    cursor = database.cursor()
    while not valid:
        Items=float(Items[0])+1
        var=bytes(str(Items), 'utf-8')
        if var in database:
            valid=True
        if Items>5:
            #NO RESULTS WERE FOUND
            return []
        
    item=cursor.get(var, db.DB_SET)
    while item != None:
        ItemSet.append(item[1].decode('utf-8'))
        item = cursor.next()
        
    return ItemSet

#Finds values less than for rscore
def lesser(Items,index):
    valid=False
    if index=='NONE':
        return        
    ItemList=[]
    database = db.DB() 
    database.open(index)
    cursor = database.cursor()
    while not valid:
        Items=int(Items)-1.0
        var=bytes(str(Items), 'utf-8')
        if var in database:
            valid=True
        if Items<1:
            #NO RESULTS WERE FOUND
            return []
        
    results=cursor.get(var, db.DB_SET)
    ItemList.append(results[1].decode("utf-8"))
    for x  in range(cursor.count()-1):
        ItemList.append(cursor.next_dup()[1].decode("utf-8"))
    results=cursor.get(var, db.DB_SET)
    
    item=cursor.get(var, db.DB_SET)
    while item != None:
        ItemList.append(item[1].decode('utf-8'))
        item = cursor.prev()
    return ItemList

#Merges two lists together
def merge(Item1, Item2):
    if len(Item1)==0 or len(Item2)== 0:
        Item3= Item1 + Item2
        return Item3
    Item3=[]
    Item3=list(set(Item1) & set(Item2))
    return Item3

#Takes queries and calls appropriate functions
def queires(grt, less, col, word):
    products=[]
    reviews=[]
    ItemList=[]
    word1=[]
    word2=[]
    missing=[]
    Items1=[]
    Items2=[]
    Items3=[]
    Items4=[]
    rscore, rdate, pprice=Separator(grt,'>')
    rscore1, rdate1, pprice1=Separator(less,'<')  
    rscore=merge(rscore, rscore1)
    rdate=merge(rdate, rdate1)
    pprice=merge(pprice, pprice1)    
    #we split the col in to their respective lists
    count=0
    while count < len(col):
        if col[count]=='p':
            products.append(col[count+1])
        else:
            reviews.append(col[count+1])
        count+=2
    #Making Duplicates of word   
    for item in word:
        word1.append(item)
        word2.append(item)
    #We check Pterms
    if len(products) != 0:
        Items1=searching(products,'pt.idx',False)
    #We check rterms
    if len(reviews) != 0: 
        Items2=searching(reviews,'rt.idx',False)
    #We check words
    if len(word) != 0:
        Items3,missing=searching(word,'pt.idx',True)
        Items4,missing1=searching(word,'rt.idx',True)
    #If an item is not found in both seaches     
    for item in missing:
        if item in missing1:
            print("NO RESULTS WERE FOUND")
            return
    Items3+=Items4
    #removes the voids from item 3
    while "VOID" in Items3:
        Items3.remove("VOID")
    #checks for voids, if it has a void then it wasn't found
    if "VOID" in Items1 or "VOID" in Items2 or "VOID" in Items3 :
        print("NO RESULTS WERE FOUND")
        return
    #Setting each Item set to True
    pt=True
    rt=True
    wild=True
    rs=True
    pp=True
    rd=True     
    #If they are empty, they get filled with the others
    if len(Items1)==0:
        Items1+=Items2+Items3+rscore+rdate+pprice
        pt=False
    if len(Items2)==0:
        Items2+=Items1+Items3+rscore+rdate+pprice
        rt=False   
    if len(Items3)==0:
        Items3+=Items1+Items2+rscore+rdate+pprice
        wild=False
    if len(rscore)==0:
        rscore+=Items3+Items1+Items2+rdate+pprice
        rs=False
    if len(rdate)==0:
        rdate+= Items3 +Items1+Items2+rscore+pprice
        rd=False
    if len(pprice)==0:
        pprice+=Items3 +Items1+Items2+rscore+rdate
        pp=False
        
    #If All are empty
    if not rt and not pt and not wild and not rs and not pp and not rd:
        print("NO RESULTS WERE FOUND")
        return
       
    masterlist=list(set(Items1) & set(Items2) &set(Items3) &set(rscore) &set(pprice) &set(rdate))    
    #We return the reveiws from all the queires  
    if len(masterlist)==0:
        print("NO RESULTS WERE FOUND")
        return
    else:         
        returnReveiws(masterlist)        
        return

def main():
    loop=True
    while(loop){
        grt, less, col, word=inputs()
        queires(grt, less, col, word)
    }
    
main()
print("-----Query Completed-----")