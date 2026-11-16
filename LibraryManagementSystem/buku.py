import sqlite3
from database import koneksi


# 1. Fungsi menambahkan buku
def tambah_buku():
    print("\n========== TAMBAH BUKU ==========")

    judul = input("Masukkan judul buku: ").strip()
    penulis = input("Masukkan nama penulis: ").strip()
    penerbit = input("Masukkan nama penerbit: ").strip()

    if not judul or not penulis or not penerbit:
        print("Semua data wajib diisi!")
        return

    try:
        tahun = int(input("Masukkan tahun terbit: "))
        stok = int(input("Masukkan jumlah stok: "))

        if tahun <= 0 or stok < 0:
            print("Tahun harus positif dan stok tidak boleh negatif!")
            return

        conn = koneksi()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO buku (judul, penulis, penerbit, tahun, stok)
            VALUES (?, ?, ?, ?, ?)
        """, (judul, penulis, penerbit, tahun, stok))

        conn.commit()
        conn.close()

        print("\nBuku berhasil ditambahkan!")

    except ValueError:
        print("Tahun dan stok harus berupa angka!")


# 2. Fungsi menampilkan semua buku
def tampilkan_buku():
    print("\n========== DAFTAR BUKU ==========")

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM buku")
    data = cursor.fetchall()

    conn.close()

    if not data:
        print("Belum ada data buku.")
        return

    print("-" * 95)
    print(f"{'ID':<5} {'Judul':<25} {'Penulis':<20} {'Penerbit':<15} {'Tahun':<10} {'Stok':<5}")
    print("-" * 95)

    for buku in data:
        print(
            f"{buku[0]:<5} "
            f"{buku[1][:24]:<25} "
            f"{buku[2][:19]:<20} "
            f"{buku[3][:14]:<15} "
            f"{buku[4]:<10} "
            f"{buku[5]:<5}"
        )

    print("-" * 95)


# 3. Fungsi mencari buku
def cari_buku():
    print("\n========== CARI BUKU ==========")

    keyword = input("Masukkan judul buku: ").strip()

    if not keyword:
        print("Kata pencarian tidak boleh kosong!")
        return

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM buku
        WHERE judul LIKE ?
    """, ("%" + keyword + "%",))

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("Buku tidak ditemukan!")
        return

    print("\nHasil pencarian:")

    for buku in data:
        print("--------------------------------")
        print("ID       :", buku[0])
        print("Judul    :", buku[1])
        print("Penulis  :", buku[2])
        print("Penerbit :", buku[3])
        print("Tahun    :", buku[4])
        print("Stok     :", buku[5])



# 4. Fungsi menghapus buku
def hapus_buku():
    print("\n========== HAPUS BUKU ==========")

    try:
        id_buku = int(input("Masukkan ID buku: "))

        conn = koneksi()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT judul FROM buku WHERE id = ?",
            (id_buku,)
        )

        data = cursor.fetchone()

        if data is None:
            print("Buku tidak ditemukan!")
            conn.close()
            return

        print("Buku yang akan dihapus:", data[0])

        konfirmasi = input(
            "Yakin ingin menghapus? (y/n): "
        ).lower()

        if konfirmasi == "y":
            try:
                cursor.execute(
                    "DELETE FROM buku WHERE id = ?",
                    (id_buku,)
                )

                conn.commit()
                print("Buku berhasil dihapus!")

            except sqlite3.IntegrityError:
                conn.rollback()
                print(
                    "Buku tidak dapat dihapus karena "
                    "memiliki riwayat transaksi."
                )

        else:
            print("Penghapusan dibatalkan.")

        conn.close()

    except ValueError:
        print("ID harus berupa angka!")


# 5. Menu pengelolaan buku
def menu_buku():
    while True:
        print("\n================================")
        print("       MENU PENGELOLAAN BUKU")
        print("================================")
        print("1. Tambah Buku")
        print("2. Tampilkan Daftar Buku")
        print("3. Cari Buku")
        print("4. Hapus Buku")
        print("0. Kembali")
        print("================================")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_buku()
        elif pilihan == "2":
            tampilkan_buku()
        elif pilihan == "3":
            cari_buku()
        elif pilihan == "4":
            hapus_buku()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak tersedia!")