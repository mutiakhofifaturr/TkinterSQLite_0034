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
