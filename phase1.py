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
import string

def openfile():
#opens customers.txt and stores name and city with phone number as key
    raw=[]
    file = input("Enter in file to prepare: ")
    try: 
        file= open(file, "r")
        print("Creating files.")
    #if file doesn't exist
    except:
        return None
    #if file exists
    else:
        #Formating file to be processed
        number=1
        for line in file:
            line= line.strip()
            line=line.replace('"',' &quot ')
            line=line.replace('\\' , '\\\\')
            raw.append(line)
        file.close()
        return raw
    
    
def reviews(raw):      
    count=1
    i=0
    string=''
    try:
        file= open('reviews.txt', "w")
    except IOError:
        print("This really shouldn't happen")
    else:
        string+= str(count)         
        for line in raw:
            lines= line.split(":",1)
            if lines[0]== '':
                file.write(string)
                file.write("\n")
                count+=1                
                string=''
                string+= str(count)
            else:
                if lines[0]=='product/title':
                    string+=',"'
                    string+= str(lines[1].strip()) 
                    string+='"'                    
                elif lines[0]=='review/profileName':
                    string+=',"'
                    string+= str(lines[1].strip()) 
                    string+='"' 
                elif lines[0]=='review/summary':
                    string+=',"'
                    string+= str(lines[1].strip()) 
                    string+='"' 
                elif lines[0]=='review/text':
                    string+=',"'
                    string+= str(lines[1].strip()) 
                    string+='"' 
                else:
                    string+= ','
                    string+= str(lines[1].strip()) 
        try: 
            string=int(string)
            file.close()
            return
        except:
            file.write(string)
            file.close()


def pterms(raw):
    try: 
        file= open('pterms.txt', "w")
    #if file doesn't exist
    except IOError:
        print("Error with file")
    count=1
    for line in raw:
        lines=line.split(': ', 1 )
        if lines[0] == 'product/title':
            words=''
            for char in lines[1]:
                if char.isalnum() or char.isspace():
                    words+=char
                else:
                    words+=' '
            words=words.split(" ")
            for word in words:
                if len(word) >2:
                    file.write(word.lower()+","+str(count)+'\n')
        elif lines[0]== '':
            count+=1
    file.close()
    return

def rterms(raw):
    try: 
        file= open('rterms.txt', "w")
    #if file doesn't exist
    except IOError:
        print("Error with file")
    count=1
    for line in raw:
        lines=line.split(': ', 1 )
        if lines[0] == 'review/summary' or lines[0] == 'review/text' :
            words=''
            for char in lines[1]:
                if char.isalnum() or char.isspace():
                    words+=char
                else:
                    words+=' '
            words=words.split(" ")
            for word in words:
                if len(word) >2:
                    file.write(word.lower()+","+str(count)+'\n')
        elif lines[0]== '':
            count+=1
    file.close()
    return

def scores(raw):
    try: 
        file= open('scores.txt', "w")
    #if file doesn't exist
    except IOError:
        print("Error with file")
    count=1
    for line in raw:
        lines=line.split(': ', 1 )
        if lines[0] == 'review/score':
            file.write(lines[1]+","+str(count)+'\n')
        elif lines[0]== '':
            count+=1            
    file.close()    
    return  

def main():
    print("-----Beginning Phase 1-----")    
    raw=openfile()
    if raw == None:
        print ("File does not exist.")
        main()
    else:
        reviews(raw)
        print("reviews.txt created.")
        pterms(raw)
        print("pterms.txt created.")
        rterms(raw)
        print("rterms.txt created.")
        scores(raw)
        print("scores.txt created.")
        print("-----Complete Phase 1-----")
        
        return

main()