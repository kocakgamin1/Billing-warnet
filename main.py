import multiprocessing as mp
import time

from client.lock_screen import tampilan_kunci
from core import storage
from core.monitor import monitor
from server.web_server import buat_app, run_flask


def pulihkan_sesi(status_pc, deadline, sesi_id):
    aktif = storage.sesi_aktif()
    if not aktif:
        return
    berakhir = aktif["mulai"] + aktif["menit_beli"] * 60
    sisa = berakhir - time.time()
    if sisa > 0:
        sesi_id.value = aktif["id"]
        deadline.value = berakhir
        status_pc.value = 1
        print("[pulihkan] sesi #{} lanjut, sisa {} detik".format(aktif["id"], int(sisa)))
    else:
        storage.tutup_sesi(aktif["id"], "waktu habis (aplikasi mati)")
        print("[pulihkan] sesi #{} ditutup, waktu habis saat aplikasi mati".format(aktif["id"]))


def main():
    storage.init()
    config = storage.load_config()

    status_pc = mp.Value("i", 0)
    deadline = mp.Value("d", 0.0)
    sesi_id = mp.Value("i", 0)

    pulihkan_sesi(status_pc, deadline, sesi_id)

    p_lock = tampilan_kunci(status_pc)
    p_timer = mp.Process(target=monitor, args=(status_pc, deadline, sesi_id), daemon=True)
    p_timer.start()

    print("Panel operator: http://localhost:{}".format(config["server"]["port"]))
    try:
        run_flask(buat_app(status_pc, deadline, sesi_id), config)
    finally:
        p_lock.terminate()
        p_timer.terminate()


if __name__ == "__main__":
    mp.freeze_support()
    main()
