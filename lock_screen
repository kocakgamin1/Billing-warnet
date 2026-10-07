import mulitprocessing as mp
import tkinter as tk


def jalankan_tampilan_kunci(status_pc):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    root.title("Layar Kunci")
    
    label_status = tk.Label(root, text="Status PC: {}".format(status_pc.value), fg="white", bg="black")
    label_status.pack(pady=20)

    button_unlock = tk.Button(root, text="Buka Kunci", fg="white", bg="red")
    button_unlock.pack(pady=10)

    label_desc = tk.Label(root, text="silahkan hubungi administrator untuk membuka kunci", fg="white", bg="black")
    label_desc.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button

    def cek_status():
        if status_pc.value == 1:
            root.destroy()
        else:
            root.after(1000, cek_status)

    root.after(1000, cek_status)

    root.mainloop()

def tampilan_kunci(status_pc):
    p_tampilan = mp.Process(target=jalankan_tampilan_kunci, args=(status_pc,))
    p_tampilan.start()
    return p_tampilan