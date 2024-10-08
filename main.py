import sys

from rainbow_table import RainbowTable

if __name__ == "__main__":
    print(f"Nombre d'arguments : {len(sys.argv)}")
    print(f"Arguments : {sys.argv}\n") 
    rbt = RainbowTable()

    if len(sys.argv) >= 2:
        rbt.load_file(sys.argv[1])

        rbt.exec_file()
    
    else:
        rbt.print_help()