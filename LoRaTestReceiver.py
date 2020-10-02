import subprocess

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

def analysePaquetsReceiveds(input):
    received = 0
    for line in input:
        checksumReceived = int(line[-5:])
        messageReceived = line[:-5]
        if checksumReceived == checksum(messageReceived):
            received += 1
    return received



#result = subprocess.run(['notreCommand', 'arg'], stdout=subprocess.PIPE)
#result.stdout.decode('utf-8')
received = analysePaquetsReceiveds(inputPaquets)
print(f'{received}/{nombreDePaquets} PAQUETS RECEIVEDS')