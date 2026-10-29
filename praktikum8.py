import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prediksi_diabetes.db")


def buat_database():
    """Membuat database dan tabel pasien jika belum ada."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pasien (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien    TEXT    NOT NULL,
            usia           INTEGER NOT NULL,
            gula_darah     REAL    NOT NULL,
            bmi            REAL    NOT NULL,
            riwayat_ortu   TEXT    NOT NULL,
            hasil_prediksi TEXT    NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def simpan_pasien(nama, usia, gula, bmi, riwayat, hasil):
    """Menyimpan satu data pasien ke database."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO pasien (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (nama, usia, gula, bmi, riwayat, hasil),
    )
    conn.commit()
    conn.close()


def ambil_semua_pasien():
    """Mengambil seluruh data pasien dari database."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi FROM pasien")
    data = cur.fetchall()
    conn.close()
    return data

def prediksi_risiko(gula, bmi, riwayat):
    """
    Aturan prediksi:
    - Gula >= 200            : Tinggi / Sangat Tinggi
    - Gula 140 - 199         : Sedang / Tinggi (tergantung BMI & riwayat ortu)
    - Gula < 140, BMI >= 30  : Waspada / Sedang
    - Gula < 140, BMI < 30, riwayat Ya    : Waspada
    - Gula < 140, BMI < 30, riwayat Tidak : Rendah
    """
    ada_riwayat = riwayat == "Ya"
    obesitas = bmi >= 30
    jumlah_faktor = int(obesitas) + int(ada_riwayat)  # 0, 1, atau 2

    if gula >= 200:
        return "Sangat Tinggi" if jumlah_faktor >= 1 else "Tinggi"

    if 140 <= gula < 200:
        return "Tinggi" if jumlah_faktor >= 1 else "Sedang"

    if obesitas:
        return "Sedang" if ada_riwayat else "Waspada"

    return "Waspada" if ada_riwayat else "Rendah"


WARNA_RISIKO = {
    "Rendah": "#2e7d32",         # hijau
    "Waspada": "#f9a825",        # kuning
    "Sedang": "#ef6c00",         # oranye
    "Tinggi": "#d32f2f",         # merah
    "Sangat Tinggi": "#6a1b1b",  # merah tua
}

class AplikasiDiabetes:
    def __init__(self, root):
        self.root = root
        self.root.title("Prediksi Risiko Diabetes")
        self.root.geometry("460x520")
        self.root.resizable(False, False)

        judul = tk.Label(root, text="PREDIKSI RISIKO DIABETES", font=("Arial", 15, "bold"))
        judul.pack(pady=(15, 5))

        frame = tk.Frame(root, padx=20, pady=10)
        frame.pack(fill="x")

        tk.Label(frame, text="Nama Pasien", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        self.entry_nama = tk.Entry(frame, width=28)
        self.entry_nama.grid(row=0, column=1, pady=6)

        tk.Label(frame, text="Usia (tahun)", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_usia = tk.Entry(frame, width=28)
        self.entry_usia.grid(row=1, column=1, pady=6)

        tk.Label(frame, text="Gula Darah (mg/dL)", anchor="w").grid(row=2, column=0, sticky="w", pady=6)
        self.entry_gula = tk.Entry(frame, width=28)
        self.entry_gula.grid(row=2, column=1, pady=6)

        tk.Label(frame, text="BMI", anchor="w").grid(row=3, column=0, sticky="w", pady=6)
        self.entry_bmi = tk.Entry(frame, width=28)
        self.entry_bmi.grid(row=3, column=1, pady=6)

        tk.Label(frame, text="Riwayat Diabetes Ortu", anchor="w").grid(row=4, column=0, sticky="w", pady=6)
        self.combo_riwayat = ttk.Combobox(frame, values=["Ya", "Tidak"], state="readonly", width=25)
        self.combo_riwayat.grid(row=4, column=1, pady=6)
        self.combo_riwayat.set("Pilih...")

        frame_btn = tk.Frame(root)
        frame_btn.pack(pady=10)

        tk.Button(frame_btn, text="Prediksi & Simpan", width=16, bg="#1976d2", fg="white",
                  command=self.proses_prediksi).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Lihat Data", width=12, bg="#388e3c", fg="white",
                  command=self.lihat_data).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Reset", width=10,
                  command=self.reset_form).grid(row=0, column=2, padx=5)

        tk.Label(root, text="Hasil Prediksi:", font=("Arial", 11)).pack(pady=(15, 3))
        self.label_hasil = tk.Label(root, text="-", font=("Arial", 16, "bold"),
                                    width=22, height=2, bg="#e0e0e0", fg="black")
        self.label_hasil.pack(pady=5)

        self.label_keterangan = tk.Label(root, text="", font=("Arial", 9), fg="gray", wraplength=400)
        self.label_keterangan.pack(pady=5)