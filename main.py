from browser import timer, window, bind
import fenetre, terrain, evenement

# Création d'une fenetre, d'un terrain et des événements
fenetreDeJeu = fenetre.Fenetre()
fenetreDeJeu.resize()
terrainDeJeu = terrain.Terrain(fenetreDeJeu)
evenement.creer_evenement(terrainDeJeu, fenetreDeJeu)

# Mise à jour automatique quand on change la taille
@bind(window, "resize")
def on_resize(ev):
    fenetreDeJeu.resize()

# Boucle du jeu (60 fps)
timer.set_interval(terrainDeJeu.draw, 1000//60)