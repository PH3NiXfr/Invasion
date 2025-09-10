from browser import html
import math

# Chargement des images
img_pionRouge = html.IMG(src="images/pionRouge.png")
img_pionBleu = html.IMG(src="images/pionBleu.png")

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
        self.gris = True
        if self.equipe == "rouge":
            self.image = img_pionRouge
        elif self.equipe == "bleu":
            self.image = img_pionBleu

    # Dessin d'un pion
    def draw(self, listepieces):
        self.fenetre.ctx.beginPath()
        if not self.deplacement:
            if self.equipe == "rouge":
                x, y = self.case.getTop(listepieces).pos[0], self.case.getTop(listepieces).pos[1] + self.radius
            else:
                x, y = self.case.pos[0], self.case.pos[1] + self.radius
        else:
            x, y = self.x, self.y
        self.fenetre.ctx.arc(x, y, self.radius/2, 0, 2 * math.pi)
        self.fenetre.ctx.closePath()
        self.fenetre.ctx.save()
        self.fenetre.ctx.clip()
        self.fenetre.ctx.drawImage(self.image, x - self.radius/2, y - self.radius/2, self.radius, self.radius)
        if self.gris:
            self.fenetre.ctx.fillStyle = "rgba(128,128,128,0.4)"
            self.fenetre.ctx.fillRect(x - self.radius/2, y - self.radius/2, self.radius, self.radius)
        self.fenetre.ctx.restore()
        self.fenetre.ctx.strokeStyle = "#000000"
        self.fenetre.ctx.stroke()
    
    # Détection collision point dans cercle
    def iscollision(self, mx, my):
        return self.case.iscollision(mx, my)

    # Déplacement d'un pion
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y