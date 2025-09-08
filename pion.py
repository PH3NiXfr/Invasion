import math

# Classe pion
class Pion:
    def __init__(self, case, equipe, radius, fenetreDeJeu):
        self.fenetre = fenetreDeJeu
        self.radius = radius
        self.case = case
        self.case.pion = self
        self.equipe = equipe
        self.deplacement = False
        self.x = case.pos[0]
        self.y = case.pos[1] + self.radius
        if self.equipe == "rouge":
            self.couleur = "#FF9090"
        elif self.equipe == "bleu":
            self.couleur = "#9090FF"

    # Dessin d'un pion
    def draw(self, listepieces):
        self.fenetre.ctx.beginPath()
        if not self.deplacement:
            if self.equipe == "rouge":
                self.fenetre.ctx.arc(self.case.getTop(listepieces).pos[0], self.case.getTop(listepieces).pos[1] + self.radius, self.radius/2, 0, 2 * math.pi)
            else:
                self.fenetre.ctx.arc(self.case.pos[0], self.case.pos[1] + self.radius, self.radius/2, 0, 2 * math.pi)
        else:
            self.fenetre.ctx.arc(self.x, self.y, self.radius/2, 0, 2 * math.pi)
        self.fenetre.ctx.fillStyle = self.couleur
        self.fenetre.ctx.closePath()
        self.fenetre.ctx.fill()
        self.fenetre.ctx.strokeStyle = "#000000"
        self.fenetre.ctx.stroke()
    
    # Détection collision point dans cercle
    def iscollision(self, mx, my):
        return self.case.iscollision(mx, my)

    # Déplacement d'un pion
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y