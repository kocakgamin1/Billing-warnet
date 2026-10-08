HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Z-NET Operator</title>
    <style>
        body { font-family: sans-serif; background: #0f0f1a; color: #fff; text-align: center; padding: 20px; }
        .card { background: #1a1a2e; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,242,254,0.1); border: 1px solid #333; max-width: 400px; margin: auto; }
        input, button { width: 100%; padding: 15px; margin: 12px 0; border-radius: 8px; border: none; font-size: 16px; box-sizing: border-box; }
        input { background: #252542; color: #fff; text-align: center; font-size: 18px; }
        button { background: linear-gradient(45deg, #00f2fe, #4facfe); color: #000; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { opacity: 0.9; }
        .status { font-weight: bold; font-size: 22px; padding: 5px 15px; border-radius: 20px; display: inline-block; margin-bottom: 20px; }
        .terkunci { background: rgba(255,75,75,0.1); color: #ff4b4b; border: 1px solid #ff4b4b; }
        .aktif { background: rgba(0,255,136,0.1); color: #00ff88; border: 1px solid #00ff88; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Z-NET PC CLIENT 1</h2>
        {% if status == 0 %}
            <span class="status terkunci">TERKUNCI</span>
            <form action="/mulai" method="post">
                <input type="number" name="menit" placeholder="Durasi Bermain (Menit)" required min="1">
                <button type="submit">BUKA KUNCI SEKARANG</button>
            </form>
        {% else %}
            <span class="status aktif">AKTIF / BERMAIN</span>
            <form action="/stop" method="post">
                <button type="submit" style="background: linear-gradient(45deg, #ff4b4b, #ff2a2a); color: #fff;">KUNCI PAKSA SEKARANG</button>
            </form>
        {% endif %}
    </div>
</body>
</html>
"""

def alert_redirect(pesan):
    return f'<script>alert("{pesan}"); window.location.href="/";</script>'