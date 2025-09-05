import piece, pion
import math

TAILLETERRAIN = pion.NOMBREPIONS - 1

class Terrain:
    def __init__(self, fenetreDeJeu):
        self.radius = fenetreDeJeu.canvas.width / (TAILLETERRAIN * 4 + 2)
        self.fenetre = fenetreDeJeu
        self.deplacement_piece = False
        self.etape_de_jeu = 0
        self.listepieces = []
        self.listepions = []
        # Contruction terrain
        cx = self.fenetre.canvas.width / 2 - ((self.radius * 0.85) * 2) * TAILLETERRAIN
        cy = self.fenetre.canvas.height / 2
        for i in range(TAILLETERRAIN*2+1):
            for j in range(max(-i, -TAILLETERRAIN), min(TAILLETERRAIN + 1, TAILLETERRAIN*2 - i + 1)):
                # Pieces du haut + pion rouge
                if j == TAILLETERRAIN:
                    self.ajouter_piece(piece.Piece(cx + j * self.radius * 0.85, cy - j * self.radius * 1.5, 0, self.radius, fenetreDeJeu))
                    self.ajouter_pion(pion.Pion(self.listepieces[len(self.listepieces)-1], "rouge", self.radius, fenetreDeJeu))
                    self.ajouter_piece(piece.Piece(cx + j * self.radius * 0.85, cy - j * self.radius * 1.5, 1, self.radius, fenetreDeJeu))
                    self.ajouter_piece(piece.Piece(cx + j * self.radius * 0.85, cy - j * self.radius * 1.5, 2, self.radius, fenetreDeJeu))
                # Pieces du bas + pion bleu
                elif j == -TAILLETERRAIN:
                    self.ajouter_piece(piece.Piece(cx + j * self.radius * 0.85, cy - j * self.radius * 1.5, 0, self.radius, fenetreDeJeu))
                    self.ajouter_pion(pion.Pion(self.listepieces[len(self.listepieces)-1], "bleu", self.radius, fenetreDeJeu))
                # Pieces du milieu
                else:
                    self.ajouter_piece(piece.Piece(cx + j * self.radius * 0.85, cy - j * self.radius * 1.5, 0, self.radius, fenetreDeJeu))
                    self.ajouter_piece(piece.Piece(cx + j * self.radius * 0.85, cy - j * self.radius * 1.5, 1, self.radius, fenetreDeJeu))
            cx += self.radius * 0.85 * 2

    def ajouter_piece(self, piece):
        self.listepieces.append(piece)

    def ajouter_pion(self, pion):
        self.listepions.append(pion)

    def changer_etape(self, fenetreDeJeu):
        if self.etape_de_jeu == 0:
            self.etape_de_jeu = 1
            for pion in self.listepions:
                if pion.equipe == "rouge":
                    pion.couleur = "#FF0000"
        elif self.etape_de_jeu == 1:
            self.etape_de_jeu = 2
            # Changer la couleur du canvas
            for pion in self.listepions:
                if pion.equipe == "rouge":
                    pion.couleur = "#FF9090"
            fenetreDeJeu.canvas.style.background = "#9090FF"
        elif self.etape_de_jeu == 2:
            for pion in self.listepions:
                if pion.equipe == "bleu":
                    pion.couleur = "#0000FF"
            self.etape_de_jeu = 3
        else:
            self.etape_de_jeu = 0
            for pion in self.listepions:
                if pion.equipe == "bleu":
                    pion.couleur = "#9090FF"
            fenetreDeJeu.canvas.style.background = "#FF9090"

    def detectionPieceClique(self, mx, my):
        # Niveau 2
        for piece in self.listepieces:
            if piece.niveau == 2 and piece.getBase(self.listepieces).pion is None:
                if piece.iscollision(mx, my):
                    piece.deplacement = True
                    self.deplacement_piece = True
                    break
        # Niveau 1
        if not self.deplacement_piece:
            for piece in self.listepieces:
                if piece.niveau == 1 and piece.getBase(self.listepieces).pion is None:
                    if piece.iscollision(mx, my):
                        piece.deplacement = True
                        self.deplacement_piece = True
                        break

    def detectionPionClique(self, mx, my):
        for pion in self.listepions:
            if pion.case.iscollision(mx, my):
                if pion.equipe == "rouge" and self.etape_de_jeu == 1 or pion.equipe == "bleu" and self.etape_de_jeu == 3:
                    pion.deplacement = True
                    break
    
    # Detection de la pièce relâchée
    def detectionpieceRelachee(self, mx, my):
        for piece in self.listepieces:
            if piece.deplacement:
                piece_cible_trouvee = False
                # Detection de la pièce cible
                for piece_cible in self.listepieces:
                    if piece_cible.getTop(self.listepieces).niveau < 2 and piece.getTop(self.listepieces) != piece_cible.getTop(self.listepieces):
                        if piece_cible.iscollision(mx, my):
                            # Deplacement de la pièce
                            piece.setPiece(piece_cible.pos[0], piece_cible.pos[1], piece_cible.getTop(self.listepieces).niveau + 1)
                            piece_cible_trouvee = True
                            self.changer_etape(self.fenetre)
                            break
                if not piece_cible_trouvee:
                    piece.setPiece(piece.pos[0], piece.pos[1], piece.niveau)
                piece.deplacement = False
    
    # Detection du pion relâché
    def detectionPionRelache(self, mx, my):
        for pion in self.listepions:
            if pion.deplacement:
                piece_cible_trouvee = False
                for piece_cible in self.listepieces:
                    if pion.equipe == "rouge" and piece_cible.getTop(self.listepieces).niveau == 2 or pion.equipe == "bleu" and piece_cible.getTop(self.listepieces).niveau == 0:
                        if piece_cible.iscollision(mx, my) and piece_cible.getBase(self.listepieces).pion is None and \
                            (math.sqrt((pion.case.pos[0] - piece_cible.pos[0])**2 + (pion.case.pos[1] - piece_cible.pos[1])**2) < self.radius * 2):
                            # Deplacement du pion
                            pion.case.pion = None
                            pion.case = piece_cible.getBase(self.listepieces)
                            piece_cible.getBase(self.listepieces).pion = pion
                            piece_cible_trouvee = True
                            self.changer_etape(self.fenetre)
                            break
                if not piece_cible_trouvee:
                    pion.move(pion.case.pos[0], pion.case.pos[1] + self.radius)
                pion.deplacement = False
    
    # Dessin du jeu
    def draw(self):
        # Pieces
        self.fenetre.ctx.clearRect(0, 0, self.fenetre.canvas.width, self.fenetre.canvas.height)
        for piece in self.listepieces:
            if piece.niveau == 0 and not piece.deplacement:
                piece.draw()
        for piece in self.listepieces:
            if piece.niveau == 1 and not piece.deplacement:
                piece.draw()
        for piece in self.listepieces:
            if piece.niveau == 2 and not piece.deplacement:
                piece.draw()
        # Pions
        for pion in self.listepions:
            pion.draw()
        # Pièce en déplacement
        for piece in self.listepieces:
            if piece.deplacement:
                piece.draw()
