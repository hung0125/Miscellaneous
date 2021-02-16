import os
from random import shuffle
from shutil import move
import shutil
from sys import exit, argv
from math import floor
from os.path import basename, join, exists

def genKey():
    keyVals = []
    keyStr = ""
    for i in range(256):
        keyVals.append(i)
    shuffle(keyVals)
    for i in range(256):
        keyStr += str(keyVals[i])
        if i < 255:
            keyStr += ","
    open("key.txt", "w").write(keyStr)

keyStr = ""

try:
    keyStr = open("key.txt", "r").read().split(",")
except:
    print("[info] Key doesn't exist. generated a new key (key.txt).")
    genKey()
    keyStr = open("key.txt", "r").read().split(",")

key = []
revKey = [0] * 256
for i in range(256):
    key.append(int(keyStr[i]))
    revKey[key[i]] = i

def gatherFile(instructionType, directCMD_PATH, directCMD_CMD):

    selectOptions = [
    f"\n0. {instructionType} everything (input be like '0')",
    "1. [OR selection]Only some extensions (input be like 'e+:jpg/exe/pdf...')",
    "2. [AND selection]Exclude some extensions (input be like 'e-:mp4/zip...')",
    "3. [OR selection]Only some file names (input be like 'n+:a.jpg/b.pdf/c.java...')",
    "4. [AND selection]Exclude some file names (input be like 'n-:NotThisOne.js/NotThisOneToo.cpp')",
    "*For 3, 4 in decryption: input name without '.+enc' extension."
    ]

    #Obtain basic information
    if directCMD_PATH != "":
        curDir = directCMD_PATH
    else:
        curDir = input("Directory path?: ")

    for i in range(5):
        print(selectOptions[i])
    
    if directCMD_CMD != "":
        extAsk = directCMD_CMD.split(":")
    else:
        extAsk = input(f"\n{instructionType}ion command?: ").split(":")
    qArr = []
   
    #modify query array according to options
    if extAsk[0] == "e+" or extAsk[0] == "e-":
        qArr = extAsk[1].replace("/", "/.").split("/")
        qArr[0] = '.' + qArr[0]
    elif extAsk[0] == "n+" or extAsk[0] == "n-":
        qArr = extAsk[1].split("/")
    elif extAsk[0] != "0":
        print("\nUnknown input...\n")
        exit()
    
    #search files
    fl = []
    if instructionType == "Encrypt":
        for path, subdirs, files in os.walk(curDir):
            for name in files:
                #append according to options
                if not name.endswith(".+enc"):
                    if extAsk[0] == "0":
                            fl.append(join(path, name))

                    elif extAsk[0] == "e+":
                        for i in range(len(qArr)):
                            if name.endswith(qArr[i]):
                                fl.append(join(path, name))
                                print(f"File '{name}' is {qArr[i]} format...")
                                break

                    elif extAsk[0] == "e-":
                        qualified = True
                        for i in range(len(qArr)):
                            if name.endswith(qArr[i]):
                                qualified = False
                                break
                        if qualified:
                            fl.append(join(path, name))
                            print(f"File '{name}' not found in extensions list...")

                    elif extAsk[0] == "n+":
                        for i in range(len(qArr)):
                            if qArr[i] == name:
                                fl.append(join(path, name))
                                print(f"File '{name}' = '{qArr[i]}'")
                                break

                    elif extAsk[0] == "n-":
                        qualified = True
                        for i in range(len(qArr)):
                            if qArr[i] == name:
                                qualified = False
                                break
                        if qualified:
                                fl.append(join(path, name))
                                print(f"File '{name}' not found in names list...")
    else:
        for path, subdirs, files in os.walk(curDir):
            for name in files:
                #append according to options
                if name.endswith(".+enc"):
                    if extAsk[0] == "0":
                            fl.append(join(path, name))

                    elif extAsk[0] == "e+" and name.endswith(".+enc"):
                        for i in range(len(qArr)):
                            if name.endswith(qArr[i] + ".+enc"):
                                fl.append(join(path, name))
                                print(f"File '{name}' is {qArr[i]} format...")
                                break

                    elif extAsk[0] == "e-" and name.endswith(".+enc"):
                        qualified = True
                        for i in range(len(qArr)):
                            if name.endswith(qArr[i] + ".+enc"):
                                qualified = False
                                break
                        if qualified:
                            fl.append(join(path, name))
                            print(f"File '{name}' not found in extensions list...")

                    elif extAsk[0] == "n+" and name.endswith(".+enc"):
                        for i in range(len(qArr)):
                            if qArr[i] + ".+enc" == name:
                                fl.append(join(path, name))
                                print(f"File '{name}' = '{qArr[i]}'")
                                break

                    elif extAsk[0] == "n-" and name.endswith(".+enc"):
                        qualified = True
                        for i in range(len(qArr)):
                            if qArr[i] + ".+enc" == name:
                                qualified = False
                                break
                        if qualified:
                                fl.append(join(path, name))
                                print(f"File '{name}' not found in names list...")


    return fl

def encrypt(directCMD_PATH, directCMD_CMD):
    fl = []
    if directCMD_CMD != "" and directCMD_PATH != "":
        fl = gatherFile("Encrypt", directCMD_PATH, directCMD_CMD)
    else:
        fl = gatherFile("Encrypt", "", "")
    
    #encryption   
    for i in range(len(fl)):
        try:
            
            readb = open(fl[i], "rb").read()
            print(f"[{i+1}/{len(fl)}] Protecting: {fl[i]}\n")
            
            startpt = 0
            for j in range(10):
                cont = list(readb[startpt:10000])#to byte array
                startpt += floor(len(readb) * 0.1)
                contCopy = bytes(cont)
                
                for k in range(len(cont)):
                    cont[k] = key[cont[k]]
                        
                res = bytes(cont)
                readb = readb.replace(contCopy, res, 1)
            
            try:
                move(fl[i], "Backup_" + basename(fl[i]))
                open(f"origpath_{basename(fl[i])}.txt", "w").write(fl[i])
            except:
                print(f"Failed to make backup: {fl[i]}")
            #write bytes to file
            open(fl[i], "wb").write(readb)
            os.rename(fl[i], fl[i] + ".+enc")
            try:
                #clean backup
                os.rename("Backup_" + basename(fl[i]), "DeleteMe_" + basename(fl[i]))
                os.remove( "DeleteMe_" + basename(fl[i]))
                os.remove(f"origpath_{basename(fl[i])}.txt")
            except:
                print(f"Failed to clean backup: {fl[i]}")
            
        except:
            print(f"[{i+1}/{len(fl)}] Failed protecting: " + fl[i] + "\n")
            #clean garbage
            
def decrypt(directCMD_PATH, directCMD_CMD):
    fl = []
    if directCMD_CMD != "" and directCMD_PATH != "":
        fl = gatherFile("Decrypt", directCMD_PATH ,directCMD_CMD)
    else:
        fl = gatherFile("Decrypt", "", "")
    
    #decryption
    for i in range(len(fl)):
        try:
            readb = open(fl[i], "rb").read()
            
            print(f"[{i+1}/{len(fl)}] Unprotecting: " + fl[i] + "\n")
            
            startpt = 0
            for j in range(10):
                cont = list(readb[startpt:10000])#to byte array
                startpt += floor(len(readb) * 0.1)
                contCopy = bytes(cont)
                
                for k in range(len(cont)):
                    cont[k] = revKey[cont[k]]
                        
                res = bytes(cont)
                
                readb = readb.replace(contCopy, res, 1)
            
            try:
                move(fl[i], "Backup_" + basename(fl[i]))
                open(f"origpath_{basename(fl[i])}.txt", "w").write(fl[i])
            except:
                print(f"Failed to make backup: {fl[i]}")
            
            open(fl[i], "wb").write(readb)
            os.rename(fl[i],fl[i][0:len(fl[i])-5])

            try:
                os.rename("Backup_" + basename(fl[i]), "DeleteMe_" + basename(fl[i]))
                os.remove("DeleteMe_" + basename(fl[i]))
                os.remove(f"origpath_{basename(fl[i])}.txt")
            except:
                print(f"Failed to clean backup: {fl[i]}")
        except Exception as e:
            print(f"[{i+1}/{len(fl)}] {e}")
            #clean garbage


def ask():
        print("----fileGuard V. 000----")
        print("If you would like to change a new encryption key, simply remove the 'key.txt' under the directory contains this program.")
        print('Execute from CMD: fileGuard.exe Encrypt "C:\Windows\System32" "e+:jpg/pdf/exe"')
        print("Choices:\n(1) Encrypt\n(2) Decrypt")
        action = input('Your choice (input number): ')
        if action == "1":
            print("Encrypting...\n")
            encrypt("", "")
            
        elif action == "2":
            print("Decrypting...\n")
            decrypt("", "")
        else:
            print("Unknown choice")
            ask()
            
#command example:python fileGuard.py Encrypt "C:\Windows\System32" "e+:jpg/pdf/exe"
if len(argv) == 4:
    if argv[1] == "Encrypt":
        encrypt(argv[2], argv[3])
    elif argv[1] == "Decrypt":
        decrypt(argv[2], argv[3])
    else:
        print("Invalid arguments.")
        exit()
else:
    ask()

ended = input("Finished. Press enter to exit...")
