import secrets
import time
from pathlib import Path

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

from core import storage
from core.billing import format_durasi, format_rupiah, hitung_biaya

MAX_MENIT = 24 * 60
SECRET_PATH = storage.DATA_DIR / "secret.key"


def _secret_key():
    if not SECRET_PATH.exists():
        SECRET_PATH.parent.mkdir(exist_ok=True)
        SECRET_PATH.write_text(secrets.token_hex(32))
    return SECRET_PATH.read_text().strip()


def _peringatan(pesan):
    aman = str(pesan).replace('"', "'")
    return '<script>alert("{}"); window.location.href="/";</script>'.format(aman)


def hitung_sisa(status_pc, deadline):
    if status_pc.value != 1:
        return 0
    return max(0, int(deadline.value - time.time()))


def buat_app(status_pc, deadline, sesi_id):
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).parent / "templates"),
    )
    app.secret_key = _secret_key()

    @app.template_filter("rupiah")
    def filter_rupiah(nilai):
        return format_rupiah(nilai or 0)

    @app.template_filter("durasi")
    def filter_durasi(detik):
        return format_durasi(detik)

    @app.template_filter("waktu")
    def filter_waktu(ts):
        return time.strftime("%H:%M", time.localtime(ts))

    @app.before_request
    def wajib_login():
        if request.endpoint in (None, "login"):
            return None
        if not session.get("login"):
            return redirect(url_for("login"))
        return None

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            token = storage.load_config()["operator_token"]
            if secrets.compare_digest(request.form.get("token", ""), token):
                session["login"] = True
                return redirect("/")
            error = "Token salah."
        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/")
    def home():
        config = storage.load_config()
        paket = [
            {**p, "harga": hitung_biaya(p["menit"], config["tarif_per_jam"])}
            for p in config.get("paket", [])
        ]
        sesi = storage.sesi_aktif() if status_pc.value == 1 else None
        return render_template(
            "index.html",
            config=config,
            paket=paket,
            status=status_pc.value,
            sesi=sesi,
            sisa=hitung_sisa(status_pc, deadline),
            riwayat=storage.riwayat(),
            pendapatan=storage.pendapatan_hari_ini(),
        )

    @app.route("/mulai", methods=["POST"])
    def mulai():
        if status_pc.value == 1:
            return _peringatan("PC sedang aktif.")
        menit = request.form.get("menit", type=int)
        if menit is None or menit <= 0 or menit > MAX_MENIT:
            return _peringatan("Durasi tidak valid. Isi 1-{} menit.".format(MAX_MENIT))
        config = storage.load_config()
        biaya = hitung_biaya(menit, config["tarif_per_jam"])
        sesi_id.value = storage.buka_sesi(menit, biaya)
        deadline.value = time.time() + menit * 60
        status_pc.value = 1
        return redirect("/")

    @app.route("/stop", methods=["POST"])
    def stop():
        if status_pc.value == 1:
            storage.tutup_sesi(sesi_id.value, "dihentikan operator")
            status_pc.value = 0
            deadline.value = 0
            sesi_id.value = 0
        return redirect("/")

    @app.route("/api/status")
    def api_status():
        aktif = status_pc.value == 1
        sisa = hitung_sisa(status_pc, deadline)
        menit_beli = biaya = None
        if aktif and sesi_id.value:
            baris = storage.sesi_by_id(sesi_id.value)
            if baris:
                menit_beli, biaya = baris["menit_beli"], baris["biaya"]
        return jsonify(
            aktif=aktif,
            sisa_detik=sisa,
            sisa_teks=format_durasi(sisa),
            menit_beli=menit_beli,
            biaya=biaya,
        )

    return app


def run_flask(app, config):
    server = config["server"]
    app.run(host=server["host"], port=server["port"], debug=False, use_reloader=False)
