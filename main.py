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

        self.game_mode = tk.StringVar(value="PvP")
        self.player_team_objects = []
        self.player_team_hps = [] # Untuk menyimpan HP aktual setiap anggota tim
        self.current_team_attacker_index = 0 # Indeks pemain tim yang gilirannya menyerang/diserang

        mode_frame = tk.Frame(master, bg="#ADD8E6")
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Pilih Mode:", font=("Helvetica", 10, "bold"), bg="#ADD8E6").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(mode_frame, text="Player vs Player", variable=self.game_mode, value="PvP", command=self.update_ui_for_mode, bg="#ADD8E6", font=("Helvetica", 9)).pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Player vs Boss", variable=self.game_mode, value="PvB", command=self.update_ui_for_mode, bg="#ADD8E6", font=("Helvetica", 9)).pack(side=tk.LEFT)

        # --- Pemilihan Player Utama ("Choose Your Character(s)") ---
        # Untuk PvP, ini adalah player tunggal. Untuk PvB, ini akan disembunyikan dan digantikan pemilihan tim.
        self.player1_selection_frame = tk.Frame(master, bg="#ADD8E6") # Frame baru untuk P1 tunggal
        self.player1_label_widget = tk.Label(self.player1_selection_frame, text="Choose Your Character(s):", foreground="red", bg="#ADD8E6", font=("Helvetica", 10, "bold"))
        self.player1_label_widget.pack()
        self.player1_var = tk.StringVar()
        player1_nama_list_for_dropdown = ["Kosong"] + [s.nama for s in player1_list] # Tambah "Kosong" jika perlu
        self.player1_var.set(player1_nama_list_for_dropdown[1] if len(player1_nama_list_for_dropdown) > 1 else "Kosong") # Default ke pemain pertama jika ada
        self.player1_menu = tk.OptionMenu(self.player1_selection_frame, self.player1_var, *player1_nama_list_for_dropdown, command=self.set_player1)
        self.player1_menu.pack()

        # --- Frame untuk Pemilihan Tim (Mode PvB, hingga 5 pemain) ---
        self.team_selection_frame = tk.Frame(master, bg="#ADD8E6")
        tk.Label(self.team_selection_frame, text="Choose Your Character(s) (Team up to 5):", font=("Helvetica", 10, "bold"), bg="#ADD8E6").pack()
        self.team_member_vars = [tk.StringVar() for _ in range(5)] # Untuk 5 anggota tim
        self.team_member_menus = []
        team_member_options = ["Kosong"] + [s.nama for s in player1_list]
        for i in range(5):
            self.team_member_vars[i].set("Kosong")
            menu = tk.OptionMenu(self.team_selection_frame, self.team_member_vars[i], *team_member_options, command=lambda val, slot=i: self.set_team_member(slot, val))
            tk.Label(self.team_selection_frame, text=f"Team Member {i+1}:", bg="#ADD8E6", font=("Helvetica", 9)).pack()
            menu.pack()
            self.team_member_menus.append(menu)

        # --- Frame untuk Lawan (Player 2 atau Boss) ---
        self.opponent_frame = tk.Frame(master, bg="#ADD8E6")
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

        # --- Inisialisasi Objek Player/Boss Awal ---
        self.player1_obj = None # Untuk PvP atau pemain aktif tim
        self.player2_obj = None
        self.boss_obj = None
        self.opponent_obj = None
        self.opponent_name = ""
        self.player1_hp = 0
        self.opponent_hp = 0

        # --- Progress Bar Player 1 (untuk mode PvP) ---
        self.player1_hp_display_frame_pvp = tk.Frame(master, bg="#ADD8E6") # Frame khusus untuk P1 PvP
        self.label_player1_pvp = tk.Label(self.player1_hp_display_frame_pvp,text="", bg="#ADD8E6", font=("Helvetica", 9))
        self.label_player1_pvp.pack()
        self.player1_bar_pvp = ttk.Progressbar(self.player1_hp_display_frame_pvp, length="250")
        self.player1_bar_pvp.pack()

        # --- Frame dan Widget untuk HP Tim (Mode PvB) ---
        self.team_hp_display_frame = tk.Frame(master, bg="#ADD8E6")
        self.team_member_hp_labels = []
        self.team_member_hp_bars = []
        self.team_member_hp_frames = [] # Untuk manage pack_forget per baris
        for i in range(5):
            member_hp_frame = tk.Frame(self.team_hp_display_frame, bg="#ADD8E6")
            label = tk.Label(member_hp_frame, text="", bg="#ADD8E6", font=("Helvetica", 8), width=30, anchor="w") # Width agar rata
            label.pack(side=tk.LEFT, padx=5)
            bar = ttk.Progressbar(member_hp_frame, length="180")
            bar.pack(side=tk.LEFT, padx=5)
            self.team_member_hp_labels.append(label)
            self.team_member_hp_bars.append(bar)
            self.team_member_hp_frames.append(member_hp_frame)
            # member_hp_frame tidak di-pack di sini, tapi di ganti_label

        # --- Progress Bar Lawan ---
        self.opponent_hp_display_frame = tk.Frame(master, bg="#ADD8E6") # Frame khusus untuk lawan
        self.label_opponent = tk.Label(self.opponent_hp_display_frame,text="", bg="#ADD8E6", font=("Helvetica", 9))
        self.label_opponent.pack()
        self.opponent_bar = ttk.Progressbar(self.opponent_hp_display_frame, length="250")
        self.opponent_bar.pack()

        self.tombol_battle = tk.Button(master, text="Start Battle", command=self.mulai_battle, font=("Helvetica", 10, "bold"))
        self.tombol_battle.pack(pady=15)

        self.update_ui_for_mode() # Panggil untuk setup UI awal
        self.ganti_label() # Panggil untuk inisialisasi label HP


    def update_ui_for_mode(self):
        mode = self.game_mode.get()

        self.player1_selection_frame.pack_forget()
        self.player1_hp_display_frame_pvp.pack_forget()
        self.team_selection_frame.pack_forget()
        self.team_hp_display_frame.pack_forget()
        self.player2_label_widget.pack_forget()
        self.player2_menu.pack_forget()
        self.boss_label_widget.pack_forget()
        self.boss_menu.pack_forget()
        self.opponent_hp_display_frame.pack_forget() # Sembunyikan frame HP lawan juga

        if mode == "PvP":
            self.player1_selection_frame.pack(pady=5)
            self.player1_hp_display_frame_pvp.pack(pady=5)
            self.player2_label_widget.pack()
            self.player2_menu.pack()
            self.opponent_hp_display_frame.pack(pady=5)

            # Inisialisasi Player 1 dan Player 2 untuk PvP
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
            # Reset player_team_objects dan HPs untuk tampilan awal sebelum battle
            self.player_team_objects = []
            self.player_team_hps = []

        self.ganti_label()


    def mulai_battle(self):
        mode = self.game_mode.get()
        self.player_team_objects = []
        self.player_team_hps = []
        self.current_team_attacker_index = 0

        if mode == "PvP":
            if self.player1_var.get() == "Kosong" or not player1_list:
                 messagebox.showerror("Error", "Player utama belum dipilih.")
                 return
            # self.player1_obj sudah di-set oleh set_player1
            if not self.player1_obj: # Double check jika set_player1 gagal
                messagebox.showerror("Error", "Objek Player utama tidak valid.")
                return
            self.player1_hp = self.player1_obj.hp

        elif mode == "PvB":
            for i in range(5): # Hingga 5 anggota tim
                member_name = self.team_member_vars[i].get()
                if member_name != "Kosong":
                    char_template = next((p for p in player1_list if p.nama == member_name), None)
                    if char_template:
                        new_member = player1(char_template.nama, char_template.hp, char_template.pow)
                        self.player_team_objects.append(new_member)
                        self.player_team_hps.append(new_member.hp) # Simpan HP awal

            if not self.player_team_objects:
                messagebox.showerror("Error", "Tidak ada pemain yang dipilih untuk tim dalam mode PvB.")
                return
            # self.player1_obj tidak lagi digunakan secara global untuk pemain di PvB.
            # kita akan pakai self.player_team_objects[self.current_team_attacker_index]

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
                # P1 attacks P2
                self.opponent_hp -= self.player1_obj.pow
                if self.opponent_hp < 0: self.opponent_hp = 0
                self.ganti_label()
                if self.opponent_hp <= 0:
                    messagebox.showinfo("Hasil Battle", f"{self.opponent_name} Dikalahkan Oleh {self.player1_obj.nama}!")
                    battle_over = True

                if not battle_over:
                    # P2 attacks P1
                    self.player1_hp -= self.opponent_obj.pow
                    if self.player1_hp < 0: self.player1_hp = 0
                    self.ganti_label()
                    if self.player1_hp <= 0:
                        messagebox.showinfo("Hasil Battle", f"{self.player1_obj.nama} Dikalahkan Oleh {self.opponent_name}!")
                        battle_over = True
            else: # Salah satu sudah kalah sebelum giliran
                battle_over = True

        elif mode == "PvB":
            if not self.player_team_objects or not self.opponent_obj: # Cek tim dan boss
                messagebox.showerror("Error", "Tim pemain atau Boss tidak valid untuk PvB.")
                self.tombol_battle.config(state="active"); return

            active_player_obj = self.player_team_objects[self.current_team_attacker_index]
            active_player_hp_ref_list = self.player_team_hps # List HP aktual

            # Hanya bertarung jika pemain aktif saat ini masih hidup
            if active_player_hp_ref_list[self.current_team_attacker_index] > 0 and self.opponent_hp > 0:
                # Pemain tim aktif menyerang Boss
                print(f"Tim: {active_player_obj.nama} (HP: {active_player_hp_ref_list[self.current_team_attacker_index]}) menyerang Boss.")
                self.opponent_hp -= active_player_obj.pow
                if self.opponent_hp < 0: self.opponent_hp = 0
                self.ganti_label()

                if self.opponent_hp <= 0:
                    messagebox.showinfo("Hasil Battle", f"Tim Pemain Mengalahkan {self.opponent_name} (Boss)!")
                    battle_over = True

                if not battle_over:
                    # Boss menyerang pemain tim aktif
                    print(f"Boss: {self.opponent_name} menyerang {active_player_obj.nama}.")
                    active_player_hp_ref_list[self.current_team_attacker_index] -= self.opponent_obj.pow
                    if active_player_hp_ref_list[self.current_team_attacker_index] < 0:
                        active_player_hp_ref_list[self.current_team_attacker_index] = 0
                    self.ganti_label()

                    if active_player_hp_ref_list[self.current_team_attacker_index] <= 0:
                        print(f"Tim: {active_player_obj.nama} telah dikalahkan.")
                        # Cek apakah semua anggota tim kalah
                        if all(hp <= 0 for hp in self.player_team_hps):
                            messagebox.showinfo("Hasil Battle", f"Semua Anggota Tim Kalah dari {self.opponent_name} (Boss)!")
                            battle_over = True
            elif self.opponent_hp <=0: # Boss sudah kalah sebelum giliran pemain ini
                 messagebox.showinfo("Hasil Battle", f"Tim Pemain Mengalahkan {self.opponent_name} (Boss)!")
                 battle_over = True
            elif all(hp <= 0 for hp in self.player_team_hps): # Semua tim sudah kalah
                 messagebox.showinfo("Hasil Battle", f"Semua Anggota Tim Kalah dari {self.opponent_name} (Boss)!")
                 battle_over = True


            if not battle_over:
                # Pindah ke penyerang tim berikutnya yang masih hidup
                initial_attacker_index = self.current_team_attacker_index
                while True:
                    self.current_team_attacker_index = (self.current_team_attacker_index + 1) % len(self.player_team_objects)
                    if self.player_team_hps[self.current_team_attacker_index] > 0:
                        break # Ditemukan pemain yang masih hidup
                    if self.current_team_attacker_index == initial_attacker_index:
                        # Kembali ke pemain awal, berarti tidak ada yang hidup lagi (seharusnya sudah ditangani oleh cek all hp <=0)
                        # Ini sebagai fallback jika ada kondisi tak terduga
                        if not all(hp <= 0 for hp in self.player_team_hps): # Jika masih ada yg hidup tapi loop aneh
                             print("Error: Gagal menemukan pemain tim aktif berikutnya.")
                        battle_over = True # Anggap battle selesai jika tak ada yg bisa nyerang
                        break

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
                    self.player1_obj = player1(selected_p1.nama, selected_p1.hp, selected_p1.pow) # Instance baru
                    self.player1_hp = self.player1_obj.hp
        self.ganti_label()

    def set_player2(self,value):
        if self.game_mode.get() == "PvP" and player2_list:
            selected_p2 = next((t for t in player2_list if t.nama == value), None)
            if selected_p2:
                self.player2_obj = player2(selected_p2.nama, selected_p2.hp, selected_p2.pow) # Instance baru
                self.opponent_obj = self.player2_obj
                self.opponent_name = self.player2_obj.nama
                self.opponent_hp = self.player2_obj.hp
        self.ganti_label()

    def set_team_member(self, slot_index, value):
        print(f"Tim slot {slot_index} dipilih: {value}")
        # Tidak ada update state langsung di sini, semua dihandle saat `mulai_battle`
        # Panggil ganti_label untuk refresh UI jika ada perubahan pada tampilan default tim
        if self.game_mode.get() == "PvB":
             self.ganti_label()


    def set_boss(self, value):
        if self.game_mode.get() == "PvB" and boss_list:
            selected_boss = next((b for b in boss_list if b.nama == value), None)
            if selected_boss:
                self.boss_obj = Boss(selected_boss.nama, selected_boss.hp, selected_boss.pow) # Instance baru
                self.opponent_obj = self.boss_obj
                self.opponent_name = self.boss_obj.nama
                self.opponent_hp = self.boss_obj.hp
        self.ganti_label()

    def ganti_label(self):
        mode = self.game_mode.get()

        if mode == "PvP":
            # Update HP Player 1 (PvP)
            p1_name = "Player 1"
            p1_hp = 0
            p1_max_hp = 1
            if self.player1_obj:
                p1_name = self.player1_obj.nama
                p1_hp = self.player1_hp
                p1_max_hp = self.player1_obj.hp
            self.label_player1_pvp.config(text=f"{p1_name} HP: {p1_hp}/{p1_max_hp}")
            self.player1_bar_pvp.config(maximum=p1_max_hp, value=p1_hp)

        elif mode == "PvB":
            # Update HP Tim (PvB)
            if hasattr(self, 'player_team_objects') and self.player_team_objects:
                for i in range(5):
                    if i < len(self.player_team_objects):
                        member = self.player_team_objects[i]
                        member_hp_val = self.player_team_hps[i] if i < len(self.player_team_hps) else 0
                        self.team_member_hp_labels[i].config(text=f"P{i+1} ({member.nama}) HP: {member_hp_val}/{member.hp}")
                        self.team_member_hp_bars[i].config(maximum=member.hp, value=member_hp_val)
                        self.team_member_hp_frames[i].pack(fill=tk.X, pady=1) # Tampilkan frame baris ini
                    else: # Slot tim tidak terpakai
                        self.team_member_hp_frames[i].pack_forget() # Sembunyikan frame baris ini
            else: # Jika belum ada tim (misal saat UI baru di-load)
                 for i in range(5):
                    self.team_member_hp_frames[i].pack_forget()


        # Update Label Lawan (Player 2 atau Boss)
        opp_name = "Lawan"
        opp_hp = 0
        opp_max_hp = 1
        if self.opponent_obj:
            opp_name = self.opponent_obj.nama
            opp_hp = self.opponent_hp
            opp_max_hp = self.opponent_obj.hp
            if mode == "PvB" and self.opponent_obj == self.boss_obj :
                opp_name += " (Boss)"

        self.label_opponent.config(text=f"{opp_name} HP: {opp_hp}/{opp_max_hp}")
        self.opponent_bar.config(maximum=opp_max_hp, value=opp_hp)

root = tk.Tk()
app = BattleApp(root)
root.mainloop()
