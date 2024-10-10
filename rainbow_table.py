import hashlib
from random import randint
import pickle

class RainbowTable:
    def __init__(self) -> None:
        self.fct_hachage: str
        self.alphabet: str
        self.taille: int
        self.commande: str
        self.arguments: list[str]
        self.N: int
        self.table: dict[int, set[int]] = {}

    # def __str__(self) -> str:
    #     return f"fonction de hash = {self.fct_hachage}"
    

    def __str__(self) -> str:
        attributes = '\n'.join(f'{key} : {value}' for key, value in self.__dict__.items())
        return f'{attributes}'
    

    def load_file(self, filename: str):
        """Instancie les variables de classe selon les informations contenues dans le fichier"""
        with open(filename, 'r') as file:
            lines = file.readlines()

            self.fct_hachage = lines[0].strip()
            self.alphabet = lines[1].strip()
            self.taille = int(lines[2].strip())
            self.commande = lines[3].strip()

            self.arguments = [l.strip() for l in lines[4:]]
        
        self.N = len(self.alphabet) ** self.taille


    def exec_file(self):
        """fonction qui exécute la commande `self.commande`, après avoir instancié la classe `RainbowTable` en lisant le fichier d'entrée"""
        print(self)

        if self.commande == "hash":
            if self.fct_hachage == "SHA1":
                msg = self.arguments[0]
                print(self.h(msg).upper(), f"({msg})")

        elif self.commande == "i2c":
            print(f"i2c({self.arguments[0]}) : {self.i2c(int(self.arguments[0]))}")

        elif self.commande == "config":
            print(self.__str__())
        
        elif self.commande == "h2i":
            print("h2i : ", self.h2i(self.h(self.arguments[0]), int(self.arguments[1])))

        elif self.commande == "i2i":
            idx1 = int(self.arguments[0])
            largeur = int(self.arguments[1])

            i2c = self.i2c(idx1)
            h:bytes = self.h(i2c)
            h2i = self.h2i(h, largeur)

            print(f"{idx1} --i2c--> {i2c} --h--> {h.hex()} --h2i({largeur})--> {h2i}")
            print(f"{idx1}  --i2i({largeur})-->  {self.i2i(idx1, largeur)}")
            

        elif self.commande == "chain":
            idx = int(self.arguments[1])
            largeur = int(self.arguments[0])
            print(f"chain of length {largeur}: {idx} ... {self.nouvelle_chaine(idx, largeur)}")

        elif self.commande == "create":
            hauteur = int(self.arguments[0])
            largeur = int(self.arguments[1])
            fichier = self.arguments[2]
            self.creer_table(largeur, hauteur)
            self.sauve_table(fichier)

        elif self.commande == "info":
            self.affiche_table()


    def h(self, msg: str) -> bytes:
        """fonction de hachage SHA-1"""
        h = hashlib.sha1()
        h.update(msg.encode())
        
        return h.digest()
    
    def i2c(self, number: int):
        """Fonction qui prend un entier et le transforme en texte clair"""
        res:str = ""
        base = len(self.alphabet)
        
        while number >= base:
            rest = number%base
            res = self.alphabet[rest] + res
            number //= base

        res = self.alphabet[number] + res

        return res.rjust(self.taille, self.alphabet[0])
    

    def h2i(self, y: bytes, t: int):
        return (int.from_bytes(y[:8], "little") + t) % self.N
    

    def i2i(self, x:int, t: int):
        return self.h2i(self.h(self.i2c(x)), t)


    def nouvelle_chaine(self, idx1: int, largeur: int):
        for i in range(1, largeur):
            idx1 = self.i2i(idx1, i)
        return idx1


    def index_aleatoire(self):
        return randint(0, self.N - 1)


    def creer_table(self, largeur: int, hauteur: int):
        self.table = dict()

        for i in range(hauteur):
            idx = self.index_aleatoire()
            chaine = self.nouvelle_chaine(idx, largeur)
            liste_chaines = self.table.get(chaine)
            if liste_chaines:
                liste_chaines.add(idx)
            else:
                self.table[chaine] = {idx}
        
        return self.table
    

    def sauve_table(self, filename: str):

        with open(filename, 'wb') as f:
            pickle.dump(self.table, f)

        # with open(filename, 'w', encoding="UTF-8") as file:
        #     file.write(str(self.table))


    def ouvre_table(self, filename: str):
        with open(filename, 'rb') as f:
            self.table = pickle.load(f)


    def affiche_table(self):
        res = self.__str__()
        for i in range(10):
            res += str(self.table.get(i)) + "\n"
        
        for i in range(len(self.table) - 10, len(self.table)):
            res += str(self.table.get(i)) + "\n"
        print(res)
    

    def recherche(self, table: list, hauteur: int, idx: int):
        start = 0
        end = self.N - 1

        while start <= end:
            middle = (start + end) // 2

            if table[middle] < idx:
                start = middle + 1
            elif table[middle] > idx:
                end = middle - 1
            else:
                return middle
            
        return None


    def print_help(self):
        help = """using with test file: python3 main.py <TESTFILE>
    
    A test file contains the following lines, in the following order:
    - 1st line: the hash function to use (SHA1, or some other hash function)
    - 2nd line: the full alphabet (cf option `--alphabet`)
    - 3rd line: the size of clear texts (cf option `--size`)
            (or minimum and maximum sizes of clear texts, separated by a single space)
    - 4th line: a command name (see below)
    - the following lines are the arguments (one per line) to the command (see below).
    
    possible commands, with their arguments:
    config, no argument
    hash, one argument: string to hash
    i2c, one argument: integer to give to i2c
    h2i, two arguments: string 's' and integer 't' to give to h2i
    i2i, two arguments: integer 'i' and integer 't' to give to i2i
    chain, two arguments: width of chain and starting index
    create, three arguments: height and width of table, and filename
    info, one argument: filename
    crack, two arguments: hash to crack, and filename
    crack, two arguments: hash to crack, and filename
    stats, two arguments: height and width of table"""
        
        print(help)