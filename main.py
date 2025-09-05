from browser import timer, window, bind
import fenetre, terrain, evenement, parametres

fenetreDeJeu = fenetre.Fenetre()
fenetreDeJeu.resize()
terrainDeJeu = terrain.Terrain(fenetreDeJeu)

def nouvelle_partie():
    global fenetreDeJeu, terrainDeJeu
    terrainDeJeu.constructionTerrain()
    # Création d'une fenetre, d'un terrain et des événement
    evenement.creer_evenement(terrainDeJeu, fenetreDeJeu)

nouvelle_partie()
boutonParam = parametres.boutonParam(fenetreDeJeu, nouvelle_partie)

def boucleDeJeu():
    terrainDeJeu.draw(boutonParam)
    boutonParam.draw()

# Mise à jour automatique quand on change la taille
@bind(window, "resize")
def on_resize(ev):
    fenetreDeJeu.resize()

# Boucle du jeu (60 fps)
timer.set_interval(boucleDeJeu, 1000//60)