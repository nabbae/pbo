from karakter1 import player1, player1_list
from karakter2 import player2, player2_list
from boss import Boss, boss_list # Impor Boss dan boss_list
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class BattleApp:
    def __init__(self,master):
        self.master = master
        master.title("Battle one Dimention")
        # Perbesar window untuk mengakomodasi elemen UI baru
        master.geometry("450x550") 

        master.config(bg="#ADD8E6")

        self.main_title_text = "Selamat Datang Di Game Battle Satu Dimensi Kami"
        self.main_title_label = tk.Label(master, text=self.main_title_text, font=("Helvetica", 12, "bold"), fg="black", bg="#ADD8E6")
        self.main_title_label.pack(pady=10, anchor="w")
        self.scroll_pos = 0
        self.scroll_text()

        subtitle_text = """~ by ~
Nabilah Shafirah
Muhammad Ikhwan Nurfaqih
Ajrul Mustaram
Nabilla De Estika
Fathiyah Ramadhani"""
        self.subtitle_label = tk.Label(master, text=subtitle_text, justify=tk.CENTER, font=("Helvetica", 10, "italic"), fg="black", bg="#ADD8E6")
        self.subtitle_label.pack(pady=(0, 10), anchor="s")

        # --- Pilihan Mode Permainan ---
        self.game_mode = tk.StringVar(value="PvP") # Default PvP

        mode_frame = tk.Frame(master, bg="#ADD8E6")
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Pilih Mode:", font=("Helvetica", 10, "bold"), bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="Player vs Player", variable=self.game_mode, value="PvP", command=self.update_ui_for_mode, bg="#ADD8E6", font=("Helvetica", 9)).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Player vs Boss", variable=self.game_mode, value="PvB", command=self.update_ui_for_mode, bg="#ADD8E6", font=("Helvetica", 9)).pack(side=tk.LEFT)

        # --- Pemilihan Player 1 ---
        tk.Label(master, text="Choose Player 1 :", foreground="red", bg="#ADD8E6", font=("Helvetica", 10, "bold")).pack()
        self.player1_var = tk.StringVar()
        player1_nama = [s.nama for s in player1_list]
        if player1_nama:
            self.player1_var.set(player1_nama[0])
        self.player1_menu = tk.OptionMenu(master, self.player1_var, *player1_nama, command=self.set_player1)
        self.player1_menu.pack()

        # --- Frame untuk Lawan (Player 2 atau Boss) ---
        self.opponent_frame = tk.Frame(master, bg="#ADD8E6")
        self.opponent_frame.pack(pady=5)

        # Widget untuk Player 2 (awalnya dibuat, visibilitas diatur oleh update_ui_for_mode)
        self.player2_label_widget = tk.Label(self.opponent_frame, text="Choose Player 2 :", foreground="blue", bg="#ADD8E6", font=("Helvetica", 10, "bold"))
        self.player2_var = tk.StringVar()
        player2_nama = [t.nama for t in player2_list]
        if player2_nama:
            self.player2_var.set(player2_nama[0])
        self.player2_menu = tk.OptionMenu(self.opponent_frame, self.player2_var, *player2_nama, command=self.set_player2)
        
        # Widget untuk Boss (awalnya dibuat, visibilitas diatur oleh update_ui_for_mode)
        self.boss_label_widget = tk.Label(self.opponent_frame, text="Pilih Boss:", foreground="purple", bg="#ADD8E6", font=("Helvetica", 10, "bold")) # Diubah dari "Melawan Boss:"
        # self.boss_name_display_label = tk.Label(self.opponent_frame, text="", font=("Helvetica", 10), bg="#ADD8E6") # Dihapus, diganti OptionMenu
        
        # Variabel dan OptionMenu untuk pilihan Boss
        self.boss_var = tk.StringVar()
        boss_nama_list = [b.nama for b in boss_list]
        if boss_nama_list:
            self.boss_var.set(boss_nama_list[0])
        self.boss_menu = tk.OptionMenu(self.opponent_frame, self.boss_var, *boss_nama_list, command=self.set_boss)


        # --- Inisialisasi Objek dan HP ---
        self.player1_obj = player1_list[0] if player1_list else None
        self.player2_obj = player2_list[0] if player2_list else None
        # self.boss_obj = boss_list[0] if boss_list else None # Inisialisasi boss_obj akan dihandle di set_boss atau update_ui_for_mode
        if boss_list:
            initial_boss_name = self.boss_var.get()
            self.boss_obj = next((b for b in boss_list if b.nama == initial_boss_name), boss_list[0])
        else:
            self.boss_obj = None


        self.player1_hp = self.player1_obj.hp if self.player1_obj else 0
        
        # HP dan nama lawan akan di-set lebih lanjut di update_ui_for_mode
        self.opponent_obj = None 
        self.opponent_hp = 0
        self.opponent_name = "" # Nama lawan untuk display

        # --- Progress Bar Player 1 ---
        self.label_player1 = tk.Label(master,text="", bg="#ADD8E6", font=("Helvetica", 9)) # Teks diatur di ganti_label
        self.label_player1.pack()
        self.player1_bar = ttk.Progressbar(master, length="250") # Max diatur di set_player1/ganti_label
        self.player1_bar.pack()
        
        # --- Progress Bar Lawan (Player 2 atau Boss) ---
        self.label_opponent = tk.Label(master,text="", bg="#ADD8E6", font=("Helvetica", 9)) # Teks diatur di ganti_label
        self.label_opponent.pack()
        self.opponent_bar = ttk.Progressbar(master, length="250") # Max diatur di update_ui_for_mode/ganti_label
        self.opponent_bar.pack()
        
        self.tombol_battle = tk.Button(master, text="Start Battle", command=self.mulai_battle, font=("Helvetica", 10, "bold"))
        self.tombol_battle.pack(pady=15)

        # Panggil update_ui_for_mode untuk setup UI awal berdasarkan mode default dan inisialisasi objek
        self.update_ui_for_mode() 
        # Panggil set_player1 juga untuk memastikan player1_obj dan barnya terinisialisasi dengan benar
        if self.player1_obj:
            self.set_player1(self.player1_var.get())


    def update_ui_for_mode(self):
        mode = self.game_mode.get()
        
        # Sembunyikan semua widget lawan spesifik mode dulu
        self.player2_label_widget.pack_forget()
        self.player2_menu.pack_forget()
        self.boss_label_widget.pack_forget()
        # self.boss_name_display_label.pack_forget() # Sudah dihapus
        self.boss_menu.pack_forget()


        if mode == "PvP":
            self.player2_label_widget.pack()
            if player2_list :
                 self.player2_menu.pack()
                 # Jika self.player2_obj belum ada atau tidak sesuai dengan var (misal setelah switch mode)
                 current_p2_name = self.player2_var.get()
                 selected_p2 = next((p for p in player2_list if p.nama == current_p2_name), None)
                 if selected_p2:
                     self.player2_obj = selected_p2
                 elif player2_list: # Fallback ke player pertama jika nama tidak valid
                     self.player2_obj = player2_list[0]
                     self.player2_var.set(self.player2_obj.nama)
                 
                 if self.player2_obj:
                     self.opponent_obj = self.player2_obj
                     self.opponent_name = self.player2_obj.nama
                     self.opponent_hp = self.player2_obj.hp
                     self.opponent_bar.config(maximum=self.player2_obj.hp)
                 else: # Seharusnya tidak terjadi jika player2_list tidak kosong
                    self.opponent_name = "Pilih Player 2"
                    self.opponent_hp = 0
                    self.opponent_bar.config(maximum=1)
            else:
                 self.opponent_name = "Tidak Ada Player 2"
                 self.opponent_hp = 0
                 self.opponent_obj = None
                 self.opponent_bar.config(maximum=1)
            
        elif mode == "PvB":
            self.boss_label_widget.pack() # Tampilkan label "Pilih Boss:"
            self.boss_menu.pack() # Tampilkan OptionMenu untuk Boss

            if boss_list:
                # Set boss_obj berdasarkan pilihan di boss_var
                current_boss_name = self.boss_var.get()
                selected_boss = next((b for b in boss_list if b.nama == current_boss_name), None)
                if selected_boss:
                    self.boss_obj = selected_boss
                elif boss_list: # Fallback jika nama tidak valid (seharusnya tidak terjadi dengan OptionMenu)
                    self.boss_obj = boss_list[0]
                    self.boss_var.set(self.boss_obj.nama)
                
                if self.boss_obj:
                    self.opponent_obj = self.boss_obj
                    self.opponent_name = self.boss_obj.nama
                    self.opponent_hp = self.boss_obj.hp
                    self.opponent_bar.config(maximum=self.boss_obj.hp)
                else: # Seharusnya tidak terjadi jika boss_list tidak kosong
                    self.opponent_name = "Pilih Boss"
                    self.opponent_hp = 0
                    self.opponent_bar.config(maximum=1)

            else: # boss_list kosong
                self.opponent_name = "Tidak Ada Boss Tersedia"
                self.opponent_hp = 0
                self.opponent_obj = None
                self.opponent_bar.config(maximum=1)
                self.boss_menu.pack_forget() # Sembunyikan menu jika tidak ada boss
        
        self.ganti_label()

    def mulai_battle(self):
        if not self.player1_obj:
            messagebox.showerror("Error", "Player 1 tidak dipilih atau tidak tersedia.")
            return
        if not self.opponent_obj:
            messagebox.showerror("Error", "Lawan (Player 2 atau Boss) tidak tersedia.")
            return

        self.tombol_battle.config(state="disabled")
        self.round = 1
        
        # Reset HP player 1 ke max HP dari objeknya
        self.player1_hp = self.player1_obj.hp
        
        # Reset HP lawan ke max HP dari objeknya
        self.opponent_hp = self.opponent_obj.hp
            
        self.ganti_label() # Update label sebelum battle dimulai
        self.master.after(1000, self.auto_battle) # auto_battle akan diubah di step selanjutnya

    def auto_battle(self):
        if not self.player1_obj or not self.opponent_obj:
            messagebox.showerror("Error", "Objek pemain atau lawan tidak terinisialisasi dengan benar.")
            self.tombol_battle.config(state="active")
            return

        mode = self.game_mode.get()
        player1_wins = False
        opponent_wins = False

        if self.player1_hp > 0 and self.opponent_hp > 0:
            # --- Giliran Player 1 Menyerang ---
            damage_by_player1 = self.player1_obj.pow
            self.opponent_hp -= damage_by_player1
            if self.opponent_hp < 0:
                self.opponent_hp = 0
            
            print(f"Round {self.round}: {self.player1_obj.nama} menyerang {self.opponent_name}. Damage: {damage_by_player1}. {self.opponent_name} HP: {self.opponent_hp}")

            self.ganti_label() # Update UI segera setelah serangan Player 1

            if self.opponent_hp <= 0:
                player1_wins = True
            
            # --- Giliran Lawan Menyerang (jika belum kalah) ---
            if not player1_wins:
                opponent_attack_power = 0
                if mode == "PvP":
                    opponent_attack_power = self.opponent_obj.pow
                elif mode == "PvB":
                    # Boss menyerang dengan pow konstan
                    if self.opponent_obj: # Pastikan opponent_obj (Boss) ada
                        opponent_attack_power = self.opponent_obj.pow
                    else:
                        opponent_attack_power = 0 # Tidak ada Boss, tidak ada damage
                
                self.player1_hp -= opponent_attack_power
                if self.player1_hp < 0:
                    self.player1_hp = 0

                print(f"Round {self.round}: {self.opponent_name} menyerang {self.player1_obj.nama}. Damage: {opponent_attack_power}. {self.player1_obj.nama} HP: {self.player1_hp}")
                
                self.ganti_label() # Update UI segera setelah serangan Lawan

                if self.player1_hp <= 0:
                    opponent_wins = True
            
            # --- Cek Kondisi Akhir dan Lanjutkan atau Stop ---
            if player1_wins:
                winner_name = self.player1_obj.nama
                loser_name = self.opponent_name
                if mode == "PvB": loser_name += " (Boss)"
                messagebox.showinfo("Hasil Battle", f"{loser_name} Dikalahkan Oleh {winner_name}!\n{winner_name} Menang!")
                self.tombol_battle.config(state="active")
                return 
            
            if opponent_wins:
                winner_name = self.opponent_name
                if mode == "PvB": winner_name += " (Boss)"
                loser_name = self.player1_obj.nama
                messagebox.showinfo("Hasil Battle", f"{loser_name} Dikalahkan Oleh {winner_name}!\n{winner_name} Menang!")
                self.tombol_battle.config(state="active")
                return

            self.round += 1
            self.master.after(1000, self.auto_battle)
        else:
            # Jika salah satu HP sudah 0 di awal pemanggilan fungsi (seharusnya sudah ditangani di atas)
            self.tombol_battle.config(state="active")
            # Tambahan: Tampilkan pesan jika game berakhir karena salah satu HP sudah 0 sebelum giliran
            if self.player1_hp <= 0 and not opponent_wins: # jika P1 kalah sebelum giliran lawan sempat tercatat
                 winner_name = self.opponent_name
                 if mode == "PvB": winner_name += " (Boss)"
                 messagebox.showinfo("Hasil Battle", f"{self.player1_obj.nama} Dikalahkan Oleh {winner_name}!\n{winner_name} Menang!")
            elif self.opponent_hp <= 0 and not player1_wins: # jika lawan kalah sebelum giliran P1 sempat tercatat
                 winner_name = self.player1_obj.nama
                 loser_name = self.opponent_name
                 if mode == "PvB": loser_name += " (Boss)"
                 messagebox.showinfo("Hasil Battle", f"{loser_name} Dikalahkan Oleh {winner_name}!\n{winner_name} Menang!")


    def scroll_text(self):
        padded_text = self.main_title_text + "        "
        self.scroll_pos = (self.scroll_pos + 1) % len(padded_text)
        displayed_text = padded_text[self.scroll_pos:] + padded_text[:self.scroll_pos]
        self.main_title_label.config(text=displayed_text)
        self.master.after(150, self.scroll_text)

    def set_player1(self,value):
        selected_p1 = next((s for s in player1_list if s.nama == value), None)
        if selected_p1:
            self.player1_obj = selected_p1
            self.player1_hp = self.player1_obj.hp # Reset HP saat ganti karakter
            self.player1_bar.config(maximum=self.player1_obj.hp)
        self.ganti_label()

    def set_player2(self,value):
        if self.game_mode.get() == "PvP" and player2_list:
            selected_p2 = next((t for t in player2_list if t.nama == value), None)
            if selected_p2:
                self.player2_obj = selected_p2
                self.opponent_obj = self.player2_obj 
                self.opponent_name = self.player2_obj.nama
                self.opponent_hp = self.player2_obj.hp 
                self.opponent_bar.config(maximum=self.player2_obj.hp)
        self.ganti_label()

    def set_boss(self, value):
        # Dipanggil ketika pilihan Boss berubah di OptionMenu
        if self.game_mode.get() == "PvB" and boss_list:
            selected_boss = next((b for b in boss_list if b.nama == value), None)
            if selected_boss:
                self.boss_obj = selected_boss
                self.opponent_obj = self.boss_obj
                self.opponent_name = self.boss_obj.nama
                self.opponent_hp = self.boss_obj.hp # Reset HP Boss saat dipilih
                self.opponent_bar.config(maximum=self.boss_obj.hp)
        self.ganti_label()

    def ganti_label(self):
        # Update Label Player 1
        if self.player1_obj:
            self.label_player1.config(text=f"{self.player1_obj.nama} HP: {self.player1_hp}/{self.player1_obj.hp}")
            self.player1_bar["value"] = self.player1_hp
            if self.player1_bar['maximum'] != self.player1_obj.hp: # Pastikan max bar sesuai
                 self.player1_bar.config(maximum=self.player1_obj.hp)
        else:
            self.label_player1.config(text="Player 1 HP: -/-")
            self.player1_bar["value"] = 0

        # Update Label Lawan
        if self.opponent_obj:
            max_hp_opponent = self.opponent_obj.hp
            display_name = self.opponent_name
            if self.game_mode.get() == "PvB":
                display_name += " (Boss)"
            
            self.label_opponent.config(text=f"{display_name} HP: {self.opponent_hp}/{max_hp_opponent}")
            self.opponent_bar["value"] = self.opponent_hp
            if self.opponent_bar['maximum'] != max_hp_opponent: # Pastikan max bar sesuai
                 self.opponent_bar.config(maximum=max_hp_opponent)
        else:
            self.label_opponent.config(text="Lawan HP: -/-")
            self.opponent_bar["value"] = 0
    
root = tk.Tk()
app = BattleApp(root)
root.mainloop()
