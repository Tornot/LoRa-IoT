import subprocess

texteDuPaquet = "NotreProjet"
nombreDePaquets = 10 #la fonction de checksum ne fonctionne que jusque 9, pour l'instant

def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)

def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8) #The ord() function returns the number representing the unicode code of a specified character.
        s = carry_around_add(s, w)
    return ~s & 0xffff

if __name__ == "__main__":
    for id in range(nombreDePaquets):
        paquet = texteDuPaquet + str(id)
        paquet += str(checksum(paquet))
        print(paquet)
        #subprocess.call(["command1", "paquet"])