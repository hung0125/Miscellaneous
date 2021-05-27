#The most useless Python script in the World
import requests as rq
from random import randrange as rr
from random import choice
import time

strElement = [0] * 128
for i in range(128):
    strElement[i] = i

count = 0
while True:
    howLong = rr(1,80)
    randStr = ""
    for i in range(howLong):
        randStr += chr(choice(strElement))
    
    #Or replace Google with Bing, DuckDuckGo, etc.
    open("Google.html", 'wb').write(rq.get(f"https://www.google.com/search?q={randStr}").content)
    count += 1
    print(f"#{count}: I searched:\n {randStr}\n\n_____________________")
    time.sleep(3)
