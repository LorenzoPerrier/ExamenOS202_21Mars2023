Lorenzo Perrier de La Bâthie

##Introduction

Quel est le nombre de coeurs physiques de votre machine ?
4 coeurs

Quel est le nombre de coeurs logiques de votre machine ?
8 coeurs logiques

Quelle est la quantité de mémoire cache L2 et L3 de votre machine ?
L2 : 1,0 Mo
L3 : 6,0 Mo

Ex1 : Parallélisation

1. Pour faire la parallélisation, j'ai attribué à l'aide du modulo, un calcule d'un résultat à chacun des process. Comme ce sont à chaque fois des caculs qui se font indépendamment, une telle parallélisation ne requiert aucune communication entre les process. Pour évaluer le speed up d'une telle parallélisation, j'ai ajouté une variable qui calcul le temps d'exécution du process 0. En effet, j'ai également caculé le temps total passé au calcul et à l'affichage mais celui ci ne reflète pas la réalité car les calculs se font en parallèle !
