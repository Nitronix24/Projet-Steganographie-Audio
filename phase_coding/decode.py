
import numpy as np
import soundfile as sf
from scipy.fft import fft
from math import sqrt
import tkinter as tk
from tkinter import filedialog, messagebox
import os

L = 1024

def from_bits(bits):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def phase_dec(signal, L_msg):
    m = 8 * L_msg
    x = signal[:L]
    Phi = np.angle(fft(x))
    data = ''.join('0' if Phi[L//2 - m + k] > 0 else '1' for k in range(m))
    return from_bits(data)

class DecodeApp:
    def __init__(self, root):
        self.root = root
        root.title("Phase Coding - Décodage")
        root.geometry("500x250")

        self.audio_path = None

        tk.Label(root, text="Longueur du message à décoder (en caractères) :").pack(pady=8)
        self.length_entry = tk.Entry(root, width=20)
        self.length_entry.pack(pady=5)

        tk.Button(root, text="🎵 Sélectionner un fichier .wav", command=self.load_audio).pack(pady=10)
        tk.Button(root, text="🕵️‍♂️ Décoder le message", command=self.decode).pack(pady=5)

    def load_audio(self):
        self.audio_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        if self.audio_path:
            messagebox.showinfo("Fichier sélectionné", os.path.basename(self.audio_path))

    def decode(self):
        if not self.audio_path:
            messagebox.showerror("Erreur", "Aucun fichier audio sélectionné.")
            return
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer une longueur valide.")
            return

        audio, _ = sf.read(self.audio_path)
        if audio.ndim > 1:
            audio = audio[:, 0]
        try:
            decoded = phase_dec(audio, length)
            messagebox.showinfo("Message extrait", decoded)
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du décodage : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DecodeApp(root)
    root.mainloop()
