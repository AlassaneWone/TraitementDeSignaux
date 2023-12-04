# Insctruction de lancement du projet

=== Installer les dépendances ===

pip install -r requirements.txt

=== Télécharger le nécessaire au bon fonctionnement du projet ===

Un fichier qui contient un modèle CNN pré-entraîné : https://ephec-my.sharepoint.com/:f:/g/personal/he202145_students_ephec_be/EgQa70u92DZCq0Cbu9AaseABdMv9-BIUzxbVxnZgbH2zTQ?e=dGGe8Q
(Autre solution, utiliser le script image_process.py pour créer un nouveau modèle)

Dataset d'images nécessaire à l'entraînement du CNN : https://www.kaggle.com/datasets/drgfreeman/rockpaperscissors

=== Structure de fichier pour le bon fonctionnement du projet ===
.  
└── Projet-tds/  
&nbsp;&nbsp;&nbsp;&nbsp;├── Dataset/  
&nbsp;&nbsp;&nbsp;&nbsp;│   ├── paper  
&nbsp;&nbsp;&nbsp;&nbsp;│   ├── rock  
&nbsp;&nbsp;&nbsp;&nbsp;│   └── scissors  
&nbsp;&nbsp;&nbsp;&nbsp;├── image_process.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── main.py  
&nbsp;&nbsp;&nbsp;&nbsp;├── model.keras  
&nbsp;&nbsp;&nbsp;&nbsp;├── README.md  
&nbsp;&nbsp;&nbsp;&nbsp;└── requirements.txt  

=== Explication des fichiers importants ===

- image_process.py  
&nbsp;&nbsp;&nbsp;&nbsp;Un script Python pour construire, entraîner et visualiser un modèle de réseau neuronal convolutif (CNN) pour la classification d'images de signes de main représentant "pierre", "papier" ou "ciseaux". Il utilise les images du dataset ci-dessus.

- main.py  
&nbsp;&nbsp;&nbsp;&nbsp;Un script Python qui utilise OpenCV, Tkinter, et un modèle de réseau neuronal convolutif (CNN) pré-entraîné pour créer une interface utilisateur graphique (GUI) pour jouer au jeu de "pierre-papier-ciseaux" contre l'ordinateur.

- model.keras  
&nbsp;&nbsp;&nbsp;&nbsp;Un fichier qui contient un modèle de réseau neuronal convolutif (CNN) pré-entraîné. Ce modèle a été formé pour classer des images de signes de main représentant "pierre", "papier" ou "ciseaux". Il est utilisé dans main.py pour pouvoir identifier les gestes entrés par les joueurs humains.

- requirements.txt  
&nbsp;&nbsp;&nbsp;&nbsp;Un fichier utilisé par Python pour lister toutes les dépendances du projet. Chaque ligne du fichier spécifie un paquet Python et, éventuellement, une version spécifique de ce paquet.

=== Lancement du projet ===

 - Assurez-vous d'avoir installé toutes les dépendances requises pour le projet.
 - Lancez le fichier main.py à l'aide de la commande ci-dessous dans un interpreteur python:
    python main.py

Cela devrait lancer l'interface utilisateur graphique pour jouer au jeu de "pierre-papier-ciseaux" contre l'ordinateur.

Notez que vous devez vous assurer d'être dans le répertoire du projet qui contient le script main.py et le fichier model.keras. De plus, vous devez avoir une webcam connectée à votre ordinateur, car le script utilise la webcam pour capturer les images de vos gestes.
