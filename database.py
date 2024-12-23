import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = connection.cursor()

if connection:
    print("Berhasil Terhubung ke DataBase")

cursor.execute('CREATE DATABASE IF NOT EXISTS booktopia')
print('DataBase berhasil dibuat')

cursor.execute('USE booktopia')

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    stock INT NOT NULL
);
""")
print('Tabel books berhasil dibuat')

cursor.execute("""
CREATE TABLE IF NOT EXISTS pegawai (
    pegawai_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    position VARCHAR(255) NOT NULL
);
""")
print('Tabel pegawai berhasil dibuat')

cursor.execute("""
CREATE TABLE IF NOT EXISTS peminjaman (
    peminjaman_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(50),
    nama_customer VARCHAR(255) NOT NULL,
    alamat_customer VARCHAR(255) NOT NULL,
    nama_buku VARCHAR(255) NOT NULL,
    tanggal_pinjam DATETIME NOT NULL,
    tanggal_kembali DATETIME NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);
""")
print('Tabel peminjaman berhasil dibuat')


cursor.close()
connection.close()