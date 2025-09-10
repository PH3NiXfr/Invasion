from browser import document, html, window

# Paramètres
parametresDeJeu = {
    "nombreDePion": 4,
    "nombreDeTours": 50
}

# Création du bouton "Paramètres"
class boutonParam:
    def __init__(self, fenetreDeJeu, nouvelle_partie):
        self.img = html.IMG(src="images/reglage.png")
        self.fenetreDeJeu = fenetreDeJeu
        # Position, taille du bouton et image
        self.x, self.y = window.innerWidth / 100, window.innerWidth / 100
        self.w, self.h = window.innerWidth / 15, window.innerWidth / 15
        self.img.bind("load", self.draw)
        
        # Fenetre
        self.fenetreParam = fenetreParam(nouvelle_partie)
        self.fenetreDeJeu.canvas.bind("click", self.on_click)
        self.fenetreDeJeu.canvas.bind("touchstart", self.on_touch)

    # Dessiner le bouton quand l’image est prête
    def draw(self, ev=None):
        self.fenetreDeJeu.ctx.drawImage(self.img, self.x, self.y, self.w/2, self.h/2)
    
    # Modification de la taille de la fenetre des paramètres
    def resize(self):
        self.x, self.y = window.innerWidth / 100, window.innerWidth / 100
        self.w, self.h = window.innerWidth / 15, window.innerWidth / 15
        if self.fenetreParam.fenetre_params.style.display == "none":
            self.fenetreParam.resize()
        else:
            self.fenetreParam.waitResize = True

    # Détection clic
    def on_click(self, ev):
        mx, my = ev.offsetX, ev.offsetY
        if self.x <= mx <= self.x+self.w*1.5 and self.y <= my <= self.y+self.h*1.5:
            self.fenetreParam.ouvrir_params(ev)
    
    # Détection touch
    def on_touch(self, ev):
        ev.preventDefault()
        touch = ev.touches[0]
        rect = self.fenetreDeJeu.canvas.getBoundingClientRect()
        mx = touch.clientX - rect.left
        my = touch.clientY - rect.top
        self._check_click(mx, my)

    # Vérifie si on clique sur le bouton
    def _check_click(self, mx, my):
        if self.x <= mx <= self.x+self.w*1.5 and self.y <= my <= self.y+self.h*1.5:
            self.fenetreParam.ouvrir_params(None)

# Fenetre des paramètres
class fenetreParam:
    def __init__(self, nouvelle_partie):
        # Données
        screen_w = window.innerWidth
        screen_h = window.innerHeight
        new_size = min(screen_w, screen_h)
        self.fenetre_params = html.DIV()
        self.waitResize = False

        # Style général de la fenêtre
        self.fenetre_params.style.background = "#88FF88"
        self.fenetre_params.style.width = f"{new_size}px"
        self.fenetre_params.style.height = f"{new_size}px"
        self.fenetre_params.style.position = "absolute"
        self.fenetre_params.style.left = f"{(screen_w - new_size)/2}px"
        self.fenetre_params.style.top  = f"{(screen_h - new_size)/2}px"
        self.fenetre_params.style.padding  = "20px"
        self.fenetre_params.style.display  = "none"
        self.fenetre_params.style.textAlign = "center"
        self.fenetre_params.style.fontFamily = "Arial, sans-serif"
        self.fenetre_params.style.fontSize = "30px"
        self.fenetre_params.style.lineHeight = "2"
        document <= self.fenetre_params
        
        # Titre
        titre = html.H1("Paramètres du jeu")
        titre.style.marginBottom = "30px"
        self.fenetre_params <= titre

        # Nombre de pions
        label = html.LABEL("Nombre de pions : ")
        label.style.fontSize = "30px"
        self.fenetre_params <= label

        self.input_nbPoins = html.INPUT(
            type="number",
            min=3,
            max=6,
            step=1,
            value=parametresDeJeu["nombreDePion"]
        )
        self.input_nbPoins.style.fontSize = "30px"
        self.input_nbPoins.style.margin = "30px"
        self.fenetre_params <= self.input_nbPoins
        self.fenetre_params <= html.BR()

        # Nombre de tours
        label = html.LABEL("Nombre de tours : ")
        label.style.fontSize = "30px"
        self.fenetre_params <= label

        self.input_nbTours = html.INPUT(
            type="number",
            min=10,
            max=500,
            step=2,
            value=parametresDeJeu["nombreDeTours"]
        )
        self.input_nbTours.style.fontSize = "30px"
        self.input_nbTours.style.margin = "30px"
        self.fenetre_params <= self.input_nbTours
        self.fenetre_params <= html.BR()

        # Choix de l'équipe qui commence
        label_equipe = html.LABEL("Équipe qui commence : ")
        label_equipe.style.fontSize = "30px"
        self.fenetre_params <= label_equipe

        self.select_equipe = html.SELECT()
        self.select_equipe.style.fontSize = "30px"
        self.select_equipe.style.margin = "30px"
        self.select_equipe <= html.OPTION("Rouge", value="rouge", selected=True)
        self.select_equipe <= html.OPTION("Bleu", value="bleu")

        self.fenetre_params <= self.select_equipe
        self.fenetre_params <= html.BR()

        # Bouton Appliquer
        self.appliquer = html.BUTTON("Appliquer")
        self.appliquer.style.fontSize = "30px"
        self.appliquer.style.padding = "12px 24px"
        self.appliquer.style.margin = "3px"
        self.appliquer.style.border = "none"
        self.appliquer.style.borderRadius = "8px"
        self.appliquer.style.background = "#4CAF50"
        self.appliquer.style.color = "white"
        self.appliquer.style.cursor = "pointer"

        # Bouton Fermer
        self.fermer = html.BUTTON("Fermer")
        self.fermer.style.fontSize = "30px"
        self.fermer.style.padding = "12px 24px"
        self.fermer.style.margin = "30px"
        self.fermer.style.border = "none"
        self.fermer.style.borderRadius = "8px"
        self.fermer.style.background = "#F44336"
        self.fermer.style.color = "white"
        self.fermer.style.cursor = "pointer"

        self.fenetre_params <= self.appliquer
        self.fenetre_params <= self.fermer

        self.creeEvent(nouvelle_partie)
    
    # Modification de la taille de la fenetre
    def resize(self):
        screen_w = window.innerWidth
        screen_h = window.innerHeight
        new_size = min(screen_w, screen_h)

        self.fenetre_params.style.background = "#88FF88"
        self.fenetre_params.style.width = f"{new_size}px"
        self.fenetre_params.style.height = f"{new_size}px"
        self.fenetre_params.style.position = "absolute"
        self.fenetre_params.style.left = f"{(screen_w - new_size)/2}px"
        self.fenetre_params.style.top  = f"{(screen_h - new_size)/2}px"
        self.fenetre_params.style.padding  = "20px"
        self.fenetre_params.style.display  = "none"
        self.fenetre_params.style.textAlign = "center"
        self.fenetre_params.style.fontFamily = "Arial, sans-serif"
        document <= self.fenetre_params

    # Action des boutons
    def ouvrir_params(self, ev):
        self.fenetre_params.style.display = "block"

    def fermer_params(self, ev):
        self.fenetre_params.style.display = "none"
        if self.waitResize:
            self.resize()

    def appliquer_params(self, ev, nouvelle_partie):
        global parametresDeJeu
        # Récupère les valeurs et les stocke
        parametresDeJeu["nombreDePion"] = float(self.input_nbPoins.value)
        parametresDeJeu["nombreDeTours"] = float(self.input_nbTours.value)
        self.fermer_params(ev)
        nouvelle_partie()

    # Event
    def creeEvent(self, nouvelle_partie):
        self.fermer.bind("click", lambda ev: self.fermer_params(ev))
        self.appliquer.bind("click", lambda ev: self.appliquer_params(ev, nouvelle_partie))