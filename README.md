# TP1 : compromis temps / mémoire, les tables arc-en-ciel

## INFO 002

### GRIGORYAN Gor et GALERNE Julien

[Lien du sujet](https://pierre-hyvernat.apps.math.cnrs.fr/data/Enseignement/2425/info002/tp1.html)

Le TP a été codé en Python.
Il utilise les bibliothèques [`hashlib`](https://docs.python.org/3/library/hashlib.html) et [`pickle`](https://docs.python.org/3/library/pickle.html), déjà incluses dans le langage standard.

### Question 1

OK

### Question 2

OK

### Question 3

OK

```sh
$ python3 main.py test_files/01_test_file-hash.txt

fct_hachage : SHA1
alphabet : abcdefghijklmnopqrstuvwxyz
taille : 4
commande : hash
arguments : ['Salut']
N : 456976
9F57098C5534762DD32802302DB78ADA1BA864F5 (Salut)
```

### Question 4

OK

```sh
$ python3 main.py test_files/03_test_file-i2c.txt

=> i2c(1234) : ABVM
```

### Question 5 (bonus)

### Question 6

OK

```sh
$ python3 main.py test_files/04_test_file-h2i.txt

=> h2i :  5529923
```

### Question 7

OK

```sh
$ python3 main.py test_files/05_test_file-i2i.txt

=> 123 --i2c--> aaaet --h--> 54aa3686599e735f06269f56124aa4dba1847d04 --h2i(4)--> 1714296
123  --i2i(4)-->  1714296
```

```sh
$ python3 main.py test_files/06_test_file-chain.txt

=> chain of length 100: 1 ... 3560808
```

### Question 8

L'ajout de t permet d'éviter de retomber sur le même hash lorsqu'on hash successivement une chaîne.
Par exemple, si H(H(159)) = 159, si on continue à appliquer H sur 159, on va avoir des résultats pérodiques. Si on ajoute le numéro de la colonne, on aura 159+t puis, même si on retombe sur 159 au bout de n itérations, on va appliquer H sur 159+t+n et non pas 159+t.
Cela augmente la couverture de la table.

### Question 9

OK

```sh
$ python3 main.py test_files/07_test_file-create.txt

```

### Question 10

La méthode `sauve_table()` sérialise, dans un fichier .rbt, notre classe `RainbowTableManager`.
La méthode `ouvre_table()` fait l'opération inverse.

```sh
$ python3 main.py test_files/08_test_file-info.txt
```

### Question 11

```sh
$ python3 main.py test_files/09_test_file-crack.txt

=> l'inverse de A5D7A3DE259AA726E565009E4364664E923102CB est :  TSS
```

### Question 12 (bonus)

### Question 13

```sh
$ python3 main.py test_files/10_test_file-stats.txt

=> Statistiques pour une table arc-en-ciel de hauteur de 200 et une largeur de 300 :
Couverture de la table : 86.49 %
Temps de génération : 0.222 s
Taille de la table : 1757600
Temps de calcul : 0.008 s
```

```sh
$ python3 main.py test_files/11_test_file-stats.txt

=> Statistiques pour une table arc-en-ciel de hauteur de 300000 et une largeur de 3000 :
Couverture de la table : 96.57 %
Temps de génération : 333.0 s
Taille de la table : 10240000000
Temps de calcul : 12.374 s
```

### Question 14

```sh
$ python3 main.py test_files/14_test_file-stats.txt
$ python3 main.py test_files/14_test_file-create.txt
$ python3 main.py test_files/14_test_file-crack.txt
```

```sh
=> l'inverse de 16de25af888480da1af57a71855f3e8c515dcb61 est :  CODE
```
- Paramètres
    - Hauteur : 20000 
    - Largeur : 200
- Couverture de la table
    - 96.7%
- Temps de calcul de la table
    - 3.911s
- Taille de la table 
    - 123 Ko
- Temps de calcul de l'inverse
    - 0.012s


```sh
=> l'inverse de dafaa5e15a30ecd52c2d1dc6d1a3d8a0633e67e2 est :  n00b.
```
- Paramètres
    - Hauteur : 100000
    - Largeur : 1000
- Couverture de la table :
    - 51.22 %
- Temps de calcul de la table
    - 110.204s
- Taille de la table 
    - 1.07 Mo
- Temps de calcul de l'inverse
    - 0.039s

Pour les deux prochaines empreintes, on réalise les estimations suivantes :
1. 15D136678A15DDD27378777E220F501F2A729B36
- Paramètres
    - Hauteur : 1000000
    - Largeur : 10000
- Couverture de la table :
    - 79.73 %
- Temps de calcul de la table
    - 1110.0 s
- Taille de la table 
    - .
- Temps de calcul de l'inverse
    - 41.246 s

2. C50DAD1BA2A108B04AF45EBDB810ACBC78E44BFE
- Paramètres
    - Hauteur : 6000000
    - Largeur : 60000
- Couverture de la table :
    - 77.73 %
- Temps de calcul de la table
    - 6660.0 s
- Taille de la table 
    - .
- Temps de calcul de l'inverse
    - 247.478 s

### Question 15
Avec une table arc-en-ciel de hauteur de 100000000 et une largeur de 1000000, on obtient une couverture de 99.71 %.

### Question 17

Le sel permet de, pour un mot de passe donné, hacher différemment celui-ci suivant la valeur du sel.
Ainsi, deux personnes peuvent avoir un mot de passe identique mais avoir une empreinte différente, ce qui empêche l'utilisation de table arc-en-ciel.
