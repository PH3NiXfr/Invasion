from browser import document, window, html

class Fenetre:
    def __init__(self):
        self.canvas = document["game"]
        self.canvas.style.background = "#FF9090"
        self.ctx = self.canvas.getContext("2d")
        self.vraisTaille = 400

    # Choisir un ratio fixe
    def resize(self):
        # Largeur/hauteur visibles en CSS pixels
        screen_w = window.innerWidth
        screen_h = window.innerHeight

        # Taille carrée qui tient dans l’écran
        new_size = min(screen_w, screen_h)

        # Si tu veux que ce soit net sur mobile HD/Retina
        ratio = window.devicePixelRatio or 1
        self.canvas.width = int(new_size * ratio)
        self.canvas.height = int(new_size * ratio)

        # Adapter aussi la taille CSS pour qu’il apparaisse bien centré/visible
        self.canvas.style.width = f"{new_size}px"
        self.canvas.style.height = f"{new_size}px"

        # Centre le canvas en position absolue
        self.canvas.style.position = "absolute"
        self.canvas.style.left = f"{(screen_w - new_size)/2}px"
        self.canvas.style.top  = f"{(screen_h - new_size)/2}px"

        self.vraisTaille = new_size

class Score:
    def __init__(self, fenetre, nouvelle_partie):
        self.fenetre = fenetre
        self.valeur_score = [0,0,0]
        self.nouvelle_partie = nouvelle_partie

        # Bouton Rejouer
        self.rejouer = html.BUTTON("Rejouer")
        self.rejouer.style.fontSize = "18px"
        self.rejouer.style.padding = "12px 24px"
        self.rejouer.style.margin = "15px"
        self.rejouer.style.border = "none"
        self.rejouer.style.borderRadius = "8px"
        self.rejouer.style.background = "#FFFB00"
        self.rejouer.style.color = "black"
        self.rejouer.style.cursor = "pointer"
        self.rejouer.style.position = "absolute"
        self.rejouer.style.left = "-1000px"
        self.rejouer.style.top = "-1000px"
        self.rejouer.bind("click", lambda ev: self.activer_nouvelle_partie(ev))
        document <= self.rejouer

    # Nouvelle partie du bouton rejouer
    def activer_nouvelle_partie(self, ev):
        self.nouvelle_partie()
        self.rejouer.style.position = "absolute"
        self.rejouer.style.left = "-1000px"
        self.rejouer.style.top = "-1000px"

    # Calcule du score
    def calculer(self,listepions):
        self.valeur_score = [0,0,self.valeur_score[2]]
        for pion in listepions:
            if pion.equipe == "rouge":
                self.valeur_score[0] += (int((len(listepions)/2)-1) - pion.case.ry)
            else:
                self.valeur_score[1] += (int((len(listepions)/2)-1) + pion.case.ry)

    # Dessin des texte et bouton rejouer
    def draw(self, victoire=0):
        self.fenetre.ctx.fillStyle = "black"
        self.fenetre.ctx.font = "24px Arial"
        self.fenetre.ctx.textAlign = "center"
        self.fenetre.ctx.textBaseline = "middle"
        if victoire != 0:
            self.fenetre.canvas.style.background = "#FFFB00"
            self.rejouer.style.position = "absolute"
            self.rejouer.style.left = "50%"
            self.rejouer.style.top = "50%"
            self.rejouer.style.transform = "translate(-50%, -50%)"
            self.rejouer.style.zIndex = "9999"
        if victoire == 1:
            self.fenetre.ctx.fillText("Victoire de l'équipe Rouge", self.fenetre.canvas.width/2, 25)
        elif victoire == 2:
            self.fenetre.ctx.fillText("Victoire de l'équipe Bleu", self.fenetre.canvas.width/2, 25)
        elif victoire == 3:
            self.fenetre.ctx.fillText("Egalité", self.fenetre.canvas.width/2, 25)
        else:
            self.fenetre.ctx.fillText("Plus que " + str(self.valeur_score[2]), self.fenetre.canvas.width/2, 25)
        self.fenetre.ctx.fillText(str(self.valeur_score[0]) + " : Rouge / Bleu : " + str(self.valeur_score[1]), self.fenetre.canvas.width/2, 55)