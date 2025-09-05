class FakeMouseEvent:
    def __init__(self, touch):
        self.clientX = touch.clientX
        self.clientY = touch.clientY

# Souris appuyée
def on_mouse_down(ev, terrain, fenetre):
    # Données de la souris
    rect = fenetre.canvas.getBoundingClientRect()
    mx = (ev.clientX - rect.left)*(400/fenetre.vraisTaille)
    my = (ev.clientY - rect.top)*(400/fenetre.vraisTaille)
    # Etape de jeu
    if terrain.etape_de_jeu  == 0 or terrain.etape_de_jeu  == 2:
        # Detection de la pièce cliquée
        terrain.detectionPieceClique(mx, my)
    else:
        # Detection du pion cliqué
        terrain.detectionPionClique(mx, my)

# Souris relâchée
def on_mouse_up(ev, terrain, fenetre):
    terrain.deplacement_piece = False
    rect = fenetre.canvas.getBoundingClientRect()
    mx = (ev.clientX - rect.left)*(400/fenetre.vraisTaille)
    my = (ev.clientY - rect.top)*(400/fenetre.vraisTaille)
    # Detection de la pièce relâchée
    terrain.detectionpieceRelachee(mx, my)
    # Detection du pion relâché
    terrain.detectionPionRelache(mx, my)

# Souris bouge
def on_mouse_move(ev, terrain, fenetre):
    rect = fenetre.canvas.getBoundingClientRect()
    if terrain.deplacement_piece:
        # Déplacement de la pièce
        for piece in terrain.listepieces:
            if piece.deplacement:
                mx = (ev.clientX - rect.left)*(400/fenetre.vraisTaille)
                my = (ev.clientY - rect.top)*(400/fenetre.vraisTaille)
                piece.move(mx, my)
    for pion in terrain.listepions:
        if pion.deplacement:
            # Déplacement du pion
            mx = (ev.clientX - rect.left)*(400/fenetre.vraisTaille)
            my = (ev.clientY - rect.top)*(400/fenetre.vraisTaille)
            pion.move(mx, my)

# Doigt touche
def on_touch_start(ev, terrain, fenetre):
    # Empêcher le scroll
    ev.preventDefault()
    # Premier doit
    touch = ev.touches[0]
    # faux évènement
    fake_event = FakeMouseEvent(touch)
    on_mouse_down(fake_event, terrain, fenetre)

# Doigt lâche
def on_touch_end(ev, terrain, fenetre):
    ev.preventDefault()
    touch = ev.changedTouches[0]
    # faux évènement
    fake_event = FakeMouseEvent(touch)
    on_mouse_up(fake_event, terrain, fenetre)

# Doigt bouge
def on_touch_move(ev, terrain, fenetre):
    ev.preventDefault()
    if ev.touches:
        touch = ev.touches[0]
        # faux évènement
        fake_event = FakeMouseEvent(touch)
        on_mouse_move(fake_event, terrain, fenetre)

def creer_evenement(terrain, fenetre):
    # Evenements souris
    fenetre.canvas.bind("mousedown", lambda ev: on_mouse_down(ev, terrain, fenetre))
    fenetre.canvas.bind("mouseup", lambda ev: on_mouse_up(ev, terrain, fenetre))
    fenetre.canvas.bind("mousemove", lambda ev: on_mouse_move(ev, terrain, fenetre))

    # Evenements tactile
    fenetre.canvas.bind("touchstart", lambda ev: on_touch_start(ev, terrain, fenetre))
    fenetre.canvas.bind("touchend", lambda ev: on_touch_end(ev, terrain, fenetre))
    fenetre.canvas.bind("touchmove", lambda ev: on_touch_move(ev, terrain, fenetre))