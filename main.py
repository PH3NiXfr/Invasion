from browser import timer, window, bind
import fenetre, terrain, evenement, parametres

# Création de la fenetre
fenetreDeJeu = fenetre.Fenetre()
fenetreDeJeu.resize()

# Réinitailisation du jeu
def nouvelle_partie():
    global fenetreDeJeu, terrainDeJeu, boutonParam
    # recréation du terrain
    terrainDeJeu.constructionTerrain()
    # recréation des événement
    evenement.creer_evenement(terrainDeJeu, fenetreDeJeu)

# Création des éléments du jeu
score = fenetre.Score(fenetreDeJeu, nouvelle_partie)
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