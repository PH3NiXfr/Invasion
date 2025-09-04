from browser import document, timer, window, bind
import math

# Init du jeu
NOMBREPIONS = 4
TAILLETERRAIN = NOMBREPIONS - 1
canvas = document["game"]
canvas.style.background = "#FF9090"
ctx = canvas.getContext("2d")
vraisTaille = 400

# Choisir un ratio fixe
def resize(ev=None):
    global vraisTaille

    # Largeur/hauteur visibles en CSS pixels
    screen_w = window.innerWidth
    screen_h = window.innerHeight

    # Taille carrée qui tient dans l’écran
    new_size = min(screen_w, screen_h)

    # Si tu veux que ce soit net sur mobile HD/Retina
    ratio = window.devicePixelRatio or 1
    canvas.width = int(new_size * ratio)
    canvas.height = int(new_size * ratio)

    # Adapter aussi la taille CSS pour qu’il apparaisse bien centré/visible
    canvas.style.width = f"{new_size}px"
    canvas.style.height = f"{new_size}px"
    
    # Centre le canvas en position absolue
    canvas.style.position = "absolute"
    canvas.style.left = f"{(screen_w - new_size)/2}px"
    canvas.style.top  = f"{(screen_h - new_size)/2}px"

    vraisTaille = new_size

# Premier ajustement
resize()

# Mise à jour automatique quand on change la taille (rotation mobile incluse)
@bind(window, "resize")
def on_resize(ev):
    resize(ev)

# Taille des pièces
RADIUS = canvas.width / (TAILLETERRAIN * 4 + 2)

# Variables globales
deplacement_piece = False
listepieces = []
listepions = []
etape_de_jeu = 0

# Chargement des images
img_montagne = window.Image.new()
img_montagne.src = "montagne.png"

img_plaine = window.Image.new()
img_plaine.src = "plaine.png"

img_ocean = window.Image.new()
img_ocean.src = "ocean.png"

# Classe pièce
class Piece:
    def __init__(self, ex, ey, niveau):
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
            x = ex + RADIUS * math.cos(angle)
            y = ey + RADIUS * math.sin(angle)
            self.points.append((x, y))
        self.pos = (x, y)

    # Déplacement d'une pièce de manière relative
    def move(self, new_x, new_y):
        dx = new_x - self.points[0][0]
        dy = new_y - self.points[0][1]
        self.points = [(x + dx + RADIUS, y + dy - RADIUS/2) for x, y in self.points]
    
    # Déplacement d'une pièce à une position spécifique
    def setPiece(self, new_x, new_y, niveau):
        self.points = []
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6
            x = new_x + RADIUS * math.cos(angle)
            y = new_y + RADIUS * math.sin(angle)
            self.points.append((x, y + RADIUS))
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
        ctx.beginPath()
        ctx.moveTo(self.points[0][0], self.points[0][1])
        for x, y in self.points[1:]:
            ctx.lineTo(x, y)
        ctx.closePath()
        ctx.strokeStyle = "#000000"
        ctx.stroke()

        # Clip pour restreindre l’image à l’hexagone
        ctx.save()
        ctx.clip()

        # Bounding box de l’hexagone
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Dessiner l’image dans la bounding box
        ctx.imageSmoothingEnabled = True
        ctx.imageSmoothingQuality = "high"
        ctx.drawImage(self.image, min_x, min_y, max_x-min_x, max_y-min_y)

        ctx.restore()
    
    # Recupération de la piece à la base
    def getBase(self):
        for piece in listepieces:
            if piece.niveau == 0 and self.pos == piece.pos:
                return piece
            
    # Recupération de la piece au sommet
    def getTop(self):
        piece_max = self
        for piece in listepieces:
            if self.pos == piece.pos and piece.niveau > piece_max.niveau:
                piece_max = piece
        return piece_max

# Classe pion
class Pion:
    def __init__(self, case, equipe):
        self.case = case
        self.case.pion = self
        self.equipe = equipe
        self.deplacement = False
        self.x = case.pos[0]
        self.y = case.pos[1] + RADIUS
        if self.equipe == "rouge":
            self.couleur = "#FF9090"
        elif self.equipe == "bleu":
            self.couleur = "#9090FF"

    # Dessin d'un pion
    def draw(self):
        ctx.beginPath()
        if not self.deplacement:
            ctx.arc(self.case.pos[0], self.case.pos[1] + RADIUS, RADIUS/2, 0, 2 * math.pi)
        else:
            ctx.arc(self.x, self.y, RADIUS/2, 0, 2 * math.pi)
        ctx.fillStyle = self.couleur
        ctx.closePath()
        ctx.fill()
        ctx.strokeStyle = "#000000"
        ctx.stroke()
    
    # Détection collision point dans cercle
    def iscollision(self, mx, my):
        return self.case.iscollision(mx, my)

    # Déplacement d'un pion
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

# Contruction terrain
cx = canvas.width / 2 - ((RADIUS * 0.85) * 2) * TAILLETERRAIN
cy = canvas.height / 2
for i in range(TAILLETERRAIN*2+1):
    for j in range(max(-i, -TAILLETERRAIN), min(TAILLETERRAIN + 1, TAILLETERRAIN*2 - i + 1)):
        # Pieces du haut + pion rouge
        if j == TAILLETERRAIN:
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 0))
            listepions.append(Pion(listepieces[len(listepieces)-1], "rouge"))
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 1))
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 2))
        # Pieces du bas + pion bleu
        elif j == -TAILLETERRAIN:
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 0))
            listepions.append(Pion(listepieces[len(listepieces)-1], "bleu"))
        # Pieces du milieu
        else:
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 0))
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 1))
    cx += RADIUS * 0.85 * 2

# Dessin du jeu
def draw():
    # Pieces
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    for piece in listepieces:
        if piece.niveau == 0 and not piece.deplacement:
            piece.draw()
    for piece in listepieces:
        if piece.niveau == 1 and not piece.deplacement:
            piece.draw()
    for piece in listepieces:
        if piece.niveau == 2 and not piece.deplacement:
            piece.draw()
    # Pions
    for pion in listepions:
        pion.draw()
    # Pièce en déplacement
    for piece in listepieces:
        if piece.deplacement:
            piece.draw()

# Souris appuyée
def on_mouse_down(ev):
    global deplacement_piece
    # Données de la souris
    rect = canvas.getBoundingClientRect()
    mx = (ev.clientX - rect.left)*(400/vraisTaille)
    my = (ev.clientY - rect.top)*(400/vraisTaille)
    #Etape de jeu
    if etape_de_jeu == 0 or etape_de_jeu == 2:
        # Detection de la pièce cliquée (niveau 2)
        for piece in listepieces:
            if piece.niveau == 2 and piece.getBase().pion is None:
                if piece.iscollision(mx, my):
                    piece.deplacement = True
                    deplacement_piece = True
                    break
        # Detection de la pièce cliquée (niveau 1)
        if not deplacement_piece:
            for piece in listepieces:
                if piece.niveau == 1 and piece.getBase().pion is None:
                    if piece.iscollision(mx, my):
                        piece.deplacement = True
                        deplacement_piece = True
                        break
    else:
        # Detection du pion cliqué
        for pion in listepions:
            if pion.case.iscollision(mx, my):
                if pion.equipe == "rouge" and etape_de_jeu == 1 or pion.equipe == "bleu" and etape_de_jeu == 3:
                    pion.deplacement = True
                    break

# Souris relâchée
def on_mouse_up(ev):
    global deplacement_piece
    deplacement_piece = False
    # Detection de la pièce relâchée
    for piece in listepieces:
        if piece.deplacement:
            piece_cible_trouvee = False
            # Detection de la pièce cible
            for piece_cible in listepieces:
                if piece_cible.getTop().niveau < 2 and piece.getTop() != piece_cible.getTop():
                    rect = canvas.getBoundingClientRect()
                    mx = (ev.clientX - rect.left)*(400/vraisTaille)
                    my = (ev.clientY - rect.top)*(400/vraisTaille)
                    if piece_cible.iscollision(mx, my):
                        # Deplacement de la pièce
                        piece.setPiece(piece_cible.pos[0], piece_cible.pos[1], piece_cible.getTop().niveau + 1)
                        piece_cible_trouvee = True
                        etape_suivante()
                        break
            if not piece_cible_trouvee:
                piece.setPiece(piece.pos[0], piece.pos[1], piece.niveau)
            piece.deplacement = False
    for pion in listepions:
        if pion.deplacement:
            piece_cible_trouvee = False
            for piece_cible in listepieces:
                if pion.equipe == "rouge" and piece_cible.getTop().niveau == 2 or pion.equipe == "bleu" and piece_cible.getTop().niveau == 0:
                    rect = canvas.getBoundingClientRect()
                    mx = (ev.clientX - rect.left)*(400/vraisTaille)
                    my = (ev.clientY - rect.top)*(400/vraisTaille)
                    if piece_cible.iscollision(mx, my) and piece_cible.getBase().pion is None and \
                        (math.sqrt((pion.case.pos[0] - piece_cible.pos[0])**2 + (pion.case.pos[1] - piece_cible.pos[1])**2) < RADIUS * 2):
                        # Deplacement du pion
                        pion.case.pion = None
                        pion.case = piece_cible.getBase()
                        piece_cible.getBase().pion = pion
                        piece_cible_trouvee = True
                        etape_suivante()
                        break
            if not piece_cible_trouvee:
                pion.move(pion.case.pos[0], pion.case.pos[1] + RADIUS)
            pion.deplacement = False

def etape_suivante():
    global etape_de_jeu
    if etape_de_jeu == 0:
        etape_de_jeu = 1
        for pion in listepions:
            if pion.equipe == "rouge":
                pion.couleur = "#FF0000"
    elif etape_de_jeu == 1:
        etape_de_jeu = 2
        # Changer la couleur du canvas
        for pion in listepions:
            if pion.equipe == "rouge":
                pion.couleur = "#FF9090"
        canvas.style.background = "#9090FF"
    elif etape_de_jeu == 2:
        for pion in listepions:
            if pion.equipe == "bleu":
                pion.couleur = "#0000FF"
        etape_de_jeu = 3
    else:
        etape_de_jeu = 0
        for pion in listepions:
            if pion.equipe == "bleu":
                pion.couleur = "#9090FF"
        canvas.style.background = "#FF9090"

# Souris bouge
def on_mouse_move(ev):
    global x, y
    rect = canvas.getBoundingClientRect()
    if deplacement_piece:
        # Déplacement de la pièce
        for piece in listepieces:
            if piece.deplacement:
                mx = (ev.clientX - rect.left)*(400/vraisTaille)
                my = (ev.clientY - rect.top)*(400/vraisTaille)
                piece.move(mx, my)
    for pion in listepions:
        if pion.deplacement:
            mx = (ev.clientX - rect.left)*(400/vraisTaille)
            my = (ev.clientY - rect.top)*(400/vraisTaille)
            pion.move(mx, my)

class FakeMouseEvent:
    def __init__(self, touch):
        self.clientX = touch.clientX
        self.clientY = touch.clientY

# Doigt touche
def on_touch_start(ev):
    # Empêcher le scroll
    ev.preventDefault()
    # Premier doit
    touch = ev.touches[0]
    # faux évènement
    fake_event = FakeMouseEvent(touch)
    on_mouse_down(fake_event)

# Doigt lâche
def on_touch_end(ev):
    ev.preventDefault()
    touch = ev.changedTouches[0]
    # faux évènement
    fake_event = FakeMouseEvent(touch)
    on_mouse_up(fake_event)

# Doigt bouge
def on_touch_move(ev):
    ev.preventDefault()
    if ev.touches:
        touch = ev.touches[0]
        # faux évènement
        fake_event = FakeMouseEvent(touch)
        on_mouse_move(fake_event)

# Evenements souris
canvas.bind("mousedown", on_mouse_down)
canvas.bind("mouseup", on_mouse_up)
canvas.bind("mousemove", on_mouse_move)

# Evenements tactile
canvas.bind("touchstart", on_touch_start)
canvas.bind("touchend", on_touch_end)
canvas.bind("touchmove", on_touch_move)

# Boucle du jeu (60 fps)
timer.set_interval(draw, 1000//60)