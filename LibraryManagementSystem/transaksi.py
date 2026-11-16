
from database import koneksi
from datetime import date


# =====================================
# 1. FUNGSI PEMINJAMAN BUKU
# =====================================

def pinjam_buku():
    print("\n========== PEMINJAMAN BUKU ==========")

    try:
        id_buku = int(input("Masukkan ID buku: "))
        id_anggota = int(input("Masukkan ID anggota: "))

        if id_buku <= 0 or id_anggota <= 0:
            print("ID harus lebih besar dari 0!")
            return

        conn = koneksi()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT judul, stok
            FROM buku
            WHERE id = ?
        """, (id_buku,))

        buku = cursor.fetchone()

        if buku is None:
            print("Buku tidak ditemukan!")
            conn.close()
            return

        cursor.execute("""
            SELECT nama
            FROM anggota
            WHERE id = ?
        """, (id_anggota,))

        anggota = cursor.fetchone()

        if anggota is None:
            print("Anggota tidak ditemukan!")
            conn.close()
            return

        if buku[1] <= 0:
            print("Maaf, stok buku sedang habis!")
            conn.close()
            return

        tanggal_pinjam = date.today().isoformat()

        cursor.execute("""
            INSERT INTO peminjaman
            (buku_id, anggota_id, tanggal_pinjam, status)
            VALUES (?, ?, ?, 'Dipinjam')
        """, (id_buku, id_anggota, tanggal_pinjam))

        cursor.execute("""
            UPDATE buku
            SET stok = stok - 1
            WHERE id = ? AND stok > 0
        """, (id_buku,))

        if cursor.rowcount != 1:
            conn.rollback()
            print("Peminjaman gagal!")
            conn.close()
            return

        conn.commit()

        print("\n===================================")
        print("      PEMINJAMAN BERHASIL")
        print("===================================")
        print("Judul Buku     :", buku[0])
        print("Nama Anggota   :", anggota[0])
        print("Tanggal Pinjam :", tanggal_pinjam)
        print("Sisa Stok      :", buku[1] - 1)
        print("Status         : Dipinjam")
        print("===================================")

        conn.close()

    except ValueError:
        print("ID harus berupa angka!")


# =====================================
# 2. FUNGSI PENGEMBALIAN BUKU
# =====================================

def kembalikan_buku():
    print("\n========== PENGEMBALIAN BUKU ==========")

    try:
        id_transaksi = int(input("Masukkan ID transaksi: "))

        if id_transaksi <= 0:
            print("ID transaksi tidak valid!")
            return

        conn = koneksi()
        cursor = conn.cursor()

        # Memeriksa transaksi peminjaman
        cursor.execute("""
            SELECT buku_id, status
            FROM peminjaman
            WHERE id = ?
        """, (id_transaksi,))

        transaksi = cursor.fetchone()

        if transaksi is None:
            print("Transaksi tidak ditemukan!")
            conn.close()
            return

        id_buku = transaksi[0]
        status = transaksi[1]

        # Memeriksa status peminjaman
        if status == "Dikembalikan":
            print("Buku sudah dikembalikan sebelumnya!")
            conn.close()
            return

        # Mengambil tanggal pengembalian
        tanggal_kembali = date.today().isoformat()

        # Memperbarui status transaksi
        cursor.execute("""
            UPDATE peminjaman
            SET tanggal_kembali = ?,
                status = 'Dikembalikan'
            WHERE id = ? AND status = 'Dipinjam'
        """, (tanggal_kembali, id_transaksi))

        if cursor.rowcount != 1:
            conn.rollback()
            print("Pengembalian gagal diproses!")
            conn.close()
            return

        # Menambahkan stok buku
        cursor.execute("""
            UPDATE buku
            SET stok = stok + 1
            WHERE id = ?
        """, (id_buku,))

        if cursor.rowcount != 1:
            conn.rollback()
            print("Data buku tidak ditemukan!")
            conn.close()
            return

        conn.commit()

        print("\n===================================")
        print("      PENGEMBALIAN BERHASIL")
        print("===================================")
        print("ID Transaksi     :", id_transaksi)
        print("Tanggal Kembali  :", tanggal_kembali)
        print("Status           : Dikembalikan")
        print("Stok buku berhasil ditambahkan.")
        print("===================================")

        conn.close()

    except ValueError:
        print("ID transaksi harus berupa angka!")


# =====================================
# 3. FUNGSI RIWAYAT PEMINJAMAN
# =====================================

def riwayat_peminjaman():
    print("\n========== RIWAYAT PEMINJAMAN ==========")

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            peminjaman.id,
            buku.judul,
            anggota.nama,
            peminjaman.tanggal_pinjam,
            peminjaman.tanggal_kembali,
            peminjaman.status
        FROM peminjaman
        JOIN buku ON peminjaman.buku_id = buku.id
        JOIN anggota ON peminjaman.anggota_id = anggota.id
        ORDER BY peminjaman.id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Belum ada riwayat peminjaman.")
        return

    for transaksi in data:
        print("--------------------------------------")
        print("ID Transaksi    :", transaksi[0])
        print("Judul Buku      :", transaksi[1])
        print("Nama Anggota    :", transaksi[2])
        print("Tanggal Pinjam  :", transaksi[3])
        print("Tanggal Kembali :", transaksi[4] or "-")
        print("Status          :", transaksi[5])

    print("--------------------------------------")


# =====================================
# 4. MENU TRANSAKSI
# =====================================

def menu_peminjaman():
    while True:
        print("\n================================")
        print("       MENU TRANSAKSI BUKU")
        print("================================")
        print("1. Pinjam Buku")
        print("2. Kembalikan Buku")
        print("3. Riwayat Peminjaman")
        print("0. Kembali")
        print("================================")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            pinjam_buku()

        elif pilihan == "2":
            kembalikan_buku()

        elif pilihan == "3":
            riwayat_peminjaman()

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak tersedia!")
