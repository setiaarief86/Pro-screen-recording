import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from recorder_engine import ScreenRecorderEngine
from overlays import OverlayManager
from theme_config import PALET_TEMA, RESOLUSI_MAP


def resource_path(relative_path):
    """Mendapatkan path absolut resource (mendukung mode skrip & .exe PyInstaller)"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


class ProScreenStudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProScreen Studio - Screen Recorder")
        self.root.geometry("460x610")
        self.root.resizable(False, False)

        # Memasang ikon pada title bar jendela dan taskbar
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass

        self.engine = ScreenRecorderEngine()
        self.overlays = OverlayManager(root)
        self.waktu_mulai = 0
        self.tema_saat_ini = "dark"

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.bangun_ui()
        self.terapkan_tema()

    def bangun_ui(self):
        self.header = tk.Frame(self.root, height=60)
        self.header.pack(fill="x")

        self.lbl_app_title = tk.Label(self.header, text="🎬  PROSCREEN STUDIO", font=("Segoe UI", 13, "bold"))
        self.lbl_app_title.pack(side="left", padx=20, pady=15)

        self.btn_tema = tk.Button(
            self.header, text="☀️ Light Mode", font=("Segoe UI", 8, "bold"),
            relief="flat", padx=10, pady=4, cursor="hand2", command=self.ganti_tema
        )
        self.btn_tema.pack(side="right", padx=20)

        self.container = tk.Frame(self.root, padx=20, pady=15)
        self.container.pack(fill="both", expand=True)

        # KARTU 1: MODE & DURASI
        self.card_mode, self.lbl_c1 = self.buat_kartu(self.container, "⏱️  MODE & DURASI PEREKAMAN")
        self.mode_var = tk.StringVar(value="unlimited")

        self.rb_unlim = tk.Radiobutton(
            self.card_mode, text="Rekam Tanpa Batas (Stop lewat tombol overlay)", variable=self.mode_var,
            value="unlimited", font=("Segoe UI", 9), command=self.toggle_durasi
        )
        self.rb_unlim.pack(anchor="w", pady=(2, 4))

        self.rb_timer = tk.Radiobutton(
            self.card_mode, text="Rekam Otomatis (Berhenti otomatis sesuai timer)", variable=self.mode_var,
            value="timer", font=("Segoe UI", 9), command=self.toggle_durasi
        )
        self.rb_timer.pack(anchor="w", pady=(0, 6))

        self.frame_timer = tk.Frame(self.card_mode)
        self.frame_timer.pack(anchor="w", padx=22, pady=(0, 4))

        self.jam_var, self.menit_var, self.detik_var = tk.StringVar(value="0"), tk.StringVar(value="5"), tk.StringVar(value="0")
        self.timer_labels, self.timer_spinboxes = [], []

        for lbl, var, maks in [("Jam:", self.jam_var, 23), ("Menit:", self.menit_var, 59), ("Detik:", self.detik_var, 59)]:
            l = tk.Label(self.frame_timer, text=lbl, font=("Segoe UI", 8))
            l.pack(side="left", padx=(0, 3))
            self.timer_labels.append(l)

            sb = tk.Spinbox(self.frame_timer, from_=0, to=maks, textvariable=var, width=4, relief="flat", font=("Segoe UI", 9))
            sb.pack(side="left", padx=(0, 10))
            self.timer_spinboxes.append(sb)
        self.toggle_durasi()

        # KARTU 2: RESOLUSI, FPS & KURSOR
        self.card_video, self.lbl_c2 = self.buat_kartu(self.container, "🖥️  KUALITAS VIDEO & RESOLUSI")
        self.row_res = tk.Frame(self.card_video)
        self.row_res.pack(fill="x", pady=4)
        self.lbl_res = tk.Label(self.row_res, text="Resolusi Output:", font=("Segoe UI", 9))
        self.lbl_res.pack(side="left")

        self.res_combo = ttk.Combobox(self.row_res, values=list(RESOLUSI_MAP.keys()), state="readonly", width=26, font=("Segoe UI", 9))
        self.res_combo.set("1080p Full HD (1920 x 1080)")
        self.res_combo.pack(side="right")

        self.row_fps = tk.Frame(self.card_video)
        self.row_fps.pack(fill="x", pady=4)
        self.lbl_fps = tk.Label(self.row_fps, text="Target Frame Rate:", font=("Segoe UI", 9))
        self.lbl_fps.pack(side="left")
        self.fps_combo = ttk.Combobox(self.row_fps, values=["30 FPS (Standar)", "24 FPS (Sinematik)", "60 FPS (Tinggi)"], state="readonly", width=26, font=("Segoe UI", 9))
        self.fps_combo.set("30 FPS (Standar)")
        self.fps_combo.pack(side="right")

        # DROPDOWN KURSOR MOUSE
        self.row_cursor = tk.Frame(self.card_video)
        self.row_cursor.pack(fill="x", pady=4)
        self.lbl_cursor = tk.Label(self.row_cursor, text="Kursor Mouse:", font=("Segoe UI", 9))
        self.lbl_cursor.pack(side="left")
        self.cursor_combo = ttk.Combobox(
            self.row_cursor,
            values=["Tampilkan Kursor Mouse", "Sembunyikan Kursor Mouse"],
            state="readonly", width=26, font=("Segoe UI", 9)
        )
        self.cursor_combo.set("Tampilkan Kursor Mouse")
        self.cursor_combo.pack(side="right")
        # KARTU 3: AUDIO
        self.card_audio, self.lbl_c3 = self.buat_kartu(self.container, "🎙️  SUMBER AUDIO")
        self.row_aud = tk.Frame(self.card_audio)
        self.row_aud.pack(fill="x", pady=4)
        self.lbl_aud = tk.Label(self.row_aud, text="Rekam Suara:", font=("Segoe UI", 9))
        self.lbl_aud.pack(side="left")

        self.audio_combo = ttk.Combobox(
            self.row_aud,
            values=["Suara Desktop / Aplikasi (System Audio)", "Mikrofon Saja", "Mikrofon + Suara Desktop", "Tanpa Suara (Mute)"],
            state="readonly", width=30, font=("Segoe UI", 9)
        )
        self.audio_combo.set("Suara Desktop / Aplikasi (System Audio)")
        self.audio_combo.pack(side="right")

        # KARTU 4: INDIKATOR FPS OVERLAY
        self.card_overlay, self.lbl_c4 = self.buat_kartu(self.container, "📊  INDIKATOR LAYAR")
        self.show_fps_var = tk.BooleanVar(value=True)
        self.chk_fps = tk.Checkbutton(
            self.card_overlay, text="Tampilkan penghitung FPS live di pojok kiri atas layar",
            variable=self.show_fps_var, font=("Segoe UI", 9)
        )
        self.chk_fps.pack(anchor="w", pady=2)

        # TOMBOL MULAI & STATUS
        self.btn_start = tk.Button(
            self.container, text="⏺   MULAI PEREKAMAN", font=("Segoe UI", 11, "bold"),
            bg="#ef4444", fg="white", activebackground="#dc2626", activeforeground="white",
            relief="flat", pady=12, cursor="hand2", command=self.mulai_rekam
        )
        self.btn_start.pack(fill="x", pady=(10, 6))

        self.lbl_status = tk.Label(self.container, text="Status: Siap merekam", font=("Segoe UI", 9))
        self.lbl_status.pack()

    def buat_kartu(self, parent, judul):
        frame = tk.Frame(parent, padx=14, pady=10, highlightthickness=1)
        frame.pack(fill="x", pady=(0, 10))
        lbl = tk.Label(frame, text=judul, font=("Segoe UI", 8, "bold"))
        lbl.pack(anchor="w", pady=(0, 6))
        return frame, lbl

    def ganti_tema(self):
        self.tema_saat_ini = "light" if self.tema_saat_ini == "dark" else "dark"
        self.terapkan_tema()

    def terapkan_tema(self):
        c = PALET_TEMA[self.tema_saat_ini]
        teks_btn = "☀️ Light Mode" if self.tema_saat_ini == "dark" else "🌙 Dark Mode"
        self.btn_tema.config(text=teks_btn, bg=c["badge_bg"], fg=c["badge_fg"], activebackground=c["border_card"])

        self.root.configure(bg=c["bg_main"])
        self.container.configure(bg=c["bg_main"])
        self.header.configure(bg=c["bg_card"])
        self.lbl_app_title.configure(bg=c["bg_card"], fg=c["fg_title"])

        for card, lbl in [(self.card_mode, self.lbl_c1), (self.card_video, self.lbl_c2), (self.card_audio, self.lbl_c3), (self.card_overlay, self.lbl_c4)]:
            card.configure(bg=c["bg_card"], highlightbackground=c["border_card"])
            lbl.configure(bg=c["bg_card"], fg=c["fg_card_title"])

        for w in [self.rb_unlim, self.rb_timer, self.chk_fps]:
            w.configure(bg=c["bg_card"], fg=c["fg_text"], selectcolor=c["bg_input"], activebackground=c["bg_card"], activeforeground=c["fg_text"])

        for f in [self.frame_timer, self.row_res, self.row_fps, self.row_cursor, self.row_aud]:
            f.configure(bg=c["bg_card"])

        for l in [self.lbl_res, self.lbl_fps, self.lbl_cursor, self.lbl_aud]:
            l.configure(bg=c["bg_card"], fg=c["fg_text"])

        for l in self.timer_labels:
            l.configure(bg=c["bg_card"], fg=c["fg_subtext"])

        for sb in self.timer_spinboxes:
            sb.configure(bg=c["bg_input"], fg=c["fg_text"], buttonbackground=c["btn_spin"], disabledbackground=c["bg_card"], disabledforeground=c["fg_subtext"])

        self.style.configure("TCombobox", fieldbackground=c["bg_input"], background=c["btn_spin"], foreground=c["fg_text"], arrowcolor=c["fg_text"], borderwidth=1)
        self.style.map("TCombobox", fieldbackground=[("readonly", c["bg_input"])], foreground=[("readonly", c["fg_text"])], selectbackground=[("readonly", c["bg_input"])], selectforeground=[("readonly", c["fg_text"])])
        self.lbl_status.configure(bg=c["bg_main"], fg=c["fg_subtext"])

    def toggle_durasi(self):
        state = "normal" if self.mode_var.get() == "timer" else "disabled"
        for sb in self.timer_spinboxes:
            sb.config(state=state)

    def mulai_rekam(self):
        durasi_target = None
        if self.mode_var.get() == "timer":
            try:
                durasi_target = int(self.jam_var.get() or 0) * 3600 + int(self.menit_var.get() or 0) * 60 + int(self.detik_var.get() or 0)
                if durasi_target <= 0:
                    messagebox.showwarning("Durasi Kosong", "Masukkan durasi waktu lebih dari 0 detik.")
                    return
            except ValueError:
                messagebox.showerror("Input Salah", "Durasi waktu harus berupa angka.")
                return

        self.waktu_mulai = time.time()
        self.root.withdraw()

        self.overlays.tampilkan_kontrol(self.hentikan_rekaman)
        if self.show_fps_var.get():
            self.overlays.tampilkan_fps()

        fps_angka = float(self.fps_combo.get().split()[0])
        tampilkan_kursor = (self.cursor_combo.get() == "Tampilkan Kursor Mouse")

        threading.Thread(
            target=self.engine.mulai_proses,
            args=(RESOLUSI_MAP[self.res_combo.get()], fps_angka, self.audio_combo.get(), tampilkan_kursor, self.on_selesai_simpan),
            daemon=True
        ).start()

        self.loop_update_overlay(durasi_target)

    def loop_update_overlay(self, durasi_target):
        if not self.engine.is_recording:
            return
        berjalan = int(time.time() - self.waktu_mulai)
        if durasi_target:
            sisa = max(0, durasi_target - berjalan)
            m, d = divmod(sisa, 60)
            teks = f"⏳ -{m:02d}:{d:02d}"
            if sisa <= 0:
                self.hentikan_rekaman()
                return
        else:
            m, d = divmod(berjalan, 60)
            teks = f"● {m:02d}:{d:02d}"

        self.overlays.perbarui_info(teks, self.engine.current_fps if self.show_fps_var.get() else None)
        self.root.after(500, lambda: self.loop_update_overlay(durasi_target))

    def hentikan_rekaman(self):
        if not self.engine.is_recording:
            return
        self.engine.is_recording = False
        self.overlays.tutup_semua()
        self.root.deiconify()
        self.lbl_status.config(text="Status: Menyimpan & memproses audio/video...", fg=PALET_TEMA[self.tema_saat_ini]["status_warn"])
        self.btn_start.config(state="disabled")

    def on_selesai_simpan(self, filename):
        self.root.after(0, lambda: self._reset_ui(filename))

    def _reset_ui(self, filename):
        self.btn_start.config(state="normal")
        self.lbl_status.config(text=f"Tersimpan: {filename}", fg=PALET_TEMA[self.tema_saat_ini]["status_ok"])


if __name__ == "__main__":
    root = tk.Tk()
    app = ProScreenStudioApp(root)
    root.mainloop()
