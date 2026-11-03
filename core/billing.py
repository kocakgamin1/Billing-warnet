import math


def hitung_biaya(menit, tarif_per_jam):
    return int(math.ceil(tarif_per_jam * menit / 60))


def format_rupiah(angka):
    return "Rp{:,.0f}".format(angka).replace(",", ".")


def format_durasi(detik):
    detik = max(0, int(detik))
    jam, sisa = divmod(detik, 3600)
    menit, d = divmod(sisa, 60)
    if jam:
        return "{}:{:02d}:{:02d}".format(jam, menit, d)
    return "{:02d}:{:02d}".format(menit, d)
