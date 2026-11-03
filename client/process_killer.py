import subprocess

from core import storage


def kill_processes():
    for proses in storage.load_config().get("kill_processes", []):
        subprocess.run(["taskkill", "/f", "/im", proses], capture_output=True)
