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