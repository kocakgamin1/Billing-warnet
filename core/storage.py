import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_PATH = DATA_DIR / "config.json"
CONTOH_CONFIG = DATA_DIR / "config.example.json"
DB_PATH = DATA_DIR / "billing.db"

CONFIG_DEFAULT = {
    "server": {"host": "0.0.0.0", "port": 5000},
    "operator_token": "admin123",
    "tarif_per_jam": 5000,
    "paket": [
        {"nama": "1 Jam", "menit": 60},
        {"nama": "2 Jam", "menit": 120},
        {"nama": "3 Jam", "menit": 180},
    ],
    "kill_processes": ["chrome.exe", "valorant.exe", "steam.exe", "discord.exe"],
}


def init():
    _siapkan_config()
    with koneksi() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sesi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mulai REAL NOT NULL,
                selesai REAL,
                menit_beli INTEGER NOT NULL,
                biaya INTEGER NOT NULL DEFAULT 0,
                alasan_selesai TEXT
            )
            """
        )


def _siapkan_config():
    DATA_DIR.mkdir(exist_ok=True)
    if CONFIG_PATH.exists():
        return
    if CONTOH_CONFIG.exists():
        CONFIG_PATH.write_text(CONTOH_CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        simpan_config(CONFIG_DEFAULT)


def load_config():
    _siapkan_config()
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def simpan_config(config):
    DATA_DIR.mkdir(exist_ok=True)
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8"
    )


@contextmanager
def koneksi():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def buka_sesi(menit, biaya):
    with koneksi() as conn:
        cur = conn.execute(
            "INSERT INTO sesi (mulai, menit_beli, biaya) VALUES (?, ?, ?)",
            (time.time(), menit, biaya),
        )
        return cur.lastrowid


def tutup_sesi(sesi_id, alasan):
    if not sesi_id:
        return
    with koneksi() as conn:
        conn.execute(
            "UPDATE sesi SET selesai = ?, alasan_selesai = ? WHERE id = ? AND selesai IS NULL",
            (time.time(), alasan, sesi_id),
        )


def sesi_by_id(sesi_id):
    with koneksi() as conn:
        return conn.execute("SELECT * FROM sesi WHERE id = ?", (sesi_id,)).fetchone()


def sesi_aktif():
    with koneksi() as conn:
        return conn.execute(
            "SELECT * FROM sesi WHERE selesai IS NULL ORDER BY id DESC LIMIT 1"
        ).fetchone()


def riwayat(limit=8):
    with koneksi() as conn:
        return conn.execute(
            "SELECT * FROM sesi WHERE selesai IS NOT NULL ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()


def pendapatan_hari_ini():
    with koneksi() as conn:
        row = conn.execute(
            """
            SELECT COALESCE(SUM(biaya), 0) AS total FROM sesi
            WHERE selesai IS NOT NULL
              AND date(selesai, 'unixepoch', 'localtime') = date('now', 'localtime')
            """
        ).fetchone()
    return row["total"]
