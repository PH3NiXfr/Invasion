from browser import document, timer
import math

# Données
TAILLETERRAIN = 2
RADIUS = 20

# Init du jeu
canvas = document["game"]
ctx = canvas.getContext("2d")
width = canvas.width
height = canvas.height
dragging = False
listepieces = []

# Classe pièce
class Piece:
    def __init__(self, ex, ey, niveau):
        self.points = []
        self.deplacement = False
        self.niveau = niveau
        if niveau == 0:
            self.couleur = "#4CAF50"
        elif niveau == 1:
            self.couleur = "#FFC107"
        elif niveau == 2:
            self.couleur = "#F44336"
        # Calcul des points de l'hexagone
        for i in range(6):
            angle = math.pi / 3 * i - math.pi / 6  # rotation pour que l'hexagone pointe vers le haut
            x = ex + RADIUS * math.cos(angle)
            y = ey + RADIUS * math.sin(angle)
            self.points.append((x, y))
        self.pos = (x, y)

    # Déplacement d'une pièce de manière relative
    def mouvePiece(self, new_x, new_y):
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
            self.couleur = "#4CAF50"
        elif niveau == 1:
            self.couleur = "#FFC107"
        elif niveau == 2:
            self.couleur = "#F44336"
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
        ctx.fillStyle = self.couleur
        ctx.fill()
        ctx.strokeStyle = "#000000"
        ctx.stroke()

# Contruction terrain
cx = width / 2 - ((RADIUS * 0.85) * 2) * TAILLETERRAIN
cy = height / 2
for i in range(TAILLETERRAIN*2+1):
    for j in range(max(-i, -TAILLETERRAIN), min(TAILLETERRAIN + 1, TAILLETERRAIN*2 - i + 1)):
        # Pieces du haut
        if j == TAILLETERRAIN:
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 0))
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 1))
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 2))
        # Pieces du bas
        elif j == -TAILLETERRAIN:
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 0))
        # Pieces du milieu
        else:
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 0))
            listepieces.append(Piece(cx + j * RADIUS * 0.85, cy - j * RADIUS * 1.5, 1))
    cx += RADIUS * 0.85 * 2

# Dessin du jeu
def draw():
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
    for piece in listepieces:
        if piece.deplacement:
            piece.draw()

# Souris appuyée
def on_mouse_down(ev):
    global dragging
    # Données de la souris
    rect = canvas.getBoundingClientRect()
    mx = ev.clientX - rect.left
    my = ev.clientY - rect.top
    # Detection de la pièce cliquée (niveau 2)
    for piece in listepieces:
        if piece.niveau == 2:
            if piece.iscollision(mx, my):
                piece.deplacement = True
                dragging = True
                break
    # Detection de la pièce cliquée (niveau 1)
    if not dragging:
        for piece in listepieces:
            if piece.niveau == 1:
                if piece.iscollision(mx, my):
                    piece.deplacement = True
                    dragging = True
                    break

# Souris relâchée
def on_mouse_up(ev):
    global dragging
    dragging = False
    # Detection de la pièce relâchée
    for piece in listepieces:
        if piece.deplacement:
            piece_cible_trouvee = False
            # Detection de la pièce cible (niveau 1)
            for piece_cible in listepieces:
                if piece_cible.niveau == 1 and piece != piece_cible:
                    rect = canvas.getBoundingClientRect()
                    mx = ev.clientX - rect.left
                    my = ev.clientY - rect.top
                    if piece_cible.iscollision(mx, my):
                        # Deplacement de la pièce
                        piece.setPiece(piece_cible.pos[0], piece_cible.pos[1], 2)
                        piece_cible_trouvee = True
                        break
            # Detection de la pièce cible (niveau 0)
            for piece_cible in listepieces:
                if piece_cible.niveau == 0 and piece != piece_cible and not piece_cible_trouvee:
                    rect = canvas.getBoundingClientRect()
                    mx = ev.clientX - rect.left
                    my = ev.clientY - rect.top
                    if piece_cible.iscollision(mx, my):
                        # Deplacement de la pièce
                        piece.setPiece(piece_cible.pos[0], piece_cible.pos[1], 1)
                        piece_cible_trouvee = True
                        break
            if not piece_cible_trouvee:
                piece.setPiece(piece.pos[0], piece.pos[1], piece.niveau)
            piece.deplacement = False

# Souris bouge
def on_mouse_move(ev):
    global x, y
    if dragging:
        rect = canvas.getBoundingClientRect()
        # Déplacement de la pièce
        for piece in listepieces:
            if piece.deplacement:
                mx = ev.clientX - rect.left
                my = ev.clientY - rect.top
                piece.mouvePiece(mx, my)

# Doigt touche
def on_touch_start(ev):
    global dragging
    # Données du tactile
    rect = canvas.getBoundingClientRect()
    touch = ev.touches[0]
    mx = touch.clientX - rect.left
    my = touch.clientY - rect.top
    # Detection de la pièce touchée (niveau 2)
    for piece in listepieces:
        if piece.niveau == 2:
            if piece.iscollision(mx, my):
                piece.deplacement = True
                dragging = True
                break
    # Detection de la pièce touchée (niveau 1)
    if not dragging:
        for piece in listepieces:
            if piece.niveau == 1:
                if piece.iscollision(mx, my):
                    piece.deplacement = True
                    dragging = True
                    break

# Doigt lâche
def on_touch_end(ev):
    global dragging
    dragging = False
    # Detection de la pièce relâchée
    for piece in listepieces:
        if piece.deplacement:
            piece_cible_trouvee = False
            # Detection de la pièce cible (niveau 1)
            for piece_cible in listepieces:
                if piece_cible.niveau == 1 and piece != piece_cible:
                    rect = canvas.getBoundingClientRect()
                    mx = ev.clientX - rect.left
                    my = ev.clientY - rect.top
                    if piece_cible.iscollision(mx, my):
                        # Deplacement de la pièce
                        piece.setPiece(piece_cible.pos[0], piece_cible.pos[1], 2)
                        piece_cible_trouvee = True
                        break
            # Detection de la pièce cible (niveau 0)
            for piece_cible in listepieces:
                if piece_cible.niveau == 0 and piece != piece_cible and not piece_cible_trouvee:
                    rect = canvas.getBoundingClientRect()
                    mx = ev.clientX - rect.left
                    my = ev.clientY - rect.top
                    if piece_cible.iscollision(mx, my):
                        # Deplacement de la pièce
                        piece.setPiece(piece_cible.pos[0], piece_cible.pos[1], 1)
                        piece_cible_trouvee = True
                        break
            if not piece_cible_trouvee:
                piece.setPiece(piece.pos[0], piece.pos[1], piece.niveau)
            piece.deplacement = False
    ev.preventDefault()

# Doigt bouge
def on_touch_move(ev):
    global x, y
    if dragging:
        rect = canvas.getBoundingClientRect()
        touch = ev.touches[0]
        mx = touch.clientX - rect.left
        my = touch.clientY - rect.top
        for piece in listepieces:
            if piece.deplacement:
                piece.mouvePiece(mx, my)
    ev.preventDefault()

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