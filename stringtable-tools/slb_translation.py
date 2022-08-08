#imports or something i dunno
import sys
#main vars
dbgp = False if len(sys.argv) == 1 else True  #  if you want to see what the program does, input anything as the next argument after the file name
# code_ic = chr(0x1B) new patch
code_ic = ''

stdchars = ["À", "Á", "Â", "Ã", "Ä", "Å", "Æ", "Ç", "È", "É", "Ê", "Ë", "Ì", "Í", "Î", "Ï",
            "Ð", "Ñ", "Ò", "Ó", "Ô", "Õ", "Ö", "Ø", "Ù", "Ú", "Û", "Ũ", "Ü", "Ý", "þ", "ß",
            "ṡ", "à", "á", "â", "ã", "ä", "å", "æ", "ç", "è", "é", "ê", "ë", "ì", "í", "î",
            "ï", "ð", "ñ", "ò", "ó", "ô", "õ", "ö", "ø", "ù", "ú", "û", "ũ", "ü", "ý", "¿",
            "¡", "Œ", "œ"] 

CODES = {stdchars[i]:chr(i+0xa0) for i in range(65)}

"""CODES = {"\'":")1", #Dashes and stuff
         "\'":")2",
         "-":")6",
         "-":")7",
         
         "À":"NAA", #all the vowels you could ever want
         "È":"NAE",
         "Ì":"NAI",
         "Ò":"NAO",
         "Ù":"NAU",
         "à":"NAa",
         "è":"NAe",
         "ì":"NAi",
         "ò":"NAo",
         "ù":"NAu",
         "Á":"NBA",
         "É":"NBE",
         "Í":"NBI",
         "Ó":"NBO",
         "Ú":"NBU",
         "á":"NBa",
         "é":"NBe",
         "í":"NBi",
         "ó":"NBo",
         "ú":"NBu",
         "Â":"NCA",
         "Ê":"NCE",
         "Î":"NCI",
         "Ô":"NCO",
         "Û":"NCU",
         "â":"NCa",
         "ê":"NCe",
         "î":"NCi",
         "ô":"NCo",
         "û":"NCu",
         "Ä":"NHA",
         "Ë":"NHE",
         "Ï":"NHI",
         "Ö":"NHO",
         "Ü":"NHU",
         "ä":"NHa",
         "ë":"NHe",
         "ï":"NHi",
         "ö":"NHo",
         "ü":"NHu",
         
         "ß":"N{", #more characters
         "Ç":"Nq",
         "ç":"Na",
         "¿":"N?",
         "¡":"N!",

         "ñ":"Nn", #spanish characters
         "Ñ":"NN",
         }"""
    #This doesn't contain all the codes, but these should be all that are used
         

#how is language slb formed?
class StringGroup:
    def __init__(self,name,num,count,point):
        self.name = name
        self.id = num
        self.entryCount = count
        self.pointer = point
        self.strings = []
    def addString(self,pstringn):
        self.strings.append(pstringn)

def conversion(pointer,array):   # 4-byte little-endian number to actual number
    a = 0
    for i in range(4):
        a += (array[pointer+i]*(256**i))
    return a
def deconversion(var,pointer,array):  # the opposite
    s = var.to_bytes(4,byteorder='little')  # This won't work on Python 2... Too bad!
    for i in range(4):
        array[pointer+i] = s[i]
    #Using this instead of a return statement is dumb, but I would rather have it do this than have to deal with merging lists.
    # if it ain't broke, don't fix it

def check_string(something):
    for lchr in something:
        if ord(lchr) > 255:
            print(something)
            print("WRONG CHARACTER DETECTED!", lchr)
            rwith = input("Help out and replace it! Write: ")
            something = something.replace(lchr,rwith)
            check_string(something)
            break
    return something


def reorg(fname):
    #This should work for taking the entirety of the google doc translated files at face value
    # update: yes it does
    file = open(fname, 'r',encoding="ANSI")  # This might cause a memory leak... too bad!
    lines = file.readlines() # splits it into lines
    lines = [x.rstrip('\n') for x in lines] # takes away newline character
    lines.append("dummystring") # adds the dummy string
    ids = ['Fluff','Lev1','Lev2','Lev3','Lev4','Lev5','Lev6','Lev7','Lev8'] # demarcation lines
    levels = [["F"],["1"],["2"],["3"],["4"],["5"],["6"],["7"],["8"]] # lists prepped for strings (initialized with one element)
    #print(levels)
    i = -1
    for line in lines:  # for every line
        #print(line)
        if line not in ids:  # if DOES NOT detect one of the demarcation characters
            levels[i].append(line) # adds line to the string list
            if len(line) > 255:  # catch for a line that's too long
                print("Line in level",i,"is too long! Printing...")  #  ALERT THE LOCALIZER
                print(line)
        else:  #  if it DOES detect one of the demarcation characters
            i += 1  # moves up by an element
        """
        REASON WHY i IS -1 AT THE START
        This would usually mean that it goes to the first element from the BACK of the list, in this case Lev8
        HOWEVER, since the "Fluff" string is the first in the file, i immediately jumps from -1 to 0, so to Fluff, as intended 
        """
    for level in levels:  # for every level
        level.pop(0) # deletes the first string (it's only there to actually have the lists prepared)
        try:
            level.pop(-1)  # tries to delete the last string (either an empty line or the dummy string at the end)
        except:
            pass  # if this does not work it means there was nothing, or i dunno why this handling is here - if it ain't broke don't fix it
    for level in levels:
        for lstr in level:
            lstr = check_string(lstr)
    return levels



def slb_read(fname):
    groups = []
    global dbgp
    file = open(fname,"rb") # This might cause a memory leak... too bad!
    slbIntList = list(file.read())
    
    if dbgp:
        print("FULL SLB",fname,"INCOMING")
        print(slbIntList)
        #return slbIntList

    groupCount = conversion(0,slbIntList) # standard slb reading
    fPoint = conversion(4,slbIntList)

    pointer = fPoint
    for i in range(groupCount): # for all groups
        name = ""
        for l1 in range(4):
            name += chr(slbIntList[pointer+3-l1])  # all the information
        num = conversion(pointer+4,slbIntList)
        count = conversion(pointer+8,slbIntList)
        point = conversion(pointer+12,slbIntList)
        if dbgp:
            print(name,num,count,point)
        groups.append(StringGroup(name,num,count,point))  # adds the group to the group list
        pointer += 16
        #print(pointer)
    if dbgp:
        print("End of groups at",pointer)
        print("Mid pointer count:",(conversion(groups[0].pointer,slbIntList)-pointer)/4)


    acount = sum([group.entryCount for group in groups])  # all the strings
    
    if dbgp:
        print("Group count:",groupCount)
        print("All strings:",acount)
        

    for i in range(groupCount): # for all groups
        pointer = conversion(groups[i].pointer,slbIntList) # pointer to the middle pointers corresponding to the group
        if i == 0 and dbgp:
            print("Start of strings at",pointer)
        for l1 in range(groups[i].entryCount): # for all strings
            slen = slbIntList[pointer]  # length byte
            #print(slen)
            st = ""  # new string
            for l2 in range(slen): # for all characters in the string
                st += chr(slbIntList[pointer+l2+1])  # added
            groups[i].strings.append(st)  # added to strings
            #print(st)
            pointer += slen+2 # pointer moved forward by string length + length byte + null terminator
    if dbgp:
        print("End Of Strings at",pointer) #at the null terminator, before padding or footer pointers
        while pointer % 4 != 0:  # padding
            pointer += 1
    
        print("Bottom poitners incoming, staring at",pointer)  # bottom pointers (not necessary)
        print(slbIntList[pointer:])
        print("Bottom pointer count",(len(slbIntList[pointer:])/4)-1)
            
    return groups

def string_translate(dis_slb,source):
    #dis_slb.groups yada yada
    edited = ""
    #print(source)
    # code handling v2: 1-byte boogaloo
    slist = [list(s) for s in source]
    for lstring in slist:
        for i in range(len(lstring)):
            for code in CODES:
                if lstring[i] == code:
                    #print(lstring[i])
                    lstring[i] = CODES[code]
                    #print(lstring[i])
                    #print(lstring)
                    print("CODE",code,"(",hex(ord(CODES[code])),") FOUND!")
                    break
        # print(char)
    source = [''.join(s) for s in slist]
    #print(source)
    #input()
    """for code in CODES:  # code handling
        # edited = [l.replace(code,code_ic+CODES[code]) for l in source]
        edited = [l.replace(code,CODES[code]) for l in source]
        if edited != source:
            print("CODE",code,"(",hex(ord(CODES[code])),") FOUND!")
            source = edited"""
    
    for i in range(len(source)): # for all the lines
        line = source[i]
        if len(line) > 255: #because of course
            print("The following string is too long! Please shorten!")
            print(line)
            print("Index of string",i)
            input()
            raise Exception("LengthError: Killing the program!")
        #if "ro" in line:
        #    print(line)
    
    tcount = sum([group.entryCount for group in dis_slb])  # total count
    if tcount != len(source):
        print("Miscount detected in this level!")  # go yell at whoever didn't update the spreadsheet
        print("SLB contains",tcount,"strings")
        print("Text file contains",len(source),"strings")
        #print(source)
        exit()
    acount = 0
    for i in range(len(dis_slb)): #replacing the strings
        for l1 in range(len(dis_slb[i].strings)):
            #if dbgp == True:
            #    print("Matching",dis_slb[i].strings[l1],"and",source[acount])
            try:
                dis_slb[i].strings[l1] = source[acount]
            except IndexError:  # This should not happen anymore with the previous handling but who knows
                # If this ever gets tripped, may Mata Nui help you (or just go yell at me)
                print("IndexError detected. Died at",dis_slb[i].strings[l1-1],"and",source[acount-1])
                exit()
            acount += 1
    return dis_slb



def slb_write(dis_slb,out_fname):
    global dbgp
    debug = dbgp  # too lazy to change the references
    blank_pointer = [0, 0, 0, 0]
    slbIntList = blank_pointer*2
    #top pointers do not change since the string distribution does not change :>
    midPointers = []
    bottomPointers = []
    deconversion(len(dis_slb),0,slbIntList) #group count
    deconversion(8,4,slbIntList) #first pointer
    bottomPointers.append(4)
    slbIntList.extend(blank_pointer*4*len(dis_slb)) #that's all the groups!
    pointer = 8
    acount = sum([group.entryCount for group in dis_slb]) # all strings, again
    for group in dis_slb:
        for i in range(4):  # writing the info
            slbIntList[pointer+3-i] = ord(group.name[i])
        pointer += 4
        deconversion(group.id,pointer,slbIntList)
        pointer += 4
        deconversion(group.entryCount,pointer,slbIntList)
        pointer += 4
        deconversion(group.pointer,pointer,slbIntList)
        bottomPointers.append(pointer)
        pointer += 4
    if debug:
        print(slbIntList)
        print(pointer)
    for i in range(acount):  #mid section skip
        slbIntList.extend(blank_pointer) 
        bottomPointers.append(pointer)
        pointer += 4
    pointer = len(slbIntList)  # pointer set to the end
    if debug:
        print(pointer)
        print(len(bottomPointers))
    for group in dis_slb:  # STRINGS
        for string in group.strings:
            slbIntList.extend([0 for i in range(len(string)+2)]) # allocating string length + length byte + null terminator
            slbIntList[pointer] = len(string) # length byte
            midPointers.append(pointer) # added to pointers
            pointer += 1
            for i in range(len(string)): # writing the string
                slbIntList[pointer] = ord(string[i])
                pointer += 1
            #print(slbIntList)
            #print(slbIntList[pointer])
            pointer += 1 # since a 0 already is here from line 267, we can skip setting this to 0
    finalPointer = pointer # pointer to the end of the strings (it's a surprise tool that will help us later)
    pointer = 8+16*len(dis_slb) #start of mid pointers
    for ptr in midPointers:  # adding all the mid pointers
        deconversion(ptr,pointer,slbIntList)
        pointer += 4
    pointer = finalPointer  # it's later now!
    while len(slbIntList) % 4 != 0: # padding
        slbIntList.append(0)
    pointer = len(slbIntList) # pointer set again to the end
    slbIntList.extend(blank_pointer*(len(bottomPointers)+2)) # allocating all bottom pointers + count + coffee signature
    for ptr in bottomPointers:  # all the bottom pointers
        deconversion(ptr,pointer,slbIntList)
        pointer += 4
    deconversion(len(bottomPointers),pointer,slbIntList) # count
    pointer += 4 # coffee signature
    slbIntList[pointer] = 0xEE
    slbIntList[pointer+1] = 0xFF
    slbIntList[pointer+2] = 0xC0
    #done, hopefully
    if dbgp:
        print(slbIntList)
    for i in range(len(slbIntList)):
        if slbIntList[i] > 255:  # final checks if this works
            print("AA WRONG CHARACTER")  # something must have gone horribly wrong - didn't save as ANSI?
            print(slbIntList[i-5:i+4], i)
            print([chr(n) for n in slbIntList[i-5:i+4]])  # this should help you find it
            replacement = ord(input("Please help out by replacing the character:"))
            slbIntList[i] = replacement
    with open(out_fname,"wb") as the_slb:
        the_slb.write(bytearray(slbIntList))  # this does *not* cause a memory leak
    return slbIntList
    #TODO: Write to file
    
            
def slb_full(slb_fname,source,out_fname):  # culmination
    foo = slb_read(slb_fname)  # reads template SLB, returns SLB class
    bar = string_translate(foo,source) # changes strings in SLB class
    slb_write(bar,out_fname) # writes from SLB class back to SLB, using group distribution from template SLB
    print("Completed",out_fname)  # yay


def game_full(rebuilt,lang):
    slb_names = ["Fluff_eng.slb","Lev1_eng.slb","Lev2_eng.slb","Lev3_eng.slb","Lev4_eng.slb","Lev5_eng.slb","Lev6_eng.slb","Lev7_eng.slb"]  # all of them
    if rebuilt:
        slb_names.append("Lev8_eng.slb") # and nobua
    sources = reorg(lang+".txt")  # all the strings
    out_names = [s.replace("eng",lang) for s in slb_names]  # output SLBs to use
    for i in range(len(slb_names)):  # for all the SLBs
        slb_full(slb_names[i],sources[i],out_names[i]) # above function

if __name__ == '__main__':
    """I don't know why, I don't want to know why,
    I shouldn't have to wonder why,
    but for whatever stupid reason '0' is interpreted as True so I have to do this terribleness"""
    r = bool(int(input("Is this Rebuilt? (0 or 1)")))
    l = input("Language string (3 characters):")  # this should be understandable
    game_full(r,l)
    
#slb_full("Lev1_eng.slb",reorg("ger.txt")[1],"Lev1_ger.slb")

"""
RECONSTRUCTED LANG SLB INFO:

First pointer at $0004, *always* points to $0008

Group pointers (top) point to their first middle pointer

All middle pointers point to the strings (specifically to the length byte)

Bottom pointers:

amount = groups + strings + 1

first one points to $0004

next %groupcount pointers all point to their pointers

next %stringcount pointers all point to the mid pointers

last one has the amount of pointers

rest is the coffee signature

"""



