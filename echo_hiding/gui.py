import tkinter as tk
from tkinter import messagebox
from EchoHidingAudioStego import encodeAudio, decodeAudio
from utils import selectAudioFile, saveOutputFile

def launch_gui():
    root = tk.Tk()
    root.title("Audio Steganography - Echo Hiding")

    # === VARIABLES ===
    input_audio_path = tk.StringVar()
    output_audio_path = tk.StringVar()
    audio_to_decode_path = tk.StringVar()
    decoded_output = tk.StringVar()
    decode_length = tk.StringVar()
    embed_length_var = tk.BooleanVar(value=False)  # checkbox par défaut activée
    d0_var = tk.IntVar(value=1000)   # Delay pour bit 0
    d1_var = tk.IntVar(value=2000)  # Delay pour bit 1
    alpha_var = tk.DoubleVar(value=0.5)  # Amplifacation factor

    # === FONCTIONS ===
    def choose_audio():
        input_audio_path.set(selectAudioFile())

    def choose_output_audio():
        output_audio_path.set(saveOutputFile())

    def choose_decode_audio():
        audio_to_decode_path.set(selectAudioFile())

    def encode():
        try:
            audio = input_audio_path.get()
            text = entry_message.get()
            if not text:
                raise ValueError("Veuillez saisir un message à encoder.")
            out = output_audio_path.get()
            embed_len = embed_length_var.get()
            d0 = d0_var.get()
            d1 = d1_var.get()
            alpha = alpha_var.get()

            encodeAudio(audio, out, text, d0=d0, d1=d1, alpha=alpha, embed_length=embed_len)
            messagebox.showinfo("Succès", "Encodage terminé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def decode(auto=True):
        try:
            path = audio_to_decode_path.get()
            if not path:
                raise ValueError("Veuillez sélectionner un fichier à décoder.")
            d0 = d0_var.get()
            d1 = d1_var.get()
            
            if auto:
                result = decodeAudio(path, d0=d0, d1=d1)
            else:
                length_str = decode_length.get()
                if not length_str.isdigit():
                    raise ValueError("Veuillez entrer une longueur (en octets) valide.")
                result = decodeAudio(path, d0=d0, d1=d1, force_length=int(length_str))
            decoded_output.set(result)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # === INTERFACE ===

    # --- ENCODES ---
    tk.Label(root, text="Encodage").grid(row=0, column=0, sticky="w", pady=10)

    tk.Button(root, text="Choisir audio source", command=choose_audio).grid(row=1, column=0)
    tk.Label(root, textvariable=input_audio_path).grid(row=1, column=1)

    tk.Label(root, text="Message à encoder").grid(row=2, column=0)
    entry_message = tk.Entry(root, width=50)
    entry_message.grid(row=2, column=1)

    # Case à cocher pour longueur du message
    tk.Checkbutton(root, text="Encoder la longueur du message (16 bits)",
                   variable=embed_length_var).grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

    # Champs pour d0 et d1
    tk.Label(root, text="Delay bit 0 (d0)").grid(row=4, column=0)
    tk.Entry(root, textvariable=d0_var, width=10).grid(row=4, column=1, sticky="w")

    tk.Label(root, text="Delay bit 1 (d1)").grid(row=5, column=0)
    tk.Entry(root, textvariable=d1_var, width=10).grid(row=5, column=1, sticky="w")

    tk.Label(root, text="Facteur d'amplification alpha").grid(row=6, column=0)
    tk.Entry(root, textvariable=alpha_var, width=10).grid(row=6, column=1, sticky="w")

    tk.Button(root, text="Choisir sortie audio", command=choose_output_audio).grid(row=7, column=0)
    tk.Label(root, textvariable=output_audio_path).grid(row=7, column=1)

    tk.Button(root, text="Encoder", command=encode).grid(row=8, column=0, pady=10)

    # --- DECODE ---
    tk.Label(root, text="Décodage").grid(row=9, column=0, sticky="w", pady=10)

    tk.Button(root, text="Choisir audio à décoder", command=choose_decode_audio).grid(row=10, column=0)
    tk.Label(root, textvariable=audio_to_decode_path).grid(row=10, column=1)

    tk.Label(root, text="Longueur message (en octets) [optionnel]").grid(row=11, column=0)
    tk.Entry(root, textvariable=decode_length).grid(row=11, column=1)

    tk.Button(root, text="Décoder (automatique)", command=lambda: decode(auto=True)).grid(row=12, column=0, pady=5)
    tk.Button(root, text="Décoder (manuel)", command=lambda: decode(auto=False)).grid(row=12, column=1)

    tk.Label(root, textvariable=decoded_output, wraplength=400).grid(row=13, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
