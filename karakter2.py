class player2:
    def __init__(self,nama,hp,pow):
        self.nama = nama ##label
        self.hp = hp ##progress bar
        self.pow = pow

player2_list = [
    player2("Tower", 1000, 150),
    player2("Turtle", 500, 500),
    player2("Canon", 750, 250),
    player2("Lancer", 750, 350),
    player2("Infantry", 500, 550)
]