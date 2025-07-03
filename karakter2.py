class player2:
    def __init__(self,nama,hp,pow):
        self.nama = nama ##label
        self.hp = hp ##progress bar
        self.pow = pow

player2_list = [
    player2("Tower", 10000, 150),
    player2("Turtle", 5000, 500),
    player2("Canon", 7500, 250),
    player2("Lancer", 7500, 350),
    player2("Infantry", 5000, 550)
]
