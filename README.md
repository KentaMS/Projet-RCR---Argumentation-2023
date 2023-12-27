# Projet_RCR_-_Argumentation_2023

Énoncé du projet :
https://moodle.u-paris.fr/mod/resource/view.php?id=975445  

## Conseils d'utilisation : 
- Ouvrir un cmd et se placer au même niveau que le programme python *program.py*.

- Lancer le programme à l'aide du cmd en spécifiant les paramètres de la manière suivante :

      ~$ python program.py -p [type_du_problème] -f [chemin_vers_le_fichier] -a [ARG1,ARG2,...,ARGn]
   
Avec :
-   **[type_du_problème]** = VE-CO, DC-CO, DS-CO, VE-ST, DC-ST ou DS-ST.  
-   **[ARG1,ARG2,...,ARGn]** selon les conventions de nommage des arguments : alphanumérique sensible à la case, '_' compris, et "att" et "arg" exclus.

Dans le cas d'un problème DC-XX ou DS-XX, un seul argument ARG doit être spécifié avec -a.  
* Remarque : Pour tester l'ensemble vide en tant qu'argument, il suffit d'utiliser l'option -a sans aucun argument derrière, ou bien simplement ne pas spéficier l'option du tout.

## Exemple de commandes :
Un helper récapitulant ces différentes options est disponible via la commande suivante :

    ~$ python3 program.py --help

Voici un petit exemple de quelques commandes valides :

    ~$ python3 .\program.py -p DC-CO -f test_af4.apx -a B
    YES
    ~$ python3 .\program.py -p VE-ST -f test_af1.apx -a A,C
    NO
    ~$ python3 .\program.py -p VE-CO -f test_af5.apx -a
    YES

Dans ces exemples, les fichiers se trouvent au niveau du répertoire courant.

* À noter qu'une commande invalide (par exemple, exécution de la commande avec un fichier qui n'existe pas) produira une réponse spécifiant l'erreur.

Exemple d'une commande invalide (fichier qui n'existe pas) :

    ~$ python3 .\program.py -p DS-CO -f test_file.apx -a B
    The file test_file.apx does not exist.      

Exemple d'une commande invalide (plusieurs arguments founis pour un problème de la forme DC-XX ou DS-XX) :

    ~$ python3 .\program.py -p DC-CO -f test_af3.apx -a A,D
    Only one argument should be specified for the determine problems.   
