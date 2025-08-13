**Ringkasan Capstone Project Module 1**
Tujuan: Aplikasi terminal sederhana untuk mengelola data supplier (create, read, update, delete), ekspor ke TXT, dan utilitas edit nomor induk.
Stack:
Bahasa: Python
DB: SQLite via sqlite3 (embedded, file peserta.db)

**Model Data**
Tabel: supplier
nomor_induk TEXT, PK
nama TEXT NOT NULL
umur INTEGER
domisili TEXT
tipe TEXT
status TEXT (Aktif/Idle)

**Fitur Utama**
1. Create Database
Validasi: nomor_induk unik (cek pre-insert), nama wajib, umur numerik, status dinormalisasi (title-case & whitelist).

2. Read Database
Tabel rapi (fixed-width formatting); fallback pesan kosong jika tidak ada data.

3. Update Database (Partial Update)
Edit sebagian kolom: tekan Enter untuk mempertahankan nilai lama.

4. Update Primary Key
Ganti nomor_induk lama → baru, cegah duplikasi (IntegrityError).

5. Delete
Konfirmasi Y/N + preview 1 baris dalam format tabel.

6. Export TXT
Cetak seluruh data ke data_supplier.txt dalam layout tabel yang sama.
