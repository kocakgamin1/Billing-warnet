import time

from client.process_killer import kill_processes
from core import storage


def monitor(status_pc, deadline, sesi_id):
    while True:
        if status_pc.value == 1 and time.time() >= deadline.value:
            storage.tutup_sesi(sesi_id.value, "waktu habis")
            status_pc.value = 0
            deadline.value = 0
            sesi_id.value = 0
            kill_processes()
        time.sleep(0.5)
