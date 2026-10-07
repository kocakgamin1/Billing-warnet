import os
import time

from config import list_proses
from lock_screen import tampilan_kunci

def kill_processes():
    for proses in list_proses:
        os.system(f"taskkill /f /im {proses}")

def monitor(status_pc, durasi_detik):
    while True:
        if status_pc.value == 1 and durasi_detik.value > 0:
            time.sleep(1)
            durasi_detik.value -= 1
            if durasi_detik.value <= 0:
                status_pc.value = 0
                kill_processes()
        else:
            time.sleep(1)
      