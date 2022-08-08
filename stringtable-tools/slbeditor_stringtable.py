#############################
#Stringtable editor tool    #
#in python                  #
#Made by OndrikB            #
#############################
#----imports----
import math
import sys
#----variables----

slbParse = []

stringGroups = [] 
stringTempName = "" 
stringTempString = "" 

groupCount = 0

groupChosen = -1
stringChosen = -1

if len(sys.argv) >= 2:
    choice1 = "N"
else:
    choice1 = str(input("Create a new SLB (Y/N): "))
if choice1 == "N":
    pointer = 0
    if len(sys.argv) >= 2:
        slbInt = open(sys.argv[1],"rb").read()
    else:
        slbOpen = str(input("SLB file name here: "))
        slbInt = open(slbOpen,"rb").read()
    slbIntList = []


#----functions----
def forChar(string):  #foreign characters (unused)
    a = string
    b = len(a)
    for i in range(b):
        if a[i] == 'ü':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('48',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'u'
            i = 0
            a = "".join(a)
        if a[i] == 'ä':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('48',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'a'
            i = 0
            a = "".join(a)
        if a[i] == 'ö':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('48',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'o'
            i = 0
            a = "".join(a)
        if a[i] == 'á':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('42',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'a'
            i = 0
            a = "".join(a)
        if a[i] == 'é':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('42',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'e'
            i = 0
            a = "".join(a)
        if a[i] == 'í':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('42',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'i'
            i = 0
            a = "".join(a)
        if a[i] == 'ó':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('42',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'o'
            i = 0
            a = "".join(a)
        if a[i] == 'ú':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('42',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'u'
            i = 0
            a = "".join(a)
        if a[i] == 'ý':
            a = a[:i] + chr(int('1b',16)) + chr(int('4e',16)) + chr(int('42',16)) + a[i:]
            a = list(a)
            b = len(a)
            a[i+3] = 'y'
            i = 0
            a = "".join(a)
        if a[i] == 'ñ':
            a = list(a)
            a[i] = 'n'
            a = "".join(a)
    return a
def fullForChar(string): #more foreign characters (unused)
    a = string
    while ('ü' in a) or ('ä' in a) or ('ö' in a) or ('á' in a) or ('é' in a) or ('í' in a) or ('ó' in a) or ('ú' in a) or ('ý' in a) or ('ñ' in a): 
        a = forChar(a)
    return a
def oForChar(string): 
    a = list(string)
    b = len(string)
    code1 = chr(int('1b',16))
    code2 = chr(int('4e',16))
    codeUmlaut = chr(int('48',16))
    codeChar1 = chr(int('42',16))
    print(b)
    if b >= 4: 
        for i in range(3,b):
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeUmlaut) and (a[i] == 'u'):
                a = list(a)
                a[i] = 'ü'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeUmlaut) and (a[i] == 'o'):
                a = list(a)
                a[i] = 'ö'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeUmlaut) and (a[i] == 'a'):
                a = list(a)
                a[i] = 'ä'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeChar1) and (a[i] == 'a'):
                a = list(a)
                a[i] = 'á'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeChar1) and (a[i] == 'e'):
                a = list(a)
                a[i] = 'é'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeChar1) and (a[i] == 'i'):
                a = list(a)
                a[i] = 'í'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeChar1) and (a[i] == 'o'):
                a = list(a)
                a[i] = 'ó'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeChar1) and (a[i] == 'u'):
                a = list(a)
                a[i] = 'ú'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
            if (a[i-3] == code1) and (a[i-2] == code2) and (a[i-1] == codeChar1) and (a[i] == 'y'):
                a = list(a)
                a[i] = 'ý'
                a.pop(i-3)
                a.pop(i-3)
                a.pop(i-3)
    if b >= 3:
        for i in range(2,b):
            if (a[i-2] == code1) and (a[i-1] == chr(int('28',16))) and (a[i] == '5'): #this works
                a = list(a)
                a[i] = '.'
                a[i-1] = '.'
                a[i-2] = '.'
            if (a[i-2] == code1) and (a[i-1] == chr(int('28',16))) and (a[i] == '2'): #this does not work
                a = list(a)
                a[i] = '\''
                a.pop(i-2)
                a.pop(i-2)
            if (a[i-2] == code1) and (a[i-1] == chr(int('28',16))) and (a[i] == '6'): #this doesn't either
                a = list(a)
                a[i] = '-'
                a.pop(i-2)
                a.pop(i-2)
    a = "".join(a)
    return a
def fullOForChar(string):
    a = list(string)
    code = chr(int('1b',16))
    b = a
    c = code
    while b != c:
        b = a
        a = oForChar(a)
        c = a
    a = "".join(a)
    return a
def conversion(pointer): #slb -> value
    a = 0
    for i in range(4):
        a += (slbIntList[pointer+i]*(256**i))
    return a
def deconversion(var,pointer):  #value -> slb
    global slbParse
    s = var.to_bytes(4,byteorder='little')
    for i in range(4):
        slbParse[pointer+i] = s[i]
def slbAppend(var): #appends x bytes to slb
    global slbParse
    for i in range(var):
        slbParse.append(0)
def acount(chosen): #counts up group entries
    a = 0
    if chosen >= 1:
        for i in range(chosen):
            a += stringGroups[i].entryCount
    return a
def parseSLB(newSlbName): #new SLB creation
    #usage of existing variables
    global groupCount
    global stringGroups
    global slbParse
    #declaring new variables
    pointer = 0
    #pointers
    bottomPointers = [] #footer (points to groups)
    midPointers = [] #points to strings
    topPointers = [] #points to mid
    slbAppend(4)
    deconversion(groupCount,pointer)
    slbAppend(4)
    pointer += 4
    deconversion(8,pointer)
    bottomPointers.append(pointer)
    pointer += 4
    slbAppend(groupCount*16)
    #for i in range(groupCount):
    #    for l1 in range(stringGroups[i].entryCount):
    #        stringGroups[i].strings[l1] = stringGroups[i].strings[l1]
    for i in range(groupCount):
        for l1 in range(4): #name writing
            l = list(stringGroups[i].name)
            slbParse[pointer+3-l1] = ord(l[l1]) 
        pointer += 4 #add to pointer (overwrite protection)
        deconversion(stringGroups[i].ID,pointer) #ID writing
        pointer += 4 
        deconversion(stringGroups[i].entryCount,pointer) #entry count writing
        pointer += 4 
        deconversion(0,pointer) #will be pointer
        bottomPointers.append(pointer)
        pointer += 4 
    allEntries = acount(groupCount) #counts all strings
    slbAppend(allEntries*4) 
    for i in range(allEntries):
        deconversion(0,pointer) #will be pointer 
        bottomPointers.append(pointer)
        pointer += 4
    pointStrings = pointer #the point where strings start
    lengths = 0 #all lengths get counted up here
    slbAppend(2*allEntries) #... why
    for i in range(groupCount): #for every group
        for l1 in range(stringGroups[i].entryCount):
            slbParse[pointStrings+lengths] = len(stringGroups[i].strings[l1]) #length byte
            slbAppend(len(stringGroups[i].strings[l1])) #appends info
            pointer = pointStrings+lengths+1 #sets pointer
            midPointers.append(pointStrings+lengths) #mid pointer
            if l1 == 0: #if it's the first string
                topPointers.append(8+(groupCount*16)+(acount(i)*4)) #8 = bytes until start of groups , group bytes, count up of pointer bytes by acount()
            for l2 in range(len(stringGroups[i].strings[l1])):  #for every character in the string
                listString = list(stringGroups[i].strings[l1]) #list gets created
                slbParse[l2+pointer] = ord(listString[l2]) #string is written 1 by 1
                spoint = l2+pointer #string pointer is recreated
            slbParse[spoint+1] = 0 #null terminator is set
            lengths += len(stringGroups[i].strings[l1])+2  #length of string + string + null get added to length countup (pointer)
    pointer = 20 #first group pointer entry
    for i in range(groupCount): #for every group
        deconversion(topPointers[i],pointer) #top pointer gets written
        pointer += 16 #pointer added
    pointer = 8+16*groupCount  #8 = bytes until start of group + group bytes = start of mid pointers
    for i in range(allEntries): #for every string
        deconversion(midPointers[i],pointer) #mid pointer written
        pointer += 4 #pointer added
    finalPointer = spoint+2 #taking spoint from the string writing + length byte + null terminator
    pointer = finalPointer #setting pointer
    while pointer % 4 != 0: #making sure that it doesn't crash
        slbAppend(1)
        pointer += 1
    for i in range(len(bottomPointers)): #footer
        slbAppend(4)
        deconversion(bottomPointers[i],pointer) #writing
        pointer += 4
    slbAppend(4) #length of footer
    deconversion(len(bottomPointers),pointer) #written
    pointer += 4 #pointer increased
    slbAppend(4) #signature
    slbParse[pointer] = 238 #EE
    slbParse[pointer+1] = 255 #FF
    slbParse[pointer+2] = 192 #C0
    slbParse[pointer+3] = 0 #finished
    newSlb = open(newSlbName, "wb") #opening file
    for i in range(len(slbParse)): #checking for apostrophe
        if chr(slbParse[i]) == '’':
            slbParse[i] = ord('\'') #replacing with game-readable version
    slbWriteList = bytearray(slbParse) #conversion to byte array
    newSlb.write(slbWriteList) #writing
    newSlb.close() #done
    #---END---
def newEntry(groupSelected):
    global stringGroups
    print("Entry add mode. What would you like to enter into group ",stringGroups[groupSelected].name," ",stringGroups[groupSelected].ID,"?",sep="")
    newEntryName = str(input())
    if len(newEntryName) >= 256: 
        print("Warning! String entry is too long! Please input again.")
        newEntry(groupSelected)
    elif len(newEntryName) != 0:
        stringGroups[groupSelected].addNew(0,len(newEntryName),newEntryName)
        stringGroups[groupSelected].entryCount += 1
        newEntry(groupSelected)
    else:
        print("Taking to group choice mode.")
        groupChoice()
def nGroupFile(groupSelected):
    global groupCount
    gSO = groupCount
    fileRead = str(input("File name to enter from? "))
    if len(fileRead) == 0:
        print("Name invalid.")
        nGroupFile(groupSelected)
    else:
        with open(fileRead, "r",encoding="ANSI") as f:
            file = []
            new = 0
            for line in f:
                file.append(line)
            for i in range(len(file)):
                file[i] = file[i].rstrip("\n")
            for i in range(len(file)):
                if len(file[i]) != 0 and len(file[i]) != 1:
                    stringGroups[groupSelected].addNew(0,len(file[i]),file[i])
                    stringGroups[groupSelected].entryCount += 1
                if len(file[i]) == 1:
                    new = 1
                    newGroupID = 1
                    for l1 in range(groupCount):
                        if stringGroups[groupSelected].name == stringGroups[l1].name:
                            newGroupID += 1
                    stringGroups.append(stringGroupTable(stringGroups[groupSelected].name,newGroupID,0,0,1))
                    groupCount += 1
                    stSel = 0
                    groupSelected += 1
    groupChoice()
def newGroup():
    global groupCount
    global stringGroups
    newGroupName = str(input("What's the name of your new group? "))
    if len(newGroupName) < 4:
        print("Your group name is too short. Please try again (Group name length must be 4)")
        newGroup()
    if len(newGroupName) > 4:
        print("Your group name is too long. Please try again (Group name length must be 4)")
        newGroup()
    newGroupID = 1
    for i in range(groupCount):
        if newGroupName == stringGroups[i].name:
            newGroupID += 1
    stringGroups.append(stringGroupTable(newGroupName,newGroupID,0,0,1))
    groupCount += 1
    print("New group (",stringGroups[groupCount-1].name," ",stringGroups[groupCount-1].ID,"), has been created.",sep="")
    choice2 = str(input("Do you want to enter the text into the group from a file? (Y/N): "))
    if choice2 == "Y":
        nGroupFile(groupCount-1)
    else:
        newEntry(groupCount-1)
def deletGroup(groupChosen):
    global groupCount
    global stringGroups
    choice = str(input("Should the entries carry over to a different group? (Y/N): "))
    if choice == "Y":
        newEntriesGroup = int(input("What number group? "))
        if newEntriesGroup >= groupCount+1 or newEntriesGroup <= -1:
            print("Invalid group chosen, entries will carry over to next.")
            newEntriesGroup = groupChosen+2
        newEntriesGroup -= 1
        for i in range(stringGroups[groupChosen].entryCount):
            stringGroups[newEntriesGroup].addNew(0,len(stringGroups[groupChosen].strings[i]),stringGroups[groupChosen].strings[i])
        stringGroups[newEntriesGroup].entryCount += stringGroups[groupChosen].entryCount
    stringGroups.pop(groupChosen)
    groupCount -= 1
    groupChoice()
def editEntry(groupChosen,stringChosen):
    print("Entry editing mode. Entry ",stringChosen+1," in group ",groupChosen+1," (",stringGroups[groupChosen].name," ",stringGroups[groupChosen].ID,"), (",stringGroups[groupChosen].strings[stringChosen],") is to be edited. What do you want to replace it with? ",sep="")
    newEntryName = str(input())
    if len(newEntryName) >= 256:
        print("Warning! String entry is too long! Please input again.")
        editEntry(groupChosen,stringChosen)                  
    stringGroups[groupChosen].strings[stringChosen] = newEntryName
    stringGroups[groupChosen].lengths[stringChosen] = len(newEntryName)
    groupChoice()
def stringOut(groupChoose,output):
    with open(output, 'a') as the_file:
        for i in range(stringGroups[groupChoose].entryCount):
            newstring = stringGroups[groupChoose].strings[i]
            the_file.write((newstring+'\n'))
    the_file.close()
    groupChoice()
def enterGroup(groupSelected):
    fileRead = str(input("File name to enter from? "))
    if len(fileRead) == 0:
        print("Name invalid.")
        groupChoice()
    else:
        with open(fileRead, "r",encoding="ANSI") as f:
            file = []
            for line in f:
                file.append(line)
            for i in range(len(file)):
                file[i] = file[i].rstrip("\n")
            for i in range(stringGroups[groupSelected].entryCount):
                if len(file[i]) != 0:
                    stringGroups[groupSelected].strings[i] = file[i]
                    stringGroups[groupSelected].lengths[i] = len(file[i])
    groupChoice()
def dmpStbl():
    global groupCount
    fileRead = str(input("File name to put to? "))
    if len(fileRead) == 0:
        print("Name invalid.")
        groupChoice()
    else:
        with open(fileRead, 'a',encoding='utf-8') as the_file:
            for i in range(groupCount):
                for l1 in range(stringGroups[i].entryCount):
                    newstring = stringGroups[i].strings[l1]
                    the_file.write((newstring+'\n'))
    the_file.close()
    groupChoice()
def repStbl():
    print("Total string amount: "+str(acount(groupCount)))
    fileRead = str(input("File name to enter from? "))
    if len(fileRead) == 0:
        print("Name invalid.")
        nGroupFile(groupSelected)
    
    else:
        with open(fileRead, "r",encoding="ANSI") as f:
            file = []
            for line in f:
                file.append(line)
            for i in range(len(file)):
                file[i] = file[i].rstrip("\n")
            for i in range(len(file)):
                if len(file[i]) >= 256:
                    print("!Too long!",file[i])
            for i in range(groupCount):
                for l1 in range(stringGroups[i].entryCount):
                    print(acount(i)+l1)
                    stringGroups[i].strings[l1] = file[acount(i)+l1]
                    stringGroups[i].lengths[l1] = len(file[acount(i)+l1])
    groupChoice()
def groupChoice():
    global groupCount
    global stringGroups
    for i in range(groupCount):
            print("String group ",i+1," (",stringGroups[i].name," ",stringGroups[i].ID,"), ",stringGroups[i].entryCount," entries",sep="")
    choice1 = str(input("Done? (Y/N): "))
    if choice1 == "N":
        choiceAll = str(input("Input stringtable to file? (Y/N): "))
        if choiceAll == "Y":
            dmpStbl()
        choiceRep = str(input("Replace stringtable with file? (Y/N): "))
        if choiceRep == "Y":
            repStbl()
        choice2 = str(input("Add new group? (Y/N): "))
        if choice2 == "Y":
            newGroup()
        elif choice2 == "N":
            groupChosen = int(input("Choose a group: "))
            groupChosen -= 1
            if groupChosen <= -1 or groupChosen >= groupCount:
                print("Invalid group selected, taking first")
                groupChosen = 0
            print("String group ",groupChosen+1," (",stringGroups[groupChosen].name," ",stringGroups[groupChosen].ID,"), ",stringGroups[groupChosen].entryCount," entries",sep="")
            if groupCount != 1:
                choice4 = str(input("Delete this group? (Y/N): "))
            else:
                choice4 = "N"
            if choice4 == "Y":
                deletGroup(groupChosen)
            if choice4 == "N":
                strAll = str(input("Show all strings? (Y/N): "))
                if strAll == "Y":
                    for i in range(stringGroups[groupChosen].entryCount):
                        print(stringGroups[groupChosen].strings[i])
                    choiceIdk = str(input("Put group to file? (Y/N) "))
                    if choiceIdk == "Y":
                        txtOut = str(input("File name to write group to? (blank to cancel): "))
                        if len(txtOut) != 0:
                            stringOut(groupChosen,txtOut)
                    else:
                        groupChoice()
                elif strAll == "N":
                    choiceOther = str(input("Replace group with file input? (Y/N) "))
                    if choiceOther == "Y":
                        enterGroup(groupChosen)
                    if choiceOther == "N":   
                        choice3 = str(input("Add new string? (Y/N): "))
                        if choice3 == "Y":
                            newEntry(groupChosen)
                        elif choice3 == "N":
                            stringChosen = int(input("Choose a string: "))
                            stringChosen -= 1
                        if stringChosen <= -1 or stringChosen >= stringGroups[groupChosen].entryCount:
                                print("Invalid string selected, taking first")
                                stringChosen = 0
                        print("String ",stringChosen+1,", Length: ",stringGroups[groupChosen].lengths[stringChosen],", Text: \"",stringGroups[groupChosen].strings[stringChosen],"\"",sep="")
                        if stringGroups[groupChosen].entryCount >= 1:
                            choice6 = str(input("Move/Remove this string? (Y/N): ")) 
                        else:
                            choice6 = "N"
                        if choice6 == "N": 
                            choice5 = str(input("Edit this string? (Y/N): "))
                            if choice5 == "Y":
                                editEntry(groupChosen,stringChosen)
                            if choice5 == "N":
                                groupChoice()
                            else:
                                print("Please choose Y or N")
                                groupChoice()
                        if choice6 == "Y":
                            num = str(input("Which group do you want this string moved to? (don't input anything to delete string entirely): "))
                            if num == "":
                                stringGroups[groupChosen].entryCount -= 1
                                stringGroups[groupChosen].removeString(stringChosen)
                            num2 = int(num)
                            num2 -= 1
                            if num2 <= -1 or num2 >= groupCount:
                                print("Moving to invalid group. Move cancelled")
                            else:
                                stringGroups[num2].entryCount += 1
                                stringGroups[num2].addNew(0,len(stringGroups[groupChosen].strings[stringChosen]),stringGroups[groupChosen].strings[stringChosen])
                                stringGroups[groupChosen].entryCount -= 1
                                stringGroups[groupChosen].removeString(stringChosen)
                            groupChoice()
                        else:
                            print("Please choose Y or N")
                            groupChoice()
                    else:
                        print("Please choose Y or N")
                        groupChoice()
                else:
                    print("Please choose Y or N")
                    groupChoice()
        else:
            print("Please choose Y or N")
            groupChoice()
    elif choice1 == "Y":
        newSlbName = str(input("Name of new SLB file? (blank to not write) "))
        for l1 in range(groupCount):
            for l2 in range(stringGroups[l1].entryCount):
                if len(stringGroups[l1].strings[l2]) >= 256:
                    print("String "+stringGroups[l1].strings[l2]+" is too long!")
                for l3 in range(len(stringGroups[l1].strings[l2])):
                    if ord(stringGroups[l1].strings[l2][l3]) >= 256:
                        print("Character "+stringGroups[l1].strings[l2][l3]+"in string \""+stringGroups[l1].strings[l2]+"\" is too big!")
        if len(newSlbName) != 0:
            parseSLB(newSlbName)
        sys.exit()
    else:
        print("Please choose Y or N")
        groupChoice()
#----classes----
class stringGroupTable:
    def __init__(self,name,num,count,point,new):
        self.name = name
        self.ID = num
        self.entryCount = count
        self.pointerPointer = point
        self.edited = new
        self.pointers = []
        self.lengths = []
        self.strings = []
    def addNew(self,pointer,length,pstringn):
        self.pointers.append(pointer)
        self.lengths.append(length)
        self.strings.append(pstringn)
    def removeString(self,address):
        self.pointers.pop(address)
        self.lengths.pop(address)
        self.strings.pop(address)
#----main----
if choice1 == "N":
    for b in slbInt:
        slbIntList.append(b)
    pointer = 0
    groupCount = conversion(pointer)
    pointer += 4
    bodyOffset = conversion(pointer)
    pointer = bodyOffset
    for i in range(groupCount): 
        for l1 in range(4):
            stringTempName += str(chr(slbIntList[pointer+3-l1]))
        stringGroups.append(stringGroupTable(stringTempName,conversion(pointer+4),conversion(pointer+8),conversion(pointer+12),0))
        pointer += 16
        stringTempName = ""
    for i in range(groupCount):
        pointer = stringGroups[i].pointerPointer
        if stringGroups[i].edited == 0:
            for l1 in range(stringGroups[i].entryCount):
                stringTempString = ""
                for l2 in range(slbInt[conversion(pointer+l1*4)]):
                    stringTempString += str(chr(slbInt[conversion(pointer+l1*4)+1+l2]))
                stringGroups[i].addNew(conversion(pointer+l1*4),slbInt[conversion(pointer+l1*4)],stringTempString)
    groupChoice()
if choice1 == "Y":
    newGroup()