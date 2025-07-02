class Boss:
    def __init__(self, nama, hp, pow_normal, pow_enraged_multiplier=1.5, enrage_threshold=0.5):
        self.nama = nama
        self.hp = hp
        self.pow_normal = pow_normal
        self.pow_enraged_multiplier = pow_enraged_multiplier
        self.enrage_threshold = enrage_threshold  # Persentase HP untuk masuk mode enraged

    def get_current_power(self, current_hp):
        """Mengembalikan kekuatan serangan Boss saat ini berdasarkan HP-nya."""
        if current_hp <= (self.hp * self.enrage_threshold):
            return self.pow_normal * self.pow_enraged_multiplier
        return self.pow_normal

# Daftar Boss
boss_list = [
    Boss("Lord Terkutuk", 25000, 300), # HP besar, power standar, akan meningkat saat enraged
    Boss("Golem Raksasa", 35000, 250, pow_enraged_multiplier=1.3, enrage_threshold=0.4), # HP sangat besar, power sedikit lebih rendah, multiplier enrage lebih kecil
    Boss("Naga Hitam", 20000, 400, pow_enraged_multiplier=2.0, enrage_threshold=0.6) # HP standar boss, power tinggi, multiplier enrage besar
]

# Contoh penggunaan (bisa dihapus atau dikomentari nanti)
if __name__ == '__main__':
    # Membuat instance boss pertama dari list
    test_boss = boss_list[0]
    print(f"Boss: {test_boss.nama}, HP: {test_boss.hp}, Power Normal: {test_boss.pow_normal}")

    # Mensimulasikan HP boss untuk melihat perubahan power
    simulated_hp_normal = test_boss.hp * 0.6
    power_at_normal_hp = test_boss.get_current_power(simulated_hp_normal)
    print(f"Power saat HP {simulated_hp_normal}: {power_at_normal_hp}")

    simulated_hp_enraged = test_boss.hp * (test_boss.enrage_threshold * 0.9) # Sedikit di bawah threshold
    power_at_enraged_hp = test_boss.get_current_power(simulated_hp_enraged)
    print(f"Power saat HP {simulated_hp_enraged} (enraged): {power_at_enraged_hp}")

    simulated_hp_exactly_threshold = test_boss.hp * test_boss.enrage_threshold
    power_at_threshold_hp = test_boss.get_current_power(simulated_hp_exactly_threshold)
    print(f"Power saat HP {simulated_hp_exactly_threshold} (tepat di threshold, enraged): {power_at_threshold_hp}")
