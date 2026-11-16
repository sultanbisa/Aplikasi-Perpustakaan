
from database import koneksi


# 1. Fungsi menambahkan anggota
def tambah_anggota():
    print("\n========== TAMBAH ANGGOTA ==========")

    nama = input("Masukkan nama anggota: ").strip()
    alamat = input("Masukkan alamat: ").strip()
    no_hp = input("Masukkan nomor HP: ").strip()

    if not nama or not alamat or not no_hp:
        print("Semua data wajib diisi!")
        return

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO anggota (nama, alamat, no_hp)
        VALUES (?, ?, ?)
    """, (nama, alamat, no_hp))

    conn.commit()
    conn.close()

    print("\nAnggota berhasil didaftarkan!")


# 2. Fungsi menampilkan seluruh anggota
def tampilkan_anggota():
    print("\n========== DAFTAR ANGGOTA ==========")

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM anggota")
    data = cursor.fetchall()

    conn.close()

    if not data:
        print("Belum ada anggota terdaftar.")
        return

    print("-" * 75)
    print(f"{'ID':<8} {'Nama':<25} {'Alamat':<25} {'No HP':<15}")
    print("-" * 75)

    for anggota in data:
        print(
            f"{anggota[0]:<8} "
            f"{anggota[1][:24]:<25} "
            f"{anggota[2][:24]:<25} "
            f"{anggota[3]:<15}"
        )

    print("-" * 75)


# 3. Fungsi mencari anggota
def cari_anggota():
    print("\n========== CARI ANGGOTA ==========")

    keyword = input("Masukkan nama anggota: ").strip()

    if not keyword:
        print("Nama pencarian tidak boleh kosong!")
        return

    conn = koneksi()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM anggota
        WHERE nama LIKE ?
    """, ("%" + keyword + "%",))

    data = cursor.fetchall()

    conn.close()

    if not data:
        print("Anggota tidak ditemukan!")
        return

    print("\nHasil pencarian:")

    for anggota in data:
        print("--------------------------------")
        print("ID      :", anggota[0])
        print("Nama    :", anggota[1])
        print("Alamat  :", anggota[2])
        print("No HP   :", anggota[3])


# 4. Fungsi menghapus anggota
def hapus_anggota():
    print("\n========== HAPUS ANGGOTA ==========")

    try:
        id_anggota = int(input("Masukkan ID anggota: "))

        conn = koneksi()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nama FROM anggota WHERE id = ?",
            (id_anggota,)
        )

        data = cursor.fetchone()

        if data is None:
            print("Anggota tidak ditemukan!")
            conn.close()
            return

        print("Anggota yang akan dihapus:", data[0])

        konfirmasi = input("Yakin ingin menghapus? (y/n): ").lower()

        if konfirmasi == "y":
            try:
                cursor.execute(
                    "DELETE FROM anggota WHERE id = ?",
                    (id_anggota,)
                )

                conn.commit()
                print("Anggota berhasil dihapus!")

            except Exception:
                print("Anggota tidak dapat dihapus karena memiliki riwayat peminjaman.")

        else:
            print("Penghapusan dibatalkan.")

        conn.close()

    except ValueError:
        print("ID harus berupa angka!")


# 5. Menu pengelolaan anggota
def menu_anggota():
    while True:
        print("\n================================")
        print("      MENU PENGELOLAAN ANGGOTA")
        print("================================")
        print("1. Tambah Anggota")
        print("2. Tampilkan Daftar Anggota")
        print("3. Cari Anggota")
        print("4. Hapus Anggota")
        print("0. Kembali")
        print("================================")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_anggota()

        elif pilihan == "2":
            tampilkan_anggota()

        elif pilihan == "3":
            cari_anggota()

        elif pilihan == "4":
            hapus_anggota()

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak tersedia!")
