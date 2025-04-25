import numpy as np
import soundfile as sf
from scipy.fft import fft, ifft
from math import pi
import tkinter as tk
from tkinter import filedialog, messagebox
import os

L = 1024

def get_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def phase_enc(signal, text):
    data = get_bits(text)
    I = len(signal)
    m = len(data)
    N = I // L
    s = signal[:N*L].reshape((N, L))
    w = fft(s)
    Phi = np.angle(w)
    A = np.abs(w)

    DeltaPhi = np.zeros((N, L))
    for k in range(1, N):
        DeltaPhi[k] = Phi[k] - Phi[k-1]

    PhiData = np.array([pi/2 if bit == '0' else -pi/2 for bit in data])
    Phi_new = np.copy(Phi)
    mid = L // 2
    Phi_new[0, mid - m:mid] = PhiData
    Phi_new[0, mid+1:mid+1+m] = -PhiData[::-1]

    for k in range(1, N):
        Phi_new[k] = Phi_new[k-1] + DeltaPhi[k]

    z = np.real(ifft(A * np.exp(1j * Phi_new)))
    out = z.reshape(-1)
    return np.concatenate((out, signal[N*L:]))

class EncodeApp:
    def __init__(self, root):
        self.root = root
        root.title("Phase Coding - Encodage")
        root.geometry("500x300")

        self.audio_path = None

        tk.Label(root, text="Message à cacher :").pack(pady=8)
        self.text_entry = tk.Entry(root, width=60)
        self.text_entry.pack(pady=5)

        tk.Button(root, text="🎵 Sélectionner un fichier .wav", command=self.load_audio).pack(pady=10)
        tk.Button(root, text="🔐 Encoder le message", command=self.encode).pack(pady=5)

    def load_audio(self):
        self.audio_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        if self.audio_path:
            messagebox.showinfo("Fichier sélectionné", os.path.basename(self.audio_path))

    def encode(self):
        if not self.audio_path:
            messagebox.showerror("Erreur", "Aucun fichier audio sélectionné.")
            return
        message = self.text_entry.get()
        if not message:
            messagebox.showerror("Erreur", "Message vide.")
            return
        audio, fs = sf.read(self.audio_path)
        if audio.ndim > 1:
            audio = audio[:, 0]
        stego = phase_enc(audio, message)
        out_path = self.audio_path.replace(".wav", "_stego.wav")
        sf.write(out_path, stego, fs)
        messagebox.showinfo("Succès", f"Audio encodé sauvegardé sous :\n{out_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncodeApp(root)
    root.mainloop()
