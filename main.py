import multiprocessing as mp

from lock_screen import tampilan_kunci
from timer_monitor import monitor
from web_server import buat_app, run_flask

if __name__ == "__main__":
    mp.freeze_support()

    status_pc = mp.Value('i', 0)
    durasi_detik = mp.Value('i', 0)

    tampilan_kunci(status_pc)

    p_timer = mp.Process(target=monitor, args=(status_pc, durasi_detik))
    p_timer.start()

    run_flask(buat_app(status_pc, durasi_detik))