import piece, pion, parametres
import math

class Terrain:
    def __init__(self, fenetreDeJeu, boutonParam, score):
        self.fenetre = fenetreDeJeu
        self.boutonParam = boutonParam
        self.score = score
        self.constructionTerrain()
    
    # Contruction terrain
    def constructionTerrain(self):
        self.listepieces = []
        self.listepions = []
        self.etape_de_jeu = 0
        self.victoire = 0
        self.tailleDuTerrain = int(parametres.parametresDeJeu["nombreDePion"]) - 1
        self.score.valeur_score[2] = int(parametres.parametresDeJeu["nombreDeTours"]) + 1
        self.radius = self.fenetre.canvas.width / (self.tailleDuTerrain * 4 + 2)
        self.deplacement_piece = False
        cx = self.fenetre.canvas.width / 2 - ((self.radius * 0.85) * 2) * self.tailleDuTerrain
        cy = self.fenetre.canvas.height / 2 + self.radius
        for i in range(self.tailleDuTerrain*2+1):
            for j in range(max(-i, -self.tailleDuTerrain), min(self.tailleDuTerrain + 1, self.tailleDuTerrain*2 - i + 1)):
                # Pieces du haut + pion rouge
                if j == self.tailleDuTerrain:
                    self.ajouter_piece(piece.Piece(cx, cy, i, j, 0, self.radius, self.fenetre))
                    self.ajouter_pion(pion.Pion(self.listepieces[len(self.listepieces)-1], "rouge", self.radius, self.fenetre))
                    self.ajouter_piece(piece.Piece(cx, cy, i, j, 1, self.radius, self.fenetre))
                    self.ajouter_piece(piece.Piece(cx, cy, i, j, 2, self.radius, self.fenetre))
                # Pieces du bas + pion bleu
                elif j == -self.tailleDuTerrain:
                    self.ajouter_piece(piece.Piece(cx, cy, i, j, 0, self.radius, self.fenetre))
                    self.ajouter_pion(pion.Pion(self.listepieces[len(self.listepieces)-1], "bleu", self.radius, self.fenetre))
                # Pieces du milieu
                else:
                    self.ajouter_piece(piece.Piece(cx, cy, i, j, 0, self.radius, self.fenetre))
                    self.ajouter_piece(piece.Piece(cx, cy, i, j, 1, self.radius, self.fenetre))
            cx += self.radius * 0.85 * 2
        if self.boutonParam.fenetreParam.select_equipe.value == "rouge":
            self.etape_de_jeu = 3
            self.changer_etape()
        else:
            self.etape_de_jeu = 1
            self.changer_etape()

    def ajouter_piece(self, piece):
        self.listepieces.append(piece)

    def ajouter_pion(self, pion):
        self.listepions.append(pion)

    # Etapes de jeu
    def changer_etape(self):
        # Déplacement piece joueur rouge
        if self.etape_de_jeu == 0:
            self.etape_de_jeu = 1
            for pion in self.listepions:
                if pion.equipe == "rouge":
                    pion.gris = False
        # Déplacement pion joueur rouge
        elif self.etape_de_jeu == 1:
            self.etape_de_jeu = 2
            # Changer la couleur du canvas
            for pion in self.listepions:
                if pion.equipe == "rouge":
                    pion.gris = True
            self.fenetre.canvas.style.background = "#9090FF"
            self.score.valeur_score[2] -= 1
            # Condition de fin de jeu
            if self.score.valeur_score[2] <= 0:
                self.score.calculer(self.listepions)
                if self.score.valeur_score[0] > self.score.valeur_score[1]:
                    self.victoire = 1
                elif self.score.valeur_score[0] < self.score.valeur_score[1]:
                    self.victoire = 2
                else:
                    self.victoire = 3
        # Déplacement piece joueur bleu
        elif self.etape_de_jeu == 2:
            for pion in self.listepions:
                if pion.equipe == "bleu":
                    pion.gris = False
            self.etape_de_jeu = 3
        # Déplacement pion joueur bleu
        else:
            self.etape_de_jeu = 0
            for pion in self.listepions:
                if pion.equipe == "bleu":
                    pion.gris = True
            self.fenetre.canvas.style.background = "#FF9090"
            self.score.valeur_score[2] -= 1
            # Condition de fin de jeu
            if self.score.valeur_score[2] <= 0:
                self.score.calculer(self.listepions)
                if self.score.valeur_score[0] > self.score.valeur_score[1]:
                    self.victoire = 1
                elif self.score.valeur_score[0] < self.score.valeur_score[1]:
                    self.victoire = 2
                else:
                    self.victoire = 3
        self.score.calculer(self.listepions)

    # Deplacement d'une piece
    def detectionPieceClique(self, mx, my):
        # Niveau 2
        for piece in self.listepieces:
            if piece.niveau == 2 and piece.getBase(self.listepieces).pion is None:
                if piece.iscollision(mx, my):
                    if not piece.getBase(self.listepieces).lastAction:
                        piece.deplacement = True
                        self.deplacement_piece = True
                        break
        # Niveau 1
        if not self.deplacement_piece:
            for piece in self.listepieces:
                if piece.niveau == 1 and piece.getBase(self.listepieces).pion is None:
                    if piece.iscollision(mx, my):
                        if not piece.getBase(self.listepieces).lastAction:
                            piece.deplacement = True
                            self.deplacement_piece = True
                            break

    # Deplacement d'un pion
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
                            if not piece_cible.getBase(self.listepieces).lastAction:
                                for pieceAction in self.listepieces:
                                    if pieceAction.lastAction:
                                        pieceAction.getBase(self.listepieces).lastAction = False
                                piece.getBase(self.listepieces).lastAction = True
                                piece_cible.getBase(self.listepieces).lastAction = True
                                piece.setPiece(piece_cible, piece_cible.getTop(self.listepieces).niveau + 1)
                                piece_cible_trouvee = True
                                self.changer_etape()
                                break
                if not piece_cible_trouvee:
                    piece.setPiece(piece, piece.niveau)
                piece.deplacement = False
    
    # Detection du pion relâché
    def detectionPionRelache(self, mx, my):
        for pion in self.listepions:
            if pion.deplacement:
                piece_cible_trouvee = False
                for piece_cible in self.listepieces:
                    if (pion.equipe == "rouge" and piece_cible.getTop(self.listepieces).niveau == 2) or (pion.equipe == "bleu" and piece_cible.getTop(self.listepieces).niveau == 0):
                        if piece_cible.iscollision(mx, my) and piece_cible.getBase(self.listepieces).pion is None:
                            if ((math.sqrt((pion.case.pos[0] - piece_cible.pos[0])**2 + (pion.case.pos[1] - piece_cible.pos[1])**2) < self.radius * 2) or \
                                # déplacement à travers les bouts du terrain
                                ((pion.case.relPos[0] == 0 and piece_cible.relPos[0] + piece_cible.relPos[1] == self.tailleDuTerrain*2) or (piece_cible.relPos[0] == 0 and pion.case.relPos[0] + pion.case.relPos[1] == self.tailleDuTerrain*2)) or \
                                ((pion.case.relPos[0] == self.tailleDuTerrain*2 and piece_cible.relPos[0] == - piece_cible.relPos[1]) or (piece_cible.relPos[0] == self.tailleDuTerrain*2 and pion.case.relPos[0] == - pion.case.relPos[1]))):
                                # Deplacement du pion
                                pion.case.pion = None
                                pion.case = piece_cible.getBase(self.listepieces)
                                piece_cible.getBase(self.listepieces).pion = pion
                                piece_cible_trouvee = True
                                self.changer_etape()
                                break
                if not piece_cible_trouvee:
                    pion.move(pion.case.pos[0], pion.case.pos[1] + self.radius)
                pion.deplacement = False
    
    # Dessin du jeu
    def draw(self, boutonParam):
        self.fenetre.ctx.clearRect(0, 0, self.fenetre.canvas.width, self.fenetre.canvas.height)
        # Pieces
        piecesN0, piecesN1, piecesN2  = [], [], []
        for piece in self.listepieces:
            if not piece.deplacement:
                if piece.niveau == 0:
                    piecesN0.append(piece)
                elif piece.niveau == 1:
                    piecesN1.append(piece)
                elif piece.niveau == 2:
                    piecesN2.append(piece)

        for i in range((self.tailleDuTerrain)*2+1):
            for piece in piecesN0:
                if self.tailleDuTerrain - i == piece.ry:
                    piece.draw(self.listepieces)
            for piece in piecesN1:
                if self.tailleDuTerrain - i == piece.ry:
                    piece.draw(self.listepieces)
            for piece in piecesN2:
                if self.tailleDuTerrain - i == piece.ry:
                    piece.draw(self.listepieces)
                    
        # Pions
        for pion in self.listepions:
            pion.draw(self.listepieces)

        # Score
        self.score.draw(self.victoire)
        
        # Pièce en déplacement
        for piece in self.listepieces:
            if piece.deplacement:
                piece.draw(self.listepieces)
        boutonParam.draw()
