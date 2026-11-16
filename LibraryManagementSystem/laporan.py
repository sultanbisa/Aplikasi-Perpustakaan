
from database import koneksi


# Fungsi dashboard statistik
def dashboard():
    conn = koneksi()
    cursor = conn.cursor()

    # Menghitung jumlah koleksi buku
    cursor.execute("SELECT COUNT(*) FROM buku")
    total_buku = cursor.fetchone()[0]

    # Menghitung total stok buku
    cursor.execute("SELECT COALESCE(SUM(stok), 0) FROM buku")
    total_stok = cursor.fetchone()[0]

    # Menghitung jumlah anggota
    cursor.execute("SELECT COUNT(*) FROM anggota")
    total_anggota = cursor.fetchone()[0]

    # Menghitung total transaksi
    cursor.execute("SELECT COUNT(*) FROM peminjaman")
    total_transaksi = cursor.fetchone()[0]

    # Menghitung buku yang masih dipinjam
    cursor.execute("""
        SELECT COUNT(*)
        FROM peminjaman
        WHERE status = 'Dipinjam'
    """)
    sedang_dipinjam = cursor.fetchone()[0]

    # Menghitung buku yang sudah dikembalikan
    cursor.execute("""
        SELECT COUNT(*)
        FROM peminjaman
        WHERE status = 'Dikembalikan'
    """)
    sudah_dikembalikan = cursor.fetchone()[0]

    conn.close()

    print("\n================================================")
    print("             DASHBOARD PERPUSTAKAAN")
    print("================================================")
    print(f"Total Judul Buku          : {total_buku}")
    print(f"Total Stok Buku           : {total_stok}")
    print(f"Total Anggota             : {total_anggota}")
    print(f"Total Transaksi           : {total_transaksi}")
    print(f"Buku Sedang Dipinjam      : {sedang_dipinjam}")
    print(f"Buku Sudah Dikembalikan   : {sudah_dikembalikan}")
    print("================================================")


# Fungsi laporan daftar buku yang sedang dipinjam
def laporan_buku_dipinjam():
    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            peminjaman.id,
            buku.judul,
            anggota.nama,
            peminjaman.tanggal_pinjam
        FROM peminjaman
        JOIN buku ON peminjaman.buku_id = buku.id
        JOIN anggota ON peminjaman.anggota_id = anggota.id
        WHERE peminjaman.status = 'Dipinjam'
        ORDER BY peminjaman.id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    print("\n========== BUKU SEDANG DIPINJAM ==========")

    if not data:
        print("Tidak ada buku yang sedang dipinjam.")
        return

    for item in data:
        print("------------------------------------------")
        print("ID Transaksi   :", item[0])
        print("Judul Buku     :", item[1])
        print("Nama Anggota   :", item[2])
        print("Tanggal Pinjam :", item[3])

    print("------------------------------------------")


# Menu laporan
def menu_laporan():
    while True:
        print("\n================================")
        print("       MENU LAPORAN")
        print("================================")
        print("1. Dashboard Statistik")
        print("2. Daftar Buku Sedang Dipinjam")
        print("0. Kembali")
        print("================================")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            dashboard()

        elif pilihan == "2":
            laporan_buku_dipinjam()

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak tersedia!")
