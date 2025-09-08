from browser import timer, window, bind
import fenetre, terrain, evenement, parametres

fenetreDeJeu = fenetre.Fenetre()
score = fenetre.Score(fenetreDeJeu)
fenetreDeJeu.resize()

def nouvelle_partie():
    global fenetreDeJeu, terrainDeJeu, boutonParam
    terrainDeJeu.constructionTerrain()
    # Création d'une fenetre, d'un terrain et des événement
    evenement.creer_evenement(terrainDeJeu, fenetreDeJeu)

boutonParam = parametres.boutonParam(fenetreDeJeu, nouvelle_partie)
terrainDeJeu = terrain.Terrain(fenetreDeJeu, boutonParam, score)

nouvelle_partie()

def boucleDeJeu():
    terrainDeJeu.draw(boutonParam)
    boutonParam.draw()

# Mise à jour automatique quand on change la taille
@bind(window, "resize")
def on_resize(ev):
    fenetreDeJeu.resize()
    boutonParam.resize()

# Boucle du jeu (60 fps)
timer.set_interval(boucleDeJeu, 1000//60)