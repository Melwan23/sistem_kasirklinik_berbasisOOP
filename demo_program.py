# // Library yang di gunakan 
from abc import ABC, abstractclassmethod

# ABSTRACTION
class LayananKlinik(ABC):
    @abstractclassmethod
    def hitung_tagihan(self):
        pass

    @abstractclassmethod
    def detail_nota(self):
        pass

# ENCAPSULATION dan INHERITANCE (Superclass 'Pasien')
class Pasien(LayananKlinik):
    def __init__(self, id_pasien, nama, biaya_tindakan, biaya_obat):
        self.__id_pasien = id_pasien
        self.__nama = nama
        self.__biaya_tindakan = max(0.0, float(biaya_tindakan))
        self.__biaya_obat = max(0.0, float(biaya_obat))

    # Getter Method
    def get_id_pasien(self):
        return self.__id_pasien

    def get_nama(self):
        return self.__nama

    def get_biaya_tindakan(self):
        return self.__biaya_tindakan

    def get_biaya_obat(self):
        return self.__biaya_obat

    # Setter Method
    def set_biaya_tindakan(self, nominal):
        if nominal >= 0:
            self.__biaya_tindakan = float(nominal)

    def set_biaya_obat(self, nominal):
        if nominal >= 0:
            self.__biaya_obat = float(nominal)

# SUB-CLASS

# INHERITANCE dan POLYMORPHISM (Pasien Umum)
class PasienUmum(Pasien):
    def hitung_tagihan(self):
        return self.get_biaya_tindakan() + self.get_biaya_obat()

    def detail_nota(self):
        print("Kategori    : Pasien Umum (Bayar 100%)")

# INHERITANCE dan POLYMORPHISM (Pasien BPJS)
class PasienBPJS(Pasien):
    def __init__(self, id_pasien, nama, biaya_tindakan, biaya_obat, no_bpjs):
        super().__init__(id_pasien, nama, biaya_tindakan, biaya_obat)
        self.__no_bpjs = no_bpjs

    # Method Overriding: Obat dikover BPJS
    def hitung_tagihan(self):
        return self.get_biaya_tindakan()

    def detail_nota(self):
        print(f"Kategori    : Pasien BPJS (No: {self.__no_bpjs})")
        print(f"Cover Obat  : Rp {self.get_biaya_obat():,.0f} (GRATIS)")

# INHERITANCE dan POLYMORPHISM (Pasien Asuransi)
class PasienAsuransi(Pasien):
    def __init__(self, id_pasien, nama, biaya_tindakan, biaya_obat, no_polis, diskon_persen):
        super().__init__(id_pasien, nama, biaya_tindakan, biaya_obat)
        self.__no_polis = no_polis
        self.__diskon_persen = float(diskon_persen)

    # Method Overriding: Potongan diskon
    def hitung_tagihan(self):
        subtotal = self.get_biaya_tindakan() + self.get_biaya_obat()
        potongan = subtotal * (self.__diskon_persen / 100)
        return subtotal - potongan

    def detail_nota(self):
        print(f"Kategori    : Pasien Asuransi (Polis: {self.__no_polis})")
        print(f"Diskon Polis: {self.__diskon_persen:.0f}%")

# MAIN PROGRAM
if __name__ == "__main__":
    print("=== SISTEM KASIR & TAGIHAN KLINIK ===")
    
    # 1. Input data
    id_pasien = input("Masukkan ID Pasien        : ")
    nama = input("Masukkan Nama Pasien      : ")
    biaya_tindakan = float(input("Biaya Tindakan Medis (Rp): "))
    biaya_obat = float(input("Biaya Obat-obatan (Rp)   : "))

    print("\nPilih Jenis Kepesertaan:")
    print("1. Pasien Umum")
    print("2. Pasien BPJS")
    print("3. Pasien Asuransi")
    pilihan = input("Pilih (1/2/3): ")

    pasien = None

    if pilihan == "1":
        pasien = PasienUmum(id_pasien, nama, biaya_tindakan, biaya_obat)
    
    elif pilihan == "2":
        no_bpjs = input("Masukkan No. Kartu BPJS : ")
        pasien = PasienBPJS(id_pasien, nama, biaya_tindakan, biaya_obat, no_bpjs)
    
    elif pilihan == "3":
        no_polis = input("Masukkan No. Polis      : ")
        diskon = float(input("Masukkan Diskon (%)     : "))
        pasien = PasienAsuransi(id_pasien, nama, biaya_tindakan, biaya_obat, no_polis, diskon)
    
    else:
        print("Pilihan tidak valid!")
        exit()

    # 3. Output Hasil
    print("\n====================================")
    print("       RINCIAN TAGIHAN KLINIK      ")
    print("====================================")
    print(f"ID Pasien   : {pasien.get_id_pasien()}")
    print(f"Nama Pasien : {pasien.get_nama()}")
    pasien.detail_nota()
    print(f"TOTAL BAYAR : Rp {pasien.hitung_tagihan():,.0f}")