from flask import Flask, request, render_template_string

from config import HOST, PORT
from lock_screen import tampilan_kunci
from templates import HTML_TEMPLATE, alert_redirect

def buat_app(status_pc, durasi_detik):
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template_string(HTML_TEMPLATE, status_pc=status_pc.value)

    @app.route('/mulai', methods=['POST'])
    def mulai():
        if status_pc.value == 0:
            menit = request.form.get('menit', type=int)
            durasi_detik.value = menit * 60
            status_pc.value = 1
        return render_template_string(alert_redirect, message="pc berhasil di buka")
    def stop():
        if status_pc.value == 1:
            status_pc.value = 0
            durasi_detik.value = 0
            tampilan_kunci(status_pc)
        return render_template_string(alert_redirect, message="pc berhasil di kunci")

    return app

def run_flask(app):
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)