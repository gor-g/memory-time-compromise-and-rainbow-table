# TP1 : compromis temps / mémoire, les tables arc-en-ciel

## INFO 002

### GRIGORYAN Gor et GALERNE Julien

[Lien du sujet](https://pierre-hyvernat.apps.math.cnrs.fr/data/Enseignement/2425/info002/tp1.html)

Exécuter le TP :

```sh
$ python3 main.py
```

```sh
$ python3 main.py test_files/01_test_file-hash.txt
```

```sh
$ python3 main.py test_files/02_test_file-config.txt
```

### Question 1

OK

### Question 2

OK

### Question 3

OK

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

### Question 9
```sh
$ python3 main.py test_files/07_test_file-create.txt

```

### Question 10
```sh
$ python3 main.py test_files/08_test_file-info.txt
```

### Question 17

Le sel permet de, pour un mot de passe donné, hacher différemment celui-ci suivant la valeur du sel.
Ainsi, deux personnes peuvent avoir un mot de passe identique mais avoir une empreinte différente.
