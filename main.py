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

        # Mengubah warna latar belakang jendela utama menjadi biru muda (#ADD8E6)
        master.config(bg="#ADD8E6")

        # Judul Utama (teks berjalan)
        self.main_title_text = "Selamat Datang Di Game Battle Satu Dimensi Saya"
        # Mengurangi ukuran font judul utama menjadi 14
        self.main_title_label = tk.Label(master, text=self.main_title_text, font=("Helvetica", 12, "bold"), fg="black", bg="#ADD8E6")
        # Mengatur agar label rata kiri (west)
        self.main_title_label.pack(pady=10, anchor="w")
        self.scroll_pos = 0
        self.scroll_text()

        # Subjudul
        self.subtitle_label = tk.Label(master, text="~ by nabilah shafirah ~", font=("Helvetica", 10, "italic"), fg="black", bg="#ADD8E6")
        # Menambahkan sedikit padding di bawah subjudul dan mengatur rata tengah
        self.subtitle_label.pack(pady=(0, 10), anchor="s")

        ##Judul Widget OptionMenu player 1
        tk.Label(master, text="Choose Player 1 :", foreground="red", bg="#ADD8E6").pack()
        #Pull Data Dari Karakter 1
        self.player1_var = tk.StringVar()
        player1_nama = [s.nama for s in player1_list]
        self.player1_var.set(player1_nama[0])
        #Widget OptionMenu
        self.player1_menu = tk.OptionMenu(master, self.player1_var, *player1_nama, command=self.set_player1)
        self.player1_menu.pack()

        ##Judul Widget OptionMenu player 2
        tk.Label(master, text="Choose Player 2 :", foreground="red", bg="#ADD8E6").pack()
        #Pull Data Dari Karakter 2
        self.player2_var = tk.StringVar()
        player2_nama = [t.nama for t in player2_list]
        self.player2_var.set(player2_nama[0])
        #Widget OptionMenu
        self.player2_menu = tk.OptionMenu(master, self.player2_var, *player2_nama, command=self.set_player2)
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

        #widget tombol button mulai battle
        self.tombol_battle = tk.Button(master, text="Start Battle", command=self.mulai_battle)
        self.tombol_battle.pack(pady=10)
    
    def mulai_battle(self):
        self.tombol_battle.config(state="disabled")
        self.round = 1
        self.player1_hp = self.player1_obj.hp
        self.player2_hp = self.player2_obj.hp
        self.ganti_label()
        self.master.after(1000, self.auto_battle)

    def auto_battle(self):
        if self.player1_hp > 0 and self.player2_hp > 0:
            #Player 1 mengerang player 2
            self.player2_hp -= self.player1_obj.pow
            if self.player2_hp < 0:
                self.player2_hp = 0
            self.ganti_label()
            if self.player2_hp <= 0:
                messagebox.showinfo("Hasil Battle", f"{self.player2_obj.nama} Dikalahkan Oleh {self.player1_obj.nama}")
                self.tombol_battle.config(state="active")
                return
            
            #Player 2 mengerang player 1
            self.player1_hp -= self.player2_obj.pow
            if self.player1_hp < 0:
                self.player1_hp = 0
            self.ganti_label()
            if self.player1_hp <= 0:
                messagebox.showinfo("Hasil Battle", f"{self.player1_obj.nama} Dikalahkan Oleh {self.player2_obj.nama}")
                self.tombol_battle.config(state="active")
                return

            self.round += 1
            self.master.after(1000, self.auto_battle)

    def scroll_text(self):
        # Membuat teks "berbantalan" untuk memastikan perulangan yang mulus dan gulir yang tampaknya berkelanjutan
        padded_text = self.main_title_text + "        " # Menambahkan beberapa spasi untuk pemisahan

        self.scroll_pos = (self.scroll_pos + 1) % len(padded_text)
        
        # Menggeser teks untuk menciptakan efek gulir
        displayed_text = padded_text[self.scroll_pos:] + padded_text[:self.scroll_pos]
        self.main_title_label.config(text=displayed_text)
        self.master.after(150, self.scroll_text) # Sesuaikan 150 untuk kecepatan gulir (lebih rendah lebih cepat)

    def set_player1(self,value):
        for s in player1_list:
            if s.nama == value:
                self.player1_obj = s
                break
        self.player1_hp = self.player1_obj.hp
        self.player1_bar.config(maximum=self.player1_obj.hp)
        self.ganti_label()

    def set_player2(self,value):
        for t in player2_list:
            if t.nama == value:
                self.player2_obj = t
                break
        self.player2_hp = self.player2_obj.hp
        self.player2_bar.config(maximum=self.player2_obj.hp)
        self.ganti_label()

    def ganti_label(self):
        self.label_player1.config(
        text=f"{self.player1_obj.nama} HP:{self.player1_hp}")

        self.label_player2.config(
        text=f"{self.player2_obj.nama} HP:{self.player2_hp}")

        self.player1_bar["value"] = self.player1_hp
        self.player2_bar["value"] = self.player2_hp
    


root = tk.Tk()
app = BattleApp(root)
root.mainloop()