import tkinter as tk


class OverlayManager:
    def __init__(self, root):
        self.root = root
        self.win_stop = None
        self.win_fps = None
        self.lbl_timer = None
        self.lbl_fps = None
        self._drag = (0, 0)

    def tampilkan_fps(self):
        self.win_fps = tk.Toplevel(self.root)
        self.win_fps.overrideredirect(True)
        self.win_fps.attributes("-topmost", True)
        self.win_fps.attributes("-alpha", 0.85)
        self.win_fps.configure(bg="#000000")
        self.win_fps.geometry("110x32+15+15")

        self.lbl_fps = tk.Label(
            self.win_fps, text="FPS: --", font=("Consolas", 11, "bold"),
            bg="#000000", fg="#22c55e"
        )
        self.lbl_fps.pack(expand=True)

    def tampilkan_kontrol(self, on_stop_callback):
        self.win_stop = tk.Toplevel(self.root)
        self.win_stop.overrideredirect(True)
        self.win_stop.attributes("-topmost", True)
        self.win_stop.attributes("-alpha", 0.92)
        self.win_stop.configure(bg="#111318")

        lebar_layar = self.root.winfo_screenwidth()
        w, h = 230, 46
        self.win_stop.geometry(f"{w}x{h}+{lebar_layar - w - 20}+15")

        self.win_stop.bind("<ButtonPress-1>", self._mulai_geser)
        self.win_stop.bind("<B1-Motion>", self._sedang_geser)

        self.lbl_timer = tk.Label(
            self.win_stop, text="● 00:00", font=("Segoe UI", 10, "bold"),
            bg="#111318", fg="#ef4444"
        )
        self.lbl_timer.pack(side="left", padx=(14, 8))

        btn_stop = tk.Button(
            self.win_stop, text="⏹ Stop", font=("Segoe UI", 9, "bold"),
            bg="#ef4444", fg="white", activebackground="#dc2626", relief="flat",
            padx=12, pady=4, cursor="hand2", command=on_stop_callback
        )
        btn_stop.pack(side="right", padx=(5, 12))

    def _mulai_geser(self, event):
        self._drag = (event.x, event.y)

    def _sedang_geser(self, event):
        if self.win_stop:
            x = self.win_stop.winfo_x() + event.x - self._drag[0]
            y = self.win_stop.winfo_y() + event.y - self._drag[1]
            self.win_stop.geometry(f"+{x}+{y}")

    def perbarui_info(self, teks_waktu, nilai_fps=None):
        if self.lbl_timer:
            self.lbl_timer.config(text=teks_waktu)
        if self.lbl_fps and nilai_fps is not None:
            self.lbl_fps.config(text=f"FPS: {nilai_fps:.1f}")

    def tutup_semua(self):
        if self.win_stop:
            self.win_stop.destroy()
            self.win_stop = None
        if self.win_fps:
            self.win_fps.destroy()
            self.win_fps = None
