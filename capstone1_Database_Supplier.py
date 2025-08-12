import sqlite3

# Koneksi ke database SQLite
conn = sqlite3.connect("supplier.db")
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS supplier (
    nomor_induk TEXT PRIMARY KEY,
    nama TEXT NOT NULL,
    umur INTEGER,
    domisili TEXT,
    tipe TEXT,
    status TEXT
)
""")
conn.commit()

# Tambah data Supplier dengan konfirmasi akhir
def tambah_supplier():
    # Loop sampai nomor_induk unik
    while True:
        nomor = input("Cek Nomor Induk Supplier: ").strip()
        if not nomor:
            print("Nomor Induk tidak boleh kosong!")
            continue

        # Cek apakah nomor_induk sudah ada
        cursor.execute("SELECT 1 FROM supplier WHERE nomor_induk = ? LIMIT 1", (nomor,))
        if cursor.fetchone():
            print("Nomor Induk sudah terdaftar. Silakan pakai nomor lain!")
            continue
        break  # unik -> lanjut isi data lain

    nama = input("Nama Lengkap: ").strip()
    if not nama:
        print("Nama tidak boleh kosong!")
        return

    # Validasi umur angka
    umur_input = input("Umur: ").strip()
    if not umur_input.isdigit():
        print("❌ Umur harus berupa angka bulat.")
        return
    umur = int(umur_input)

    domisili = input("Domisili: ").strip()
    tipe = input("Tipe Barang (PET/HDPE/PP): ").strip()

    # Normalisasi status
    status = input("Status (Aktif/Idle): ").strip().title()
    if status not in ("Aktif", "Idle"):
        print("❌ Status harus 'Aktif' atau 'Idle'.")
        return

    # Tampilkan preview data
    headers = ["Nomor Induk", "Nama", "Umur", "Domisili", "Tipe", "Status"]
    row_format = "{:<15} {:<20} {:<6} {:<15} {:<20} {:<10}"
    print("\nData yang akan ditambahkan:")
    print(row_format.format(*headers))
    print("-" * 90)
    print(row_format.format(nomor, nama, umur, domisili, tipe, status))

    # Konfirmasi akhir
    konfirmasi = input("\nApakah Anda yakin ingin menambahkan data ini? (Y/N): ").strip().lower()
    if konfirmasi == "y":
        cursor.execute(
            "INSERT INTO supplier (nomor_induk, nama, umur, domisili, tipe, status) VALUES (?, ?, ?, ?, ?, ?)",
            (nomor, nama, umur, domisili, tipe, status)
        )
        conn.commit()
        print("✅ Data supplier berhasil ditambahkan.")
    else:
        print("❌ Penambahan data dibatalkan.")

# Tampilkan data Supplier
def tampilkan_supplier():
    cursor.execute("SELECT * FROM supplier")
    data = cursor.fetchall()

    if not data:
        print("Belum ada data Supplier.")
        return

    headers = ["Nomor Induk", "Nama", "Umur", "domisili", "tipe", "Status"]
    row_format = "{:<15} {:<20} {:<6} {:<15} {:<20} {:<10}"

    print("\n" + row_format.format(*headers))
    print("-" * 90)
    for row in data:
        print(row_format.format(*[str(col) for col in row]))

# Ubah data Supplier
# Ubah data Supplier (hanya kolom yang dipilih)
def ubah_supplier():
    nomor = input("Nomor Induk Supplier yang ingin diubah: ")
    cursor.execute("SELECT * FROM supplier WHERE nomor_induk = ?", (nomor,))
    data = cursor.fetchone()

    if data:
        print("Kosongkan input jika tidak ingin mengubah nilai tertentu.\n")

        nama = input(f"Nama baru [{data[1]}]: ") or data[1]
        try:
            umur_input = input(f"Umur baru [{data[2]}]: ")
            umur = int(umur_input) if umur_input else data[2]
        except ValueError:
            print("Umur tidak valid. Gunakan angka.")
            return

        domisili = input(f"domisili baru [{data[3]}]: ") or data[3]
        tipe = input(f"tipe baru (PET/HDPE/PP) [{data[4]}]: ") or data[4]
        status = input(f"Status baru (aktif/idle) [{data[5]}]: ") or data[5]

        cursor.execute("""
            UPDATE supplier SET nama=?, umur=?, domisili=?, tipe=?, status=?
            WHERE nomor_induk=?""", (nama, umur, domisili, tipe, status, nomor))
        conn.commit()
        print("Data berhasil diubah.")
    else:
        print("Data tidak ditemukan.")


# Ubah nomor induk Supplier
def ubah_nomor_induk():
    nomor_lama = input("Nomor Induk yang ingin diubah: ")
    cursor.execute("SELECT * FROM supplier WHERE nomor_induk = ?", (nomor_lama,))
    if cursor.fetchone():
        nomor_baru = input("Masukkan Nomor Induk baru: ")
        try:
            cursor.execute("UPDATE supplier SET nomor_induk = ? WHERE nomor_induk = ?", (nomor_baru, nomor_lama))
            conn.commit()
            print("Nomor Induk berhasil diubah.")
        except sqlite3.IntegrityError:
            print("Nomor Induk baru sudah digunakan. Gunakan nomor yang unik.")
    else:
        print("Data tidak ditemukan.")

def hapus_supplier():
    nomor = input("Nomor Induk Supplier yang ingin dihapus: ").strip()

    # Cek apakah supplier ada
    cursor.execute("SELECT * FROM supplier WHERE nomor_induk = ?", (nomor,))
    data = cursor.fetchone()
    if not data:
        print("❌ Data supplier tidak ditemukan.")
        return

    # Tampilkan data sebelum hapus
    print("\nData yang akan dihapus:")
    print(f"Nomor Induk : {data[0]}")
    print(f"Nama        : {data[1]}")
    print(f"Umur        : {data[2]}")  
    print(f"Domisili    : {data[3]}")
    print(f"Tipe        : {data[4]}")
    print(f"Status      : {data[5]}")

    # Konfirmasi hapus
    konfirmasi = input("Apakah Anda yakin ingin menghapus data ini? (Y/N): ").strip().lower()
    if konfirmasi == "y":
        cursor.execute("DELETE FROM supplier WHERE nomor_induk = ?", (nomor,))
        conn.commit()
        print("✅ Data berhasil dihapus.")
    else:
        print("❌ Penghapusan dibatalkan.")

# Ekspor ke TXT
def ekspor_ke_txt():
    cursor.execute("SELECT * FROM supplier")
    data = cursor.fetchall()
    if not data:
        print("Tidak ada data untuk diekspor.")
        return

    headers = ["Nomor Induk", "Nama", "Umur", "domisili", "tipe", "Status"]
    row_format = "{:<15} {:<20} {:<6} {:<15} {:<20} {:<10}"
    lines = []

    lines.append(row_format.format(*headers))
    lines.append("-" * 90)
    for row in data:
        lines.append(row_format.format(*[str(col) for col in row]))

    with open("data_supplier.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Data berhasil diekspor ke 'data_supplier.txt'")

# Menu utama
def menu():
    while True:
        print("\n=== MENU Supplier ===")
        print("1. Tambah Supplier")
        print("2. Tampilkan Semua Supplier")
        print("3. Ubah Data Supplier")
        print("4. Hapus Supplier")
        print("5. Ekspor ke TXT")
        print("6. Ubah Nomor Induk Supplier")
        print("7. Keluar")
        pilih = input("Pilih (1-7): ")

        if pilih == "1":
            tambah_supplier()
        elif pilih == "2":
            tampilkan_supplier()
        elif pilih == "3":
            ubah_supplier()
        elif pilih == "4":
            hapus_supplier()
        elif pilih == "5":
            ekspor_ke_txt()
        elif pilih == "6":
            ubah_nomor_induk()
        elif pilih == "7":
            break
        else:
            print("Pilihan tidak valid.")

menu()
conn.close()
