######################################
#stringtable to XML & back converter #
#by OndrikB                          #
#version 1.1                         #
#Changelog:                          #
#v1.1                                #
#Added checking for long strings     #
#v1.0                                #
#Initial Release                     #
######################################
#---imports---
import sys
#---classes---
class string:
    def __init__(self,v1):
        self.string = v1
        self.length = len(v1)
class strgid:
    def __init__(self,v1,v2):
        self.name = v1
        self.num = v2
class group:
    def __init__(self,v1,v2,v3):
        self.id = v1
        self.entryCount = v2
        self.strings = v3
#---variables---
stringtable = []
name_slb = "stringtable"
name_group = "group"
name_gr_name = "name"
name_gr_c = "number"
name_strings = "strings"
name_strings_i = "string"
#---functions---
def conversion(pointer,array): 
    a = 0
    for i in range(4):
        a += (array[pointer+i]*(256**i))
    return a
def slbAppend(var,array):
    for i in range(var):
        array.append(0)
def deconversion(var,pointer,array):  
    global slbParse
    s = var.to_bytes(4,byteorder='little')
    for i in range(4):
        array[pointer+i] = s[i]
def SLB(file):
    global stringtable
    global name_slb
    global name_group
    global name_gr_name
    global name_gr_c
    global name_strings
    global name_strings_i
    print("Reading",file)
    slbIntList = list(open(file,"rb").read())
    pointer = 0
    all_groups = conversion(pointer,slbIntList)
    pointer = 4
    body_offset = conversion(pointer,slbIntList)
    pointer = body_offset
    entries = 0
    for i in range(all_groups):
        tempString = ""
        for l1 in range(4):
            tempString += str(chr(slbIntList[pointer+3-l1]))
        pointer += 4
        tempCount = conversion(pointer,slbIntList)
        pointer += 4
        entryCount = conversion(pointer,slbIntList)
        entries += entryCount
        pointer += 8
        stringtable.append(group(strgid(tempString,tempCount),entryCount,[]))
    #all groups now there, pointer at mid section (not needed)
    pointer += entries*4 #mid section skip
    #pointer at string start
    for i in range(all_groups): 
        for l1 in range(stringtable[i].entryCount): #each string in each group
            pointer += 1 #past the length byte
            tempString = ""
            while slbIntList[pointer] != 0:
                tempString += str(chr(slbIntList[pointer]))
                pointer += 1
            pointer += 1 #past the null terminator
            stringtable[i].strings.append(string(tempString))
    #all string reading done
    #catching ellipses
    for i in range(len(stringtable)):
        for l1 in range(stringtable[i].entryCount): #each string in each group
            tempString = list(stringtable[i].strings[l1].string)
            for l2 in range(len(tempString)):
                if tempString[l2] == chr(0x1B) and tempString[l2+1] == "(" and tempString[l2+2] == "5":
                    tempString[l2] = "."
                    tempString[l2+1] = "."
                    tempString[l2+2] = "."
            stringtable[i].strings[l1].string = "".join(tempString)
    #xml conversion
    xmlFile = "<?xml version=\"1.0\"?>\n<"+name_slb+">\n" #let's goooooooooo
    tab = chr(9) #lots of tabs here
    for i in range(all_groups):
        xmlFile += tab+"<"+name_group+">\n"
        xmlFile += 2*tab+"<"+name_gr_name+">"+stringtable[i].id.name+"</"+name_gr_name+">\n"
        xmlFile += 2*tab+"<"+name_gr_c+">"+str(stringtable[i].id.num)+"</"+name_gr_c+">\n"
        xmlFile += 2*tab+"<"+name_strings+">\n"
        for l1 in range(stringtable[i].entryCount):
            xmlFile += 3*tab+"<"+name_strings_i+">"+stringtable[i].strings[l1].string+"</"+name_strings_i+">\n"
        xmlFile += 2*tab+"</"+name_strings+">\n"
        xmlFile += tab+"</"+name_group+">\n"
    xmlFile += "</"+name_slb+">\n"
    fileName = list(file)
    fileName[len(fileName)-1] = "l";
    fileName[len(fileName)-2] = "m";
    fileName[len(fileName)-3] = "x";
    with open("".join(fileName), 'w',encoding="utf-8") as the_file:
        the_file.write((xmlFile+'\n'))
    the_file.close()
    print("Done")
def XML(file):
    global stringtable
    global name_slb
    global name_group
    global name_gr_name
    global name_gr_c
    global name_strings
    global name_strings_i
    print("Reading",file)
    tab = chr(9)
    slbIntList = []
    with open(file, "r",encoding="utf-8") as f:
        fileLines = []
        for line in f:
            fileLines.append(line)
        for i in range(len(fileLines)):
            fileLines[i] = fileLines[i].rstrip("\n")
        for i in range(len(fileLines)):
            fileLines[i] = fileLines[i].replace("\t","")
    currGroup = 0
    currStringCount = -1 #some bug with the first group, correction here (hacky)
    allStrings = 0
    tempStrings = []
    tempName = ""
    tempNum = ""
    for i in range(len(fileLines)):
        if fileLines[i] == "</"+name_group+">":
            currGroup += 1
            
            currStringCount = 0
        if fileLines[i][1:1+len(name_gr_name)] == name_gr_name:
            tempName = fileLines[i][2+len(name_gr_name):-len(name_gr_name)-3]
        if fileLines[i][1:1+len(name_gr_c)] == name_gr_c:
            tempNum = fileLines[i][2+len(name_gr_c):-len(name_gr_c)-3]
        if fileLines[i][1:1+len(name_strings_i)] == name_strings_i and fileLines[i] != "<"+name_strings+">" and fileLines[i] != "</"+name_strings+">":
            currStringCount += 1
            tempStrings.append(string(fileLines[i][2+len(name_strings_i):-len(name_strings_i)-3]))
            if currGroup == 0 and currStringCount == 1: #once again, a bug with first string and first group
                tempStrings.pop(0)
        if fileLines[i] == "</"+name_strings+">":
            allStrings += currStringCount
            stringtable.append(group(strgid(tempName,tempNum),currStringCount,tempStrings))
            #print("WRITE")
            #print(stringtable[len(stringtable)-1].strings)
            tempStrings = []
            #print("RESET")
            #print(stringtable[len(stringtable)-1].strings)
            #print("END")
            currStringCount = 0
        #print(tempStrings)
    #print(allStrings)
    #The entire stringtable is there
    #Checking for characters that are too long. In that case, throw error and print all offending strings.
    tooLong = 0
    tLF = 0
    for i in range(len(stringtable)):
        print("Group "+str(i+1)+" ("+stringtable[i].id.name+" "+stringtable[i].id.num+")")
        tooLong = 0
        for l1 in range(stringtable[i].entryCount):
            if len(stringtable[i].strings[l1].string) > 256:
                tooLong += 1
                tLF = 1
                print("String \""+stringtable[i].strings[l1].string+"\" is too long! Please shorten it")
        if tooLong == 0:
            print("Everything is fine in this group! :)")
    if tLF == 1:
        print("Aborting SLB writing sequence. Press any key to kill the program")
        input()
        kill_switch = 1/0 #mwahahahahahahah
    midPointers = []
    bottomPointers = []
    slbAppend(4,slbIntList)
    deconversion(len(stringtable),0,slbIntList)
    pointer = 4
    slbAppend(4,slbIntList)
    deconversion(8,4,slbIntList)
    bottomPointers.append(pointer)
    for i in range(len(stringtable)): #groups (except for pointers)
        slbAppend(16,slbIntList)
        pointer += 4
        for l1 in range(4):
            l = list(stringtable[i].id.name)
            slbIntList[pointer+3-l1] = ord(l[l1])
        pointer += 4
        deconversion(int(stringtable[i].id.num),pointer,slbIntList)
        pointer += 4
        deconversion(len(stringtable[i].strings),pointer,slbIntList)
        pointer += 4
        bottomPointers.append(pointer)
        deconversion(0,pointer,slbIntList)
    pointer += 4
    slbAppend(4*allStrings,slbIntList)
    for i in range(allStrings): #mid pointers (but no data)
        bottomPointers.append(pointer)
        deconversion(255,pointer,slbIntList)
        pointer += 4
    for i in range(len(stringtable)): #all strings
        for l1 in range(stringtable[i].entryCount):
            #length byte
            slbAppend(1,slbIntList)
            midPointers.append(pointer)
            pointer += 1
            slbIntList[len(slbIntList)-1] = stringtable[i].strings[l1].length
            slbAppend(stringtable[i].strings[l1].length,slbIntList)
            for l2 in range(stringtable[i].strings[l1].length):
                #string
                slbIntList[pointer] = ord(stringtable[i].strings[l1].string[l2])
                pointer += 1
            #null termintator
            slbAppend(1,slbIntList)
            pointer += 1
            slbIntList[len(slbIntList)-1] = 0
    #now pointers (from the bottom up)
    pointer = len(slbIntList)
    while pointer % 4 != 0: #setting to either 0, 4, B or F
        pointer += 1
        slbAppend(1,slbIntList)
    slbAppend(4*len(bottomPointers),slbIntList)
    for i in range(len(bottomPointers)):
        deconversion(bottomPointers[i],pointer,slbIntList)
        pointer += 4
    slbAppend(8,slbIntList)
    deconversion(len(bottomPointers),pointer,slbIntList)
    pointer += 4 #signature
    slbIntList[pointer] = 0xEE
    slbIntList[pointer+1] = 0xFF
    slbIntList[pointer+2] = 0xC0
    #middle pointers
    pointer = 8+16*len(stringtable)
    for i in range(len(midPointers)):
        deconversion(midPointers[i],pointer,slbIntList)
        pointer += 4
    #top pointer
    pointer = 20
    for i in range(len(stringtable)):
        if i == 0:
            nVal = 8+16*len(stringtable)
        else:
            nVal += stringtable[i-1].entryCount*4
        deconversion(nVal,pointer,slbIntList)
        pointer += 16
    print(pointer)  
    fileName = list(file)
    fileName[len(fileName)-1] = "b";
    fileName[len(fileName)-2] = "l";
    fileName[len(fileName)-3] = "s";
    newSlbName = "".join(fileName)
    newSlb = open(newSlbName, "wb")
    #slbWriteList = bytearray(slbIntList)
    newSlb.write(bytes(slbIntList))
    newSlb.close()
    #print(pointer)
    print("Done")    
#---init---
stringFile = ""
if len(sys.argv) == 1:
    print("Usage: Drag and drop a stringtable slb or xml file into the converter or use arguments (i. e: stringtable.py file1)")
    print("Press Enter to close the program")
    input()
else:
    stringFile = sys.argv[1]
#----main----
if stringFile[len(stringFile)-1] == 'b':
    SLB(stringFile)
elif stringFile[len(stringFile)-1] == 'l':
    XML(stringFile)
else:
    print("Invalid file format (must be \".xml\" or \".slb\"")
print("Press Enter to close the program")
input()