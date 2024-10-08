import hashlib
import sys

from utils import read_file, Config, print_help

config = None

def hashSHA1(msg: str) -> str:
    """Question 1"""
    h = hashlib.sha1()
    h.update(msg.encode())
    
    return h.hexdigest()


def print_config(param: dict):
    global config
    config = Config(param["alphabet"], param["taille"])

    for key, value in param.items():
        print(f"{key} = {value}")
    print(f"N = {config.N}\n")


def i2c(number: int):
    """Fonction qui prend un entier et le transforme en texte clair"""
    global config
    table = []

    for i in range(config.N):
        result = ""
        for j in range(config.taille):
            alphabet = config.alphabet
            result += alphabet[(i * j) % len(alphabet)]

        table.append(result)

    print(f"Last letter = {config.alphabet[config.N % len(config.alphabet)]}")
    return table[number]


def exec_file(param: dict):
    global config
    config = Config(param["alphabet"], param["taille"])
    command = param["commande"]

    if command == "hash":
        if param["fct_hachage"] == "SHA1":
            msg = param["message"]
            print(hashSHA1(msg).upper(), f"({msg})")

    elif command == "i2c":
        print(i2c(1234))

    elif command == "config":
        print_config(param)


if __name__ == "__main__":
    print(f"Nombre d'arguments : {len(sys.argv)}")
    print(f"Arguments : {sys.argv}\n") 
    config = None

    if len(sys.argv) >= 2:
        param = read_file(sys.argv[1])

        if param != None:
            print_config(param)
            exec_file(param)
    
    else:
        print_help()