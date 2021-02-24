import os
import subprocess
from random import shuffle
from shutil import move
from sys import exit, argv
from math import floor
from os.path import basename, join, expanduser, exists
from time import time

timeStart = 0
fileSize = 0

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
    open("fGuardkey.txt", "w").write(keyStr)

keyStr = ""

try:
    keyStr = open("fGuardkey.txt", "r").read().split(",")
except:
    print("[info] Key doesn't exist. generated a new key (fGuardkey.txt).")
    genKey()
    keyStr = open("fGuardkey.txt", "r").read().split(",")

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

    if "%userprofile%" in curDir.lower():
        curDir = curDir.replace("%userprofile%", expanduser("~")).replace("%USERPROFILE%", expanduser("~")).replace("/", "\\")
    
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

    #set timestamp
    global timeStart
    timeStart = int(time())
    
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
    global fileSize
    fl = []
    if directCMD_CMD != "" and directCMD_PATH != "":
        fl = gatherFile("Encrypt", directCMD_PATH, directCMD_CMD)
    else:
        fl = gatherFile("Encrypt", "", "")
    
    #encryption   
    for i in range(len(fl)):
        if fl[i].endswith("fGuardkey.txt") or fl[i].endswith("fileGuard.py"):
            print(f"[{i+1}/{len(fl)}] Bypassed some file you may don't want to encrypt...")
            continue
        
        try:
            readb = list(open(fl[i], "rb").read())
            print(f"[{i+1}/{len(fl)}] Protecting: {fl[i]}")
            
            startpt = 0
            
            for j in range(10):
                try:
                    for k in range(startpt, startpt + 20000):
                        readb[k] = key[readb[k]]
                except:
                    pass
                startpt += floor(len(readb) / 10)
            readb = bytes(readb)

            #write bytes to file
            open(fl[i] + ".+enc", "wb").write(readb)
            
            #record size
            fileSize += len(readb)/1024/1024
            
            try:
                #clean backup
                os.rename(fl[i], fl[i] + ".DeleteMeByfGuard")
                os.remove(fl[i] + ".DeleteMeByfGuard")
            except:
                print(f"Failed to clean original: {fl[i]}")
            
        except:
            print(f"[{i+1}/{len(fl)}] Failed protecting: " + fl[i] + "\n")
            #clean garbage
            try:
                #clean backup
                os.rename(fl[i] + ".BackupByfGuard", fl[i] + ".DeleteMeByfGuard")
                print(f"Cleaning {fl[i]}.DeleteMeByfGuard")
                os.remove(fl[i] + ".DeleteMeByfGuard")
            except:
                print(f"Failed to clean backup: {fl[i]}")
            
def decrypt(directCMD_PATH, directCMD_CMD):
    global fileSize
    fl = []
    if directCMD_CMD != "" and directCMD_PATH != "":
        fl = gatherFile("Decrypt", directCMD_PATH ,directCMD_CMD)
    else:
        fl = gatherFile("Decrypt", "", "")
    
    #decryption
    for i in range(len(fl)):        
        try:
            readb = list(open(fl[i], "rb").read())
            
            print(f"[{i+1}/{len(fl)}] Unprotecting: " + fl[i])
            
            startpt = 0

            for j in range(10):
                try:
                    for k in range(startpt, startpt + 20000):
                        readb[k] = revKey[readb[k]]
                except:
                    pass
                startpt += floor(len(readb) / 10)
            readb = bytes(readb)
            
            open(fl[i][0:len(fl[i])-5], "wb").write(readb)

            fileSize += len(readb)/1024/1024

            try:
                os.rename(fl[i], fl[i] + ".DeleteMeByfGuard")
                os.remove(fl[i] + ".DeleteMeByfGuard")
            except:
                print(f"Failed to clean original: {fl[i]}")
        except Exception as e:
            print(f"[{i+1}/{len(fl)}] {e}")
            #clean garbage
            try:
                os.rename(fl[i] + ".BackupByfGuard", fl[i] + ".DeleteMeByfGuard")
                print(f"Cleaning {fl[i]}.DeleteMeByfGuard")
                os.remove(fl[i] + ".DeleteMeByfGuard")
            except:
                print(f"Failed to clean backup: {fl[i]}")

def checkBackup():
    backupDir = input("\n\nDirectory to search (Blank = User folder): ")
    if backupDir == "":
        backupDir = "%userprofile%"
        
    if "%userprofile%" in backupDir.lower():
        backupDir = backupDir.replace("%userprofile%", expanduser("~")).replace("%USERPROFILE%", expanduser("~")).replace("/", "\\")
    i = 1
    empty = True
    for path, subdirs, files in os.walk(backupDir):
        for name in files:
            if name.endswith(".+enc"):
                curPath = join(path, name)
                if(exists(curPath[0:len(curPath)-5])):
                    empty = False
                    print(f"[{i}] {curPath[0:len(curPath)-5]} <==> {name}")
                
    if empty:
        print("Nothing to show...")

    print("Finished...\n")
    ask()

def delGarbage():
    garbageDir = input("\n\nDirectory to search (Blank = User folder): ")

    if garbageDir == "":
        garbageDir = "%userprofile%"

    if "%userprofile%" in garbageDir.lower():
        garbageDir = garbageDir.replace("%userprofile%", expanduser("~")).replace("%USERPROFILE%", expanduser("~")).replace("/", "\\")
    i = 1
    empty = True
    for path, subdirs, files in os.walk(garbageDir):
        for name in files:
            if name.endswith(".DeleteMeByfGuard"):
                try:
                    empty = False
                    os.remove(join(path, name))
                    print(f"[{i}] Cleaned: {join(path, name)}")
                except:
                    print(f"Failed to clean: {join(path, name)}")
    if empty:
        print("Nothing to clean...")
        
    print("Finished...\n")
    ask()
    
def ask():
        print("----fileGuard V. 000----")
        print("If you would like to change a new encryption key, simply remove the 'fGuardkey.txt' under the directory contains this program.")
        print('Execute from CMD: fileGuard.exe Encrypt "C:\Windows\System32" "e+:jpg/pdf/exe"')
        print("\n\n\nChoices:\n(1) Encrypt\n(2) Decrypt\n(3) Check backup files created from interruption\n(4) Delete garbage created from interruption")
        action = input('Your choice (input number): ')

        if action == "1":
            print("Encrypting...\n")
            encrypt("", "")
            #record starting ts
        elif action == "2":
            print("Decrypting...\n")
            decrypt("", "")
        elif action == "3":
            checkBackup()
        elif action == "4":
            delGarbage()
        else:
            print("Unknown choice")
            ask()
            
            
#command example:python fileGuard.py Encrypt "C:\Windows\System32" "e+:jpg/pdf/exe"
if len(argv) == 4:
    timeStart = int(time())
    if argv[1] == "Encrypt":
        encrypt(argv[2], argv[3])
    elif argv[1] == "Decrypt":
        decrypt(argv[2], argv[3])
    else:
        print("Invalid arguments.")
        exit()
else:
    ask()

timeUsed = int(time()) - timeStart
ended = input(f"Finished modifying {round(fileSize, 3)}MB of data using {timeUsed} seconds. \nPress enter to exit...")
