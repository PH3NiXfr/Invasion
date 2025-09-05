from browser import document, html, window

parametresDeJeu = {
    "nombreDePion": 4
}

# Création du bouton "Paramètres"
class boutonParam:
    def __init__(self, fenetreDeJeu, nouvelle_partie):
        self.img = html.IMG(src="images/reglage.png")
        self.fenetreDeJeu = fenetreDeJeu
        # Position et taille du bouton
        self.x, self.y = 0, 0
        self.w, self.h = window.innerWidth / 15, window.innerWidth / 15
        
        self.fenetreParam = fenetreParam(nouvelle_partie)

        self.img.bind("load", self.draw)
        
        self.fenetreDeJeu.canvas.bind("click", self.on_click)
        self.fenetreDeJeu.canvas.bind("touchstart", self.on_touch)

    # Dessiner le bouton quand l’image est prête
    def draw(self, ev=None):
        self.fenetreDeJeu.ctx.drawImage(self.img, self.x, self.y, self.w, self.h)

    # Détection clic
    def on_click(self, ev):
        mx, my = ev.offsetX, ev.offsetY
        if self.x <= mx <= self.x+self.w*1.5 and self.y <= my <= self.y+self.h*1.5:
            self.fenetreParam.ouvrir_params(ev)
    
    # Détection touch
    def on_touch(self, ev):
        ev.preventDefault()  # empêche le scroll / zoom lors du touch
        touch = ev.touches[0]  # prendre le premier doigt
        # Calculer la position relative au canvas
        rect = self.fenetreDeJeu.canvas.getBoundingClientRect()
        mx = touch.clientX - rect.left
        my = touch.clientY - rect.top
        self._check_click(mx, my)

    # Vérifie si on clique sur le bouton
    def _check_click(self, mx, my):
        if self.x <= mx <= self.x+self.w*1.5 and self.y <= my <= self.y+self.h*1.5:
            self.fenetreParam.ouvrir_params(None)
    

class fenetreParam:
    def __init__(self, nouvelle_partie):
        # Création de la fenêtre de paramètres (cachée par défaut)
        self.fenetre_params = html.DIV(
            style={
                "position": "absolute",
                "width": "300px",
                "height": "200px",
                "background": "#eee",
                "border": "2px solid #333",
                "padding": "10px",
                "display": "none",  # cachée au départ
                "top": "50px",
                "left": "50px",
                "z-index": "1000"
            }
        )
        document <= self.fenetre_params

        # Ajout du contenu à la fenêtre
        self.fenetre_params <= html.H3("Paramètres du jeu")

        # Input Vitesse
        self.fenetre_params <= html.LABEL("Nombre de pion : ")
        self.input_nbPoins = html.INPUT(type="number", min=3, max=6, step=1, value=parametresDeJeu["nombreDePion"])
        self.fenetre_params <= self.input_nbPoins
        self.fenetre_params <= html.BR()

        # Bouton appliquer
        self.appliquer = html.BUTTON("Appliquer")
        self.fenetre_params <= self.appliquer

        # Bouton fermer
        self.fermer = html.BUTTON("Fermer", style={"margin-left": "10px"})
        self.fenetre_params <= self.fermer

        self.creeEvent(nouvelle_partie)

    # Fonctions
    def ouvrir_params(self, ev):
        self.fenetre_params.style.display = "block"

    def fermer_params(self, ev):
        self.fenetre_params.style.display = "none"

    def appliquer_params(self, ev, nouvelle_partie):
        global parametresDeJeu
        # Récupère les valeurs et les stocke
        parametresDeJeu["nombreDePion"] = float(self.input_nbPoins.value)
        self.fermer_params(ev)
        nouvelle_partie()

    # Liaisons
    def creeEvent(self, nouvelle_partie):
        self.fermer.bind("click", lambda ev: self.fermer_params(ev))
        self.appliquer.bind("click", lambda ev: self.appliquer_params(ev, nouvelle_partie))