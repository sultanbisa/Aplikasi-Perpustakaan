
import sqlite3
import os

# Membuat folder database jika belum tersedia
os.makedirs("database", exist_ok=True)

# Membuat koneksi database
def koneksi():
    conn = sqlite3.connect("database/perpustakaan.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Membuat tabel database
def buat_tabel():
    conn = koneksi()
    cursor = conn.cursor()

    # Tabel buku
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            penulis TEXT NOT NULL,
            penerbit TEXT NOT NULL,
            tahun INTEGER NOT NULL,
            stok INTEGER NOT NULL CHECK(stok >= 0)
        )
    """)

    # Tabel anggota
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anggota (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            alamat TEXT NOT NULL,
            no_hp TEXT NOT NULL
        )
    """)

    # Tabel peminjaman
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peminjaman (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            buku_id INTEGER NOT NULL,
            anggota_id INTEGER NOT NULL,
            tanggal_pinjam TEXT NOT NULL,
            tanggal_kembali TEXT,
            status TEXT NOT NULL DEFAULT 'Dipinjam',
            FOREIGN KEY (buku_id) REFERENCES buku(id),
            FOREIGN KEY (anggota_id) REFERENCES anggota(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database berhasil dibuat!")
    print("Tabel buku berhasil dibuat!")
    print("Tabel anggota berhasil dibuat!")
    print("Tabel peminjaman berhasil dibuat!")


# Menjalankan program database
if __name__ == "__main__":
    buat_tabel()
