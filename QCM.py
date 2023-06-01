import random


questiondic={
                "Question": ["Si on veut mettre en évidence la présence de dihydrogène, on utilise : 1)une allumette enflammée  2)de l'eau de chaux  3)du sulfate de cuivre  réponse:",
                             "Un atome est composé : 1)D'un noyau et de protons gravitent au tour 2)D'un noyau et de neutrons gravitent au tour 3)D'un noyau et d'électrons gravitent au tour  réponse:",
                             "Une synthèse en chimie se fait par : 1)Une fusion 2)une fission 3)une reaction chimique  réponse:",
                             "Le mouvement d'un système est : 1)absolue 2)relatif 3)galiléen  réponse:",
                             "Une force peut être modélisée par : 1)un graphique 2)une fonction 3)un vecteur  réponse:",
                             "Comment appelle-t-on un référentiel dans lequel le principe d'inertie est vérifié : 1)galiléen 2)inertien 3)newtonien  réponse",
                             "La hauteur d'un son est définie par : 1)le volume sonore 2)la fréquence 3)les décibels  réponse:",
                             "Une lentille mince est caractérisée par : 1)son centre optique 2)son point focal image 3)son point focal objet 4)tout  réponse:",
                             "Un capteur transforme : 1)un signal électrique 2)une grandeur physique en un signal electrique 3)1+1=11?  réponse:",
                             "Je pense a un chiffre entre 1 et 100  réponse:"],\
                "Reponse": [1,3,3,2,3,1,2,4,2,random.randint(1,101)]
                    }


def ask():
     """fonction qui pose une question au hasard parmi la liste question"""
     random_index = random.randint(0,len(questiondic.get("Question"))-1)
     n=int(input(questiondic.get("Question")[random_index]))
     if n==questiondic.get("Reponse")[random_index]:
         return 1
     else:
         return 0


# lastScore = score
#                 done = game_loop(lastScore)

ask()












 # if hero.sprite.health <= 0:
 #            QCM.ask()
 #            if QCM.ask()==1:
 #                lastScore = score
 #                done = game_loop(lastScore)
 # score = lastScore
 # lastScore = 0