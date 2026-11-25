import cv2
import numpy as np
import mss
import threading
import datetime
import time
import os
import subprocess
import ctypes
import soundcard as sc
import soundfile as sf
import imageio_ffmpeg


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class ScreenRecorderEngine:
    def __init__(self):
        self.is_recording = False
        self.current_fps = 0.0
        self.final_filename = ""

    def dapatkan_posisi_kursor(self):
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt.x, pt.y

    def gambar_kursor(self, frame, x, y):
        pts = np.array([
            [x, y],
            [x, y + 18],
            [x + 4, y + 14],
            [x + 8, y + 21],
            [x + 11, y + 19],
            [x + 7, y + 12],
            [x + 13, y + 12]
        ], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(frame, [pts], (255, 255, 255))
        cv2.polylines(frame, [pts], True, (0, 0, 0), 1, cv2.LINE_AA)

    def rekam_audio_worker(self, mode_audio, file_wav, samplerate=44100):
        try:
            mics = []
            if "Mikrofon" in mode_audio:
                default_mic = sc.default_microphone()
                if default_mic:
                    mics.append(default_mic.recorder(samplerate=samplerate, channels=2))
            if "Desktop" in mode_audio:
                speaker_name = sc.default_speaker().name
                loopback = sc.get_microphone(id=speaker_name, include_loopback=True)
                if loopback:
                    mics.append(loopback.recorder(samplerate=samplerate, channels=2))

            if not mics:
                return False

            for m in mics:
                m.__enter__()

            frames_audio = []
            chunk_size = int(samplerate * 0.1)

            while self.is_recording:
                chunks = [m.record(numframes=chunk_size) for m in mics]
                mixed = np.sum(chunks, axis=0)
                mixed = np.clip(mixed, -1.0, 1.0)
                frames_audio.append(mixed)

            for m in mics:
                m.__exit__(None, None, None)

            if frames_audio:
                audio_data = np.concatenate(frames_audio, axis=0)
                sf.write(file_wav, audio_data, samplerate)
                return True
        except Exception as e:
            print("Error Audio:", e)
        return False
    def mulai_proses(self, target_res, target_fps, mode_audio, show_cursor, on_finished_callback):
        self.is_recording = True
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_video = f"temp_vid_{timestamp}.mp4"
        temp_audio = f"temp_aud_{timestamp}.wav"
        self.final_filename = f"Rekaman_{timestamp}.mp4"

        ada_audio = (mode_audio != "Tanpa Suara (Mute)")
        audio_sukses = [False]

        if ada_audio:
            def run_aud():
                audio_sukses[0] = self.rekam_audio_worker(mode_audio, temp_audio)
            t_aud = threading.Thread(target=run_aud, daemon=True)
            t_aud.start()

        with mss.mss() as sct:
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            out_size = target_res if target_res else (monitor["width"], monitor["height"])

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(temp_video, fourcc, target_fps, out_size)

            frame_count = 0
            fps_timer = time.time()

            while self.is_recording:
                t0 = time.time()
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                if show_cursor:
                    cx, cy = self.dapatkan_posisi_kursor()
                    rel_x = cx - monitor["left"]
                    rel_y = cy - monitor["top"]
                    if 0 <= rel_x < monitor["width"] and 0 <= rel_y < monitor["height"]:
                        self.gambar_kursor(frame, rel_x, rel_y)

                if target_res:
                    frame = cv2.resize(frame, out_size, interpolation=cv2.INTER_AREA)

                out.write(frame)

                frame_count += 1
                if time.time() - fps_timer >= 0.5:
                    self.current_fps = frame_count / (time.time() - fps_timer)
                    frame_count = 0
                    fps_timer = time.time()

                elapsed = time.time() - t0
                sleep_time = (1.0 / target_fps) - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

            out.release()

        if ada_audio:
            t_aud.join(timeout=3)

        if ada_audio and audio_sukses[0] and os.path.exists(temp_audio):
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            cmd = [
                ffmpeg_exe, "-y", "-i", temp_video, "-i", temp_audio,
                "-c:v", "copy", "-c:a", "aac", "-shortest", self.final_filename
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(temp_video):
                os.remove(temp_video)
            if os.path.exists(temp_audio):
                os.remove(temp_audio)
        else:
            if os.path.exists(temp_video):
                os.rename(temp_video, self.final_filename)

        on_finished_callback(self.final_filename)
