from karakter1 import player1,player1_list
from karakter2 import player2,player2_list
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class BattleApp:
    def __init__(self,master):
        self.master = master
        master.title("Battle one Dimention")
        master.geometry("400x400")

        ##Judul Widget OptionMenu player 1
        tk.Label(master, text="Choose Player 1 :", foreground="blue").pack()
        #Pull Data Dari Karakter 1
        self.player1_var = tk.StringVar()
        player1_nama = [s.nama for s in player1_list]
        self.player1_var.set(player1_nama[0])
        #Widget OptionMenu
        self.player1_menu = tk.OptionMenu(master, self.player1_var, *player1_nama)
        self.player1_menu.pack()

         ##Judul Widget OptionMenu player 2
        tk.Label(master, text="Choose Player 2 :", foreground="blue").pack()
        #Pull Data Dari Karakter 2
        self.player2_var = tk.StringVar()
        player2_nama = [t.nama for t in player2_list]
        self.player2_var.set(player2_nama[0])
        #Widget OptionMenu
        self.player2_menu = tk.OptionMenu(master, self.player2_var, *player2_nama)
        self.player2_menu.pack()

        #pull data progres bar
        self.player1_obj = player1_list[0]
        self.player2_obj = player2_list[0]
        self.player1_hp = self.player1_obj.hp
        self.player2_hp = self.player2_obj.hp

        #label progress barrrr player 1
        self.label_player1 = tk.Label(master,text=f"{self.player1_obj.nama} HP:{self.player1_hp}")
        self.label_player1.pack()
        #widget progress bar player 1
        self.player1_bar = ttk.Progressbar(master,maximum=self.player1_obj.hp, length="200")
        self.player1_bar.pack()
        self.player1_bar["value"] = self.player1_hp

        #label progress barrrr player 2
        self.label_player2 = tk.Label(master,text=f"{self.player2_obj.nama} HP:{self.player2_hp}")
        self.label_player2.pack()
        #widget progress bar player 2
        self.player2_bar = ttk.Progressbar(master,maximum=self.player2_obj.hp, length="200")
        self.player2_bar.pack()
        self.player2_bar["value"] = self.player2_hp

root = tk.Tk()
app = BattleApp(root)
root.mainloop()