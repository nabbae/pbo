class Boss:
    def __init__(self, nama, hp, pow):
        self.nama = nama
        self.hp = hp
        self.pow = pow # Mengganti pow_normal menjadi pow, dan menghapus atribut terkait enrage

# Daftar Boss
# Sesuaikan nilai pow jika perlu, karena sekarang ini adalah nilai serangan konstan
boss_list = [
    Boss("Lord Terkutuk", 25000, 350), # Sebelumnya pow_normal 300, dinaikkan sedikit untuk kompensasi hilangnya enrage
    Boss("Golem Raksasa", 35000, 300), # Sebelumnya pow_normal 250
    Boss("Naga Hitam", 20000, 450)    # Sebelumnya pow_normal 400
]

# Contoh penggunaan (opsional, bisa dihapus atau dikomentari)
if __name__ == '__main__':
    test_boss = boss_list[0]
    print(f"Boss: {test_boss.nama}, HP: {test_boss.hp}, Power: {test_boss.pow}")

    test_boss_2 = boss_list[1]
    print(f"Boss: {test_boss_2.nama}, HP: {test_boss_2.hp}, Power: {test_boss_2.pow}")
