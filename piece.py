from browser import html
import math

# Chargement des images
img_montagne = html.IMG(src="montagne.png")

img_plaine = html.IMG(src="plaine.png")

img_ocean = html.IMG(src="ocean.png")

# Classe pièce
class Piece:
    def __init__(self, ex, ey, niveau, radius, fenetreDeJeu):
        self.radius = radius
        self.fenetre = fenetreDeJeu
        self.points = []
        self.deplacement = False
        self.niveau = niveau
        self.pion = None
        if niveau == 0:
            self.image = img_ocean
        elif niveau == 1:
            self.image = img_plaine
        elif niveau == 2:
            self.image = img_montagne
        # Calcul des points de l'hexagone
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6  # rotation pour que l'hexagone pointe vers le haut
            x = ex + self.radius * math.cos(angle)
            y = ey + self.radius * math.sin(angle)
            self.points.append((x, y))
        self.pos = (x, y)

    # Déplacement d'une pièce de manière relative
    def move(self, new_x, new_y):
        dx = new_x - self.points[0][0]
        dy = new_y - self.points[0][1]
        self.points = [(x + dx + self.radius, y + dy - self.radius/2) for x, y in self.points]
    
    # Déplacement d'une pièce à une position spécifique
    def setPiece(self, new_x, new_y, niveau):
        self.points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = new_x + self.radius * math.cos(angle)
            y = new_y + self.radius * math.sin(angle)
            self.points.append((x, y + self.radius))
        self.pos = (new_x, new_y)
        if niveau == 0:
            self.image = img_ocean
        elif niveau == 1:
            self.image = img_plaine
        elif niveau == 2:
            self.image = img_montagne
        self.niveau = niveau
    
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
    def draw(self):
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

        self.fenetre.ctx.restore()
    
    # Recupération de la piece à la base
    def getBase(self, listepieces):
        for piece in listepieces:
            if piece.niveau == 0 and self.pos == piece.pos:
                return piece
            
    # Recupération de la piece au sommet
    def getTop(self, listepieces):
        piece_max = self
        for piece in listepieces:
            if self.pos == piece.pos and piece.niveau > piece_max.niveau:
                piece_max = piece
        return piece_max