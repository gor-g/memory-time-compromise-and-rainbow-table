import hashlib
from random import randint
from math import exp
import pickle
import time


class RainbowTableManager:
    def __init__(self) -> None:
        self.fct_hachage: str
        self.alphabet: str
        self.taille: int
        self.commande: str
        self.arguments: list[str]
        self.N: int
        self.largeur: int
        self.hauteur: int
        self.table: dict[int, set[int]] = {}

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
        """fonction qui exécute la commande `self.commande`, après avoir instancié la classe `RainbowTableManager` en lisant le fichier d'entrée"""
        print(self)

        if self.commande == "hash":
            if self.fct_hachage == "SHA1":
                msg = self.arguments[0]
                print(self.h(msg).hex().upper(), f"({msg})")

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
            start = time.time()
            print(f"chain of length {largeur}: {idx} ... {self.nouvelle_chaine(idx, largeur)}")
            end = time.time()
            print(f"Temps d'exécution de la fonction nouvelle_chaine({idx}, {largeur}) : {round(end - start, 4)} s")

        elif self.commande == "create":
            hauteur = int(self.arguments[0])
            largeur = int(self.arguments[1])
            fichier = self.arguments[2]

            start = time.time()
            self.creer_table(hauteur, largeur)
            end = time.time()
            print(f"Temps de calcul de la table : {round(end - start, 3)}s")

            self.sauve_table(fichier)

        elif self.commande == "info":
            fichier = self.arguments[0]
            self.ouvre_table(fichier)
            self.affiche_table()

        elif self.commande == "crack":
            empreinte = self.arguments[0]
            fichier = self.arguments[1]
            self.ouvre_table(fichier)

            start = time.time()
            print(f"l'inverse de {empreinte} est : ", self.inverse(self.largeur, int.from_bytes(bytes.fromhex(empreinte), "little").to_bytes(20, "little")))
            end = time.time()
            print(f"Temps de calcul de l'inverse : {round(end - start, 3)}s")

        elif self.commande == "stats":
            hauteur = int(self.arguments[0])
            largeur = int(self.arguments[1])
            self.affiche_stats(hauteur, largeur)


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


    def inverse(self, largeur:int, h:bytes):
        for t in range(largeur-1, 0, -1):
            idx = self.h2i(h, t)
            for x in range(t + 1, largeur):
                idx = self.i2i(idx, x)
            x_set = self.table.get(idx)
            if x_set:
                for x in x_set:
                    clair = self.verifie_candidat(h, t, x)
                    if clair:
                        return clair
        return None


    def verifie_candidat(self, h:bytes, t:int, idx:int):
        for i in range(1, t):
            idx = self.i2i(idx, i)

        clair = self.i2c(idx)
        if h == self.h(clair):
            return clair
        return None

    def index_aleatoire(self):
        return randint(0, self.N - 1)


    def init_table(self, hauteur: int, largeur: int ):
        self.largeur = int(largeur)
        self.hauteur = int(hauteur)
        self.table = dict()

    def fill_table(self, hauteur: int, largeur: int):
        for _ in range(hauteur):
            idx = self.index_aleatoire()
            chaine = self.nouvelle_chaine(idx, largeur)
            liste_chaines = self.table.get(chaine)
            if liste_chaines:
                liste_chaines.add(idx)
            else:
                self.table[chaine] = {idx}
        

    def creer_table(self, hauteur: int, largeur: int):
        self.init_table(hauteur, largeur)
        self.fill_table(hauteur, largeur)
        return self.table
    

    def sauve_table(self, filename: str):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)



    
    def ouvre_table(self, filename: str):
        with open(filename, 'rb') as f:
            new_self =  pickle.load(f)
        for name, value in new_self.__dict__.items():
            self.__setattr__(name, value)

    def compute_generation_time(self, hauteur: int, largeur: int):
        mini_hauteur = 20
        mini_self = self.copy(ignore_table=True)
        mini_self.init_table(mini_hauteur, largeur)
        start = time.time()
        mini_self.fill_table(mini_hauteur, largeur)
        t = time.time()-start
        return (hauteur * t/mini_hauteur)

    def affiche_stats(self, hauteur: int, largeur: int):
        m = hauteur
        v = 1.0

        for i in range(largeur):
            v = v * (1 - m / self.N)
            m = self.N * (1 - exp(-m / self.N))
        
        couverture = 100 * (1-v)

        print(f"Statistiques pour une table arc-en-ciel de hauteur de {hauteur} et une largeur de {largeur} : ")
        print(f"Couverture de la table : {round(couverture, 2)} %")
        temps_nouvelle_chaine = 0.00111 # sur une moyenne de 10000 appels à nouvelle_chaine
        print(f"Temps de génération : {round(hauteur * temps_nouvelle_chaine, 3)} s")
        print(f"Taille de la table : {self.N * (20 + 4 * 20)}") # une empreinte = 20 octets
        print(f"Temps de création estimé : {round(self.compute_generation_time(hauteur, largeur), 3)} s")


    def affiche_table(self):
        print(self)

    def copy(self, ignore_table = False):
        new_obj = self.__class__()
        if not ignore_table:
            for name, value in self.__dict__.items():
                if name != "table":
                    new_obj.__setattr__(name, value)
        else:
            for name, value in self.__dict__.items():
                new_obj.__setattr__(name, value)
        return new_obj

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