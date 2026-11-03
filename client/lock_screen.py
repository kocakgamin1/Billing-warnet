import multiprocessing as mp
import tkinter as tk


def jalankan_tampilan_kunci(status_pc):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    root.title("Layar Kunci")

    frame = tk.Frame(root, bg="black")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame, text="PC TERKUNCI", fg="#00f2fe", bg="black",
        font=("Segoe UI", 42, "bold"),
    ).pack(pady=20)

    tk.Label(
        frame,
        text="Silakan hubungi operator untuk membuka kunci",
        fg="#aaaaaa", bg="black", font=("Segoe UI", 12),
    ).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: None)  # blokir tombol close

    def cek_status():
        if status_pc.value == 0:
            root.deiconify()
            root.attributes("-topmost", True)
            root.lift()
            root.focus_force()
        else:
            root.withdraw()
        root.after(500, cek_status)

    cek_status()
    root.mainloop()


def tampilan_kunci(status_pc):
    p = mp.Process(target=jalankan_tampilan_kunci, args=(status_pc,), daemon=True)
    p.start()
    return p
