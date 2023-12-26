# Projet_RCR_-_Argumentation_2023

Énoncé du projet :
https://moodle.u-paris.fr/mod/resource/view.php?id=975445  

## Conseils d'utilisation :
Utiliser Python 3.10+.  
Placer le fichier .apx contenant les informations de l'Abstract Argumentation Framework (AF) au même niveau que le programme python (même répertoire).  
Lancer le programme à l'aide du cmd en spécifiant les paramètres de la manière suivante :  
**python3 program.py -f [nom du fichier].apx -p [type du problème] -a [ARG1,ARG2,...,ARGn]** .  
Avec **[type du problème]** = VE-CO, DC-CO, DS-CO, VE-ST, DC-ST ou DS-ST.  
Ainsi que **[ARG1,ARG2,...,ARGn]** selon les conventions de nommage des arguments : alphanumérique sensible à la case, '_' compris, et "att" et "arg" exclus.  
Dans le cas d'un problème DC-XX ou DS-XX, un seul argument ARG doit être spécifié avec -a.  
