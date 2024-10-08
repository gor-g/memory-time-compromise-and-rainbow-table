class Config:
     def __init__(self, alphabet: str, taille: int) -> None:
         self.alphabet = alphabet
         self.taille = taille
         self.N = len(self.alphabet) ** self.taille


def read_file(filename: str):
    param = {}

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

            param["fct_hachage"] = lines[0].strip()
            param["alphabet"] = lines[1].strip()
            param["taille"] = int(lines[2].strip())
            param["commande"] = lines[3].strip()

            if len(lines) > 4:
                param["message"] = lines[4].strip()

            return param
                
    except:
        print(f"La lecture du fichier {filename} n'a pas fonctionnée...")
        return None
    

def print_help():
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