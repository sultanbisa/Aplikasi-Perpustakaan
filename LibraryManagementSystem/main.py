
from database import buat_tabel
from buku import menu_buku
from anggota import menu_anggota
from transaksi import menu_peminjaman
from laporan import menu_laporan


def menu_utama():
    while True:
        print("\n================================================")
        print("             LIBRARY MANAGEMENT SYSTEM")
        print("================================================")
        print("1. Pengelolaan Data Buku")
        print("2. Pengelolaan Data Anggota")
        print("3. Transaksi Peminjaman dan Pengembalian")
        print("4. Dashboard Statistik dan Laporan")
        print("0. Keluar")
        print("================================================")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            menu_buku()

        elif pilihan == "2":
            menu_anggota()

        elif pilihan == "3":
            menu_peminjaman()

        elif pilihan == "4":
            menu_laporan()

        elif pilihan == "0":
            print("\n========================================")
            print("Terima kasih telah menggunakan aplikasi!")
            print("========================================")
            break

        else:
            print("\nPilihan tidak tersedia!")
            print("Silakan pilih menu yang benar.")


# Program utama
if __name__ == "__main__":
    buat_tabel()
    menu_utama()