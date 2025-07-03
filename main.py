from karakter1 import player1, player1_list
from karakter2 import player2, player2_list
from boss import Boss, boss_list
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class BattleApp:
    def __init__(self,master):
        self.master = master
        master.title("Battle one Dimention")
        master.geometry("450x850") # Ukuran window disesuaikan

        master.config(bg="#ADD8E6")

        self.main_title_text = "Selamat Datang Di Game Battle Satu Dimensi Saya"
        self.main_title_label = tk.Label(master, text=self.main_title_text, font=("Helvetica", 12, "bold"), fg="black", bg="#ADD8E6")
        self.main_title_label.pack(pady=10, anchor="w")
        self.scroll_pos = 0
        self.scroll_text()

        subtitle_text = """~ by ~
Nabilah Shafirah
Muhammad Ikhwan Nurfaqih
Ajrul Mustaram
Fathiyah Ramadhani
Nabilla De Estika"""
        self.subtitle_label = tk.Label(master, text=subtitle_text, justify=tk.CENTER, font=("Helvetica", 10, "italic"), fg="black", bg="#ADD8E6")
        self.subtitle_label.pack(pady=(0, 10), anchor="s")

        # Frame utama untuk semua konten kecuali tombol Start Battle
        main_content_frame = tk.Frame(master, bg="#ADD8E6")
        main_content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.game_mode = tk.StringVar(value="PvP")
        self.player_team_objects = []
        self.player_team_hps = []
        self.current_team_attacker_index = 0

        mode_frame = tk.Frame(main_content_frame, bg="#ADD8E6") # Dipack ke main_content_frame
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Pilih Mode:", font=("Helvetica", 10, "bold"), bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="Player vs Player", variable=self.game_mode, value="PvP", command=self.update_ui_for_mode, bg="#ADD8E6", font=("Helvetica", 9)).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Player vs Boss", variable=self.game_mode, value="PvB", command=self.update_ui_for_mode, bg="#ADD8E6", font=("Helvetica", 9)).pack(side=tk.LEFT)

        # --- Pemilihan Player Utama ("Choose Your Character(s)") ---
        self.player1_selection_frame = tk.Frame(main_content_frame, bg="#ADD8E6") # Dipack ke main_content_frame
        self.player1_label_widget = tk.Label(self.player1_selection_frame, text="Choose Your Character(s):", foreground="red", bg="#ADD8E6", font=("Helvetica", 10, "bold"))
        self.player1_label_widget.pack()
        self.player1_var = tk.StringVar()
        player1_nama_list_for_dropdown = ["Kosong"] + [s.nama for s in player1_list]
        self.player1_var.set(player1_nama_list_for_dropdown[1] if len(player1_nama_list_for_dropdown) > 1 else "Kosong")
        self.player1_menu = tk.OptionMenu(self.player1_selection_frame, self.player1_var, *player1_nama_list_for_dropdown, command=self.set_player1)
        self.player1_menu.pack()

        # --- Frame untuk Pemilihan Tim (Mode PvB, hingga 5 pemain) ---
        self.team_selection_frame = tk.Frame(master, bg="#ADD8E6")
        tk.Label(self.team_selection_frame, text="Choose Your Character(s) (Team up to 5):", font=("Helvetica", 10, "bold"), bg="#ADD8E6").pack(pady=(0,5))
        self.team_member_vars = [tk.StringVar() for _ in range(5)]
        self.team_member_menus = []
        team_member_options = ["Kosong"] + [s.nama for s in player1_list]
        ts_row_frames = []
        for _ in range(3):
            row_frame = tk.Frame(self.team_selection_frame, bg="#ADD8E6")
            row_frame.pack(fill=tk.X, pady=2)
            ts_row_frames.append(row_frame)
        for i in range(5):
            self.team_member_vars[i].set("Kosong")
            item_frame = tk.Frame(ts_row_frames[i // 2], bg="#ADD8E6")
            label = tk.Label(item_frame, text=f"M{i+1}:", bg="#ADD8E6", font=("Helvetica", 9))
            label.pack(side=tk.LEFT, padx=(0,2))
            menu = tk.OptionMenu(item_frame, self.team_member_vars[i], *team_member_options, command=lambda val, slot=i: self.set_team_member(slot, val))
            menu.config(width=8)
            menu.pack(side=tk.LEFT)
            self.team_member_menus.append(menu)
            item_frame.pack(side=tk.LEFT, padx=10, pady=2)

        # --- Frame untuk Lawan (Player 2 atau Boss) ---
        self.opponent_frame = tk.Frame(main_content_frame, bg="#ADD8E6") # Dipack ke main_content_frame
        self.opponent_frame.pack(pady=5)
        self.player2_label_widget = tk.Label(self.opponent_frame, text="Choose Your Enemy:", foreground="blue", bg="#ADD8E6", font=("Helvetica", 10, "bold"))
        self.player2_var = tk.StringVar()
        player2_nama = [t.nama for t in player2_list]
        if player2_nama: self.player2_var.set(player2_nama[0])
        self.player2_menu = tk.OptionMenu(self.opponent_frame, self.player2_var, *player2_nama, command=self.set_player2)
        self.boss_label_widget = tk.Label(self.opponent_frame, text="Choose Enemy Boss:", foreground="purple", bg="#ADD8E6", font=("Helvetica", 10, "bold"))
        self.boss_var = tk.StringVar()
        boss_nama_list = [b.nama for b in boss_list]
        if boss_nama_list: self.boss_var.set(boss_nama_list[0])
        self.boss_menu = tk.OptionMenu(self.opponent_frame, self.boss_var, *boss_nama_list, command=self.set_boss)

        self.player1_obj = None
        self.player2_obj = None
        self.boss_obj = None
        self.opponent_obj = None
        self.opponent_name = ""
        self.player1_hp = 0
        self.opponent_hp = 0

        self.player1_hp_display_frame_pvp = tk.Frame(main_content_frame, bg="#ADD8E6") # Dipack ke main_content_frame
        self.label_player1_pvp = tk.Label(self.player1_hp_display_frame_pvp,text="", bg="#ADD8E6", font=("Helvetica", 9))
        self.label_player1_pvp.pack()
        self.player1_bar_pvp = ttk.Progressbar(self.player1_hp_display_frame_pvp, length="250")
        self.player1_bar_pvp.pack()

        self.team_hp_display_frame = tk.Frame(main_content_frame, bg="#ADD8E6") # Dipack ke main_content_frame
        self.team_member_hp_labels = []
        self.team_member_hp_bars = []
        self.team_member_hp_frames = []
        for i in range(5):
            member_hp_frame = tk.Frame(self.team_hp_display_frame, bg="#ADD8E6")
            # Perubahan di sini untuk tata letak horizontal per baris HP tim
            label = tk.Label(member_hp_frame, text="", bg="#ADD8E6", font=("Helvetica", 8), width=20, anchor="w")
            label.pack(side=tk.LEFT, padx=(5,2))
            bar = ttk.Progressbar(member_hp_frame, length=150)
            bar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,5))
            self.team_member_hp_labels.append(label)
            self.team_member_hp_bars.append(bar)
            self.team_member_hp_frames.append(member_hp_frame)

        self.opponent_hp_display_frame = tk.Frame(main_content_frame, bg="#ADD8E6") # Dipack ke main_content_frame
        self.label_opponent = tk.Label(self.opponent_hp_display_frame,text="", bg="#ADD8E6", font=("Helvetica", 9))
        self.label_opponent.pack()
        self.opponent_bar = ttk.Progressbar(self.opponent_hp_display_frame, length="250")
        self.opponent_bar.pack()

        # Tombol Start Battle di-pack ke master, di luar main_content_frame
        self.tombol_battle = tk.Button(master, text="Start Battle", command=self.mulai_battle, font=("Helvetica", 10, "bold"))
        self.tombol_battle.pack(pady=10, side=tk.BOTTOM) # side=tk.BOTTOM untuk memastikannya di bawah

        self.update_ui_for_mode()
        self.ganti_label()


    def update_ui_for_mode(self):
        mode = self.game_mode.get()

        self.player1_selection_frame.pack_forget()
        self.player1_hp_display_frame_pvp.pack_forget()
        self.team_selection_frame.pack_forget()
        self.team_hp_display_frame.pack_forget()
        for frame in self.team_member_hp_frames: # Pastikan frame individual HP tim juga disembunyikan
            frame.pack_forget()
        self.player2_label_widget.pack_forget()
        self.player2_menu.pack_forget()
        self.boss_label_widget.pack_forget()
        self.boss_menu.pack_forget()
        self.opponent_hp_display_frame.pack_forget()

        if mode == "PvP":
            self.player1_selection_frame.pack(pady=5)
            self.player1_hp_display_frame_pvp.pack(pady=5)
            self.player2_label_widget.pack()
            self.player2_menu.pack()
            self.opponent_hp_display_frame.pack(pady=5)

            if player1_list: self.set_player1(self.player1_var.get())
            else: self.player1_obj = None; self.player1_hp = 0
            if player2_list: self.set_player2(self.player2_var.get())
            else: self.opponent_obj = None; self.opponent_hp = 0; self.opponent_name = "No Enemy"

        elif mode == "PvB":
            self.team_selection_frame.pack(pady=5)
            self.team_hp_display_frame.pack(pady=5)
            self.boss_label_widget.pack()
            self.boss_menu.pack()
            self.opponent_hp_display_frame.pack(pady=5)

            if boss_list: self.set_boss(self.boss_var.get())
            else: self.opponent_obj = None; self.opponent_hp = 0; self.opponent_name = "No Boss"
            self.player_team_objects = []
            self.player_team_hps = []

        self.ganti_label()


    def mulai_battle(self):
        mode = self.game_mode.get()
        self.player_team_objects = []
        self.player_team_hps = []
        self.current_team_attacker_index = 0

        if mode == "PvP":
            if self.player1_var.get() == "Kosong" or not player1_list: # Cek jika "Kosong" dipilih
                 messagebox.showerror("Error", "Player utama belum dipilih.")
                 return
            if not self.player1_obj:
                # Jika player1_obj masih None, coba set lagi berdasarkan var
                self.set_player1(self.player1_var.get())
                if not self.player1_obj: # Jika masih None setelah coba set
                     messagebox.showerror("Error", "Objek Player utama tidak valid.")
                     return
            self.player1_hp = self.player1_obj.hp

        elif mode == "PvB":
            for i in range(5):
                member_name = self.team_member_vars[i].get()
                if member_name != "Kosong":
                    char_template = next((p for p in player1_list if p.nama == member_name), None)
                    if char_template:
                        new_member = player1(char_template.nama, char_template.hp, char_template.pow)
                        self.player_team_objects.append(new_member)
                        self.player_team_hps.append(new_member.hp)

            if not self.player_team_objects:
                messagebox.showerror("Error", "Tidak ada pemain yang dipilih untuk tim dalam mode PvB.")
                return

        if not self.opponent_obj:
            messagebox.showerror("Error", "Lawan (Enemy atau Boss) tidak dipilih.")
            return
        self.opponent_hp = self.opponent_obj.hp

        self.tombol_battle.config(state="disabled")
        self.round = 1
        self.ganti_label()
        self.master.after(1000, self.auto_battle)


    def auto_battle(self):
        mode = self.game_mode.get()
        battle_over = False

        if mode == "PvP":
            if not self.player1_obj or not self.opponent_obj:
                messagebox.showerror("Error", "Objek pemain atau lawan PvP tidak valid.")
                self.tombol_battle.config(state="active"); return

            if self.player1_hp > 0 and self.opponent_hp > 0:
                self.opponent_hp -= self.player1_obj.pow
                if self.opponent_hp < 0: self.opponent_hp = 0
                self.ganti_label()
                if self.opponent_hp <= 0:
                    messagebox.showinfo("Hasil Battle", f"{self.opponent_name} Dikalahkan Oleh {self.player1_obj.nama}!")
                    battle_over = True

                if not battle_over:
                    self.player1_hp -= self.opponent_obj.pow
                    if self.player1_hp < 0: self.player1_hp = 0
                    self.ganti_label()
                    if self.player1_hp <= 0:
                        messagebox.showinfo("Hasil Battle", f"{self.player1_obj.nama} Dikalahkan Oleh {self.opponent_name}!")
                        battle_over = True
            else:
                battle_over = True

        elif mode == "PvB":
            if not self.player_team_objects or not self.opponent_obj:
                messagebox.showerror("Error", "Tim pemain atau Boss tidak valid untuk PvB.")
                self.tombol_battle.config(state="active"); return

            active_player_obj = self.player_team_objects[self.current_team_attacker_index]

            if self.player_team_hps[self.current_team_attacker_index] > 0 and self.opponent_hp > 0:
                print(f"Tim: {active_player_obj.nama} (HP: {self.player_team_hps[self.current_team_attacker_index]}) menyerang Boss.")
                self.opponent_hp -= active_player_obj.pow
                if self.opponent_hp < 0: self.opponent_hp = 0
                self.ganti_label()

                if self.opponent_hp <= 0:
                    messagebox.showinfo("Hasil Battle", f"Tim Pemain Mengalahkan {self.opponent_name} (Boss)!")
                    battle_over = True

                if not battle_over:
                    print(f"Boss: {self.opponent_name} menyerang {active_player_obj.nama}.")
                    self.player_team_hps[self.current_team_attacker_index] -= self.opponent_obj.pow
                    if self.player_team_hps[self.current_team_attacker_index] < 0:
                        self.player_team_hps[self.current_team_attacker_index] = 0
                    self.ganti_label()

                    if self.player_team_hps[self.current_team_attacker_index] <= 0:
                        print(f"Tim: {active_player_obj.nama} telah dikalahkan.")
                        if all(hp <= 0 for hp in self.player_team_hps):
                            messagebox.showinfo("Hasil Battle", f"Semua Anggota Tim Kalah dari {self.opponent_name} (Boss)!")
                            battle_over = True
            elif self.opponent_hp <=0:
                 messagebox.showinfo("Hasil Battle", f"Tim Pemain Mengalahkan {self.opponent_name} (Boss)!")
                 battle_over = True
            elif all(hp <= 0 for hp in self.player_team_hps):
                 messagebox.showinfo("Hasil Battle", f"Semua Anggota Tim Kalah dari {self.opponent_name} (Boss)!")
                 battle_over = True

            if not battle_over:
                initial_attacker_index = self.current_team_attacker_index
                moved_to_next = False
                for _ in range(len(self.player_team_objects)): # Loop paling banyak sejumlah anggota tim
                    self.current_team_attacker_index = (self.current_team_attacker_index + 1) % len(self.player_team_objects)
                    if self.player_team_hps[self.current_team_attacker_index] > 0:
                        moved_to_next = True
                        break

                if not moved_to_next and not all(hp <= 0 for hp in self.player_team_hps) : # Jika loop tidak menemukan yg hidup, tapi tidak semua kalah (aneh)
                    print("Error logic: Tidak ada pemain hidup ditemukan untuk giliran berikutnya, tapi tidak semua kalah.")
                    # Coba cari manual lagi, mungkin ada yang terlewat
                    found_living = False
                    for idx, hp_val in enumerate(self.player_team_hps):
                        if hp_val > 0:
                            self.current_team_attacker_index = idx
                            found_living = True
                            break
                    if not found_living: # Benar-benar tidak ada yang hidup
                         battle_over = True # Seharusnya sudah ditangani oleh cek all(hp <=0)

        if battle_over:
            self.tombol_battle.config(state="active")
        else:
            self.round += 1
            self.master.after(1000, self.auto_battle)

    def scroll_text(self):
        padded_text = self.main_title_text + "        "
        self.scroll_pos = (self.scroll_pos + 1) % len(padded_text)
        displayed_text = padded_text[self.scroll_pos:] + padded_text[:self.scroll_pos]
        self.main_title_label.config(text=displayed_text)
        self.master.after(150, self.scroll_text)

    def set_player1(self,value):
        if self.game_mode.get() == "PvP":
            if value == "Kosong":
                self.player1_obj = None
                self.player1_hp = 0
            else:
                selected_p1 = next((s for s in player1_list if s.nama == value), None)
                if selected_p1:
                    self.player1_obj = player1(selected_p1.nama, selected_p1.hp, selected_p1.pow)
                    self.player1_hp = self.player1_obj.hp
        self.ganti_label()

    def set_player2(self,value):
        if self.game_mode.get() == "PvP" and player2_list:
            selected_p2 = next((t for t in player2_list if t.nama == value), None)
            if selected_p2:
                self.player2_obj = player2(selected_p2.nama, selected_p2.hp, selected_p2.pow)
                self.opponent_obj = self.player2_obj
                self.opponent_name = self.player2_obj.nama
                self.opponent_hp = self.player2_obj.hp
        self.ganti_label()

    def set_team_member(self, slot_index, value):
        print(f"Tim slot {slot_index} dipilih: {value}")
        if self.game_mode.get() == "PvB":
             self.ganti_label()

    def set_boss(self, value):
        if self.game_mode.get() == "PvB" and boss_list:
            selected_boss = next((b for b in boss_list if b.nama == value), None)
            if selected_boss:
                self.boss_obj = Boss(selected_boss.nama, selected_boss.hp, selected_boss.pow)
                self.opponent_obj = self.boss_obj
                self.opponent_name = self.boss_obj.nama
                self.opponent_hp = self.boss_obj.hp
        self.ganti_label()

    def ganti_label(self):
        mode = self.game_mode.get()

        if mode == "PvP":
            p1_name = "Player 1"
            p1_hp = 0
            p1_max_hp = 1
            if self.player1_obj:
                p1_name = self.player1_obj.nama
                p1_hp = self.player1_hp if hasattr(self, 'player1_hp') else self.player1_obj.hp
                p1_max_hp = self.player1_obj.hp
            self.label_player1_pvp.config(text=f"{p1_name} HP: {p1_hp}/{p1_max_hp}")
            self.player1_bar_pvp.config(maximum=p1_max_hp, value=p1_hp)

        elif mode == "PvB":
            if hasattr(self, 'player_team_objects') and self.player_team_objects and hasattr(self, 'player_team_hps') and len(self.player_team_objects) == len(self.player_team_hps):
                for i in range(5):
                    if i < len(self.player_team_objects):
                        member = self.player_team_objects[i]
                        member_hp_val = self.player_team_hps[i]
                        self.team_member_hp_labels[i].config(text=f"P{i+1} ({member.nama}) HP: {member_hp_val}/{member.hp}")
                        self.team_member_hp_bars[i].config(maximum=member.hp, value=member_hp_val)
                        self.team_member_hp_frames[i].pack(fill=tk.X, pady=1)
                    else:
                        self.team_member_hp_frames[i].pack_forget()
            else:
                 for i in range(5):
                    self.team_member_hp_frames[i].pack_forget()
                    # Default text jika tidak ada tim, untuk konsistensi sebelum battle
                    self.team_member_hp_labels[i].config(text=f"Pemain Tim {i+1} HP: -/-")
                    self.team_member_hp_bars[i].config(maximum=1, value=0)


        opp_name = "Lawan"
        opp_hp = 0
        opp_max_hp = 1
        if self.opponent_obj:
            opp_name = self.opponent_obj.nama
            opp_hp = self.opponent_hp if hasattr(self, 'opponent_hp') else self.opponent_obj.hp
            opp_max_hp = self.opponent_obj.hp
            if mode == "PvB" and self.opponent_obj == self.boss_obj :
                opp_name += " (Boss)"

        self.label_opponent.config(text=f"{opp_name} HP: {opp_hp}/{opp_max_hp}")
        self.opponent_bar.config(maximum=opp_max_hp, value=opp_hp)

root = tk.Tk()
app = BattleApp(root)
root.mainloop()
