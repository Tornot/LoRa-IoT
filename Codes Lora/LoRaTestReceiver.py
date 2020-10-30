import subprocess
import xlsxwriter
import re
import time
from datetime import datetime

nombreDePaquets = 10 

inputPaquets = [
"NotreProjet051334",
"NotreProjet151078",
"NotreProjet250822",
"NotreProjet350566",
"NotreProjet450310",
"NotreProjet550054",
"NotreProjet649798",
"NotreProjet749542",
"NotreProjet849286",
"NotreProjet949030",
]

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8) #The ord() function returns the number representing the unicode code of a specified character.
        s = carry_around_add(s, w)
    return ~s & 0xffff

def timeToString (_now):
    return _now.strftime("%d-%m-%Y %H:%M:%S")

def stringToTime(inputString):
    return  datetime.strptime(inputString, "%d-%m-%Y %H:%M:%S")

def arrayToExcel(worksheet, data,  now):
    rowIndex = 0
    for dataLine in data:
        colIndex = 0
        for value in dataLine:
            if value == "0":
                worksheet.write(rowIndex,colIndex, timeToString(now))
            else:
                worksheet.write(rowIndex,colIndex, value)
            colIndex += 1
        rowIndex += 1

def analysePaquetsReceiveds(input):
    received = 0
    dataArray = []
    for line in input:
        if re.search("^Packet", line):
            dataArray.append([])

            infos = line.split(',')
            for info in infos:
                data = info.split(':')
                dataArray[len(data)-1].append(data)

        elif re.search("^Payload", line):
            message = info.split(':')[1]
            checksumReceived = int(message[-5:])
            messageReceived = message[:-5]

            if checksumReceived == checksum(messageReceived):
                dataArray[len(data)-1].append("OK")
                received += 1
            
    return received



#result = subprocess.run(['notreCommand', 'arg'], stdout=subprocess.PIPE)
#result.stdout.decode('utf-8')
received = analysePaquetsReceiveds(inputPaquets)
print(f'{received}/{nombreDePaquets} PAQUETS RECEIVEDS')