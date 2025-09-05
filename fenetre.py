from browser import document, window

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