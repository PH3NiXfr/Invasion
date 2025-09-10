from browser import html
import math

# Chargement des images
img_montagne = html.IMG(src="images/montagne.png")
img_plaine = html.IMG(src="images/plaine.png")
img_ocean = html.IMG(src="images/ocean.png")

# Classe pièce
class Piece:
    def __init__(self, px, py, rx, ry, niveau, radius, fenetreDeJeu):
        self.deplacement = False
        self.pion = None
        self.fenetre = fenetreDeJeu
        self.radius = radius
        self.niveau = niveau
        self.px = px
        self.py = py
        self.ry = ry
        self.rx = rx
        self.lastAction = False
        self.setPiece(self,self.niveau)

    # Déplacement d'une pièce de manière relative
    def move(self, new_x, new_y):
        dx = new_x - self.points[0][0]
        dy = new_y - self.points[0][1]
        self.points = [(x + dx + self.radius, y + dy - self.radius/2) for x, y in self.points]
    
    # Déplacement d'une pièce à une position spécifique
    def setPiece(self, pieceCible, niveau):
        self.niveau = niveau
        self.ry = pieceCible.ry
        self.rx = pieceCible.rx
        self.px = pieceCible.px
        self.py = pieceCible.py
        if self.niveau == 0:
            self.dy = 0
        elif self.niveau == 1:
            self.dy = self.radius/10
        elif self.niveau == 2:
            self.dy = (self.radius/10)*2
        self.ex = pieceCible.px + self.ry * self.radius * 0.85
        self.ey = (pieceCible.py - self.ry * self.radius * 1.5) + self.ry*1.8 - self.dy
        self.points = []
        if niveau == 0:
            self.image = img_ocean
        elif niveau == 1:
            self.image = img_plaine
        elif niveau == 2:
            self.image = img_montagne
        # Calcul des points de l'hexagone
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = self.ex + self.radius * math.cos(angle)
            y = self.ey + self.radius * math.sin(angle)
            self.points.append((x, y))
        self.pos = (x, y)
        self.relPos = (self.rx, self.ry)
    
    # Détection collision point dans polygone
    def iscollision(self, mx, my):
        inside = False
        n = len(self.points)
        for i in range(n):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i+1) % n]
            if ((y1 > my) != (y2 > my)) and \
            (mx < (x2 - x1) * (my - y1) / (y2 - y1 + 1e-9) + x1):
                inside = not inside
        return inside 
    
    # Dessin d'une pièce
    def draw(self, listepieces):
        self.fenetre.ctx.beginPath()
        self.fenetre.ctx.moveTo(self.points[0][0], self.points[0][1])
        for x, y in self.points[1:]:
            self.fenetre.ctx.lineTo(x, y)
        self.fenetre.ctx.closePath()
        self.fenetre.ctx.strokeStyle = "#000000"
        self.fenetre.ctx.stroke()

        # Clip pour restreindre l’image à l’hexagone
        self.fenetre.ctx.save()
        self.fenetre.ctx.clip()

        # Bounding box de l’hexagone
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Dessiner l’image dans la bounding box
        self.fenetre.ctx.imageSmoothingEnabled = True
        self.fenetre.ctx.imageSmoothingQuality = "high"
        self.fenetre.ctx.drawImage(self.image, min_x, min_y, max_x-min_x, max_y-min_y)
        if self.getBase(listepieces).lastAction:
            self.fenetre.ctx.fillStyle = "rgba(100, 100, 100, 0.4)"
            self.fenetre.ctx.fillRect(min_x, min_y, max_x-min_x, max_y-min_y)

        self.fenetre.ctx.restore()
    
    # Recupération de la piece à la base
    def getBase(self, listepieces):
        for piece in listepieces:
            if piece.niveau == 0 and self.relPos == piece.relPos:
                return piece
            
    # Recupération de la piece au sommet
    def getTop(self, listepieces):
        piece_max = self
        for piece in listepieces:
            if self.relPos == piece.relPos and piece.niveau > piece_max.niveau:
                piece_max = piece
        return piece_max