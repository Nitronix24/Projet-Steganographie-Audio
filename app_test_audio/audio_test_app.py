import os
import csv
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame

class AudioTestApp:
    def __init__(self, master):
        self.master = master
        master.title("Test Auditif - Audio Steganography")

        # Initialisation du mixer Pygame
        pygame.mixer.init()

        # Variables
        self.subject_id = tk.StringVar()
        self.root_dir = tk.StringVar()
        self.ratings = {}  # (folder, filename) -> IntVar

        # --- Sujet & Sélection du dossier ---
        top_frame = ttk.Frame(master, padding=10)
        top_frame.pack(fill="x")

        ttk.Label(top_frame, text="ID du sujet:").grid(row=0, column=0, sticky="w")
        ttk.Entry(top_frame, textvariable=self.subject_id, width=20).grid(row=0, column=1, sticky="w")
        ttk.Button(top_frame, text="Charger dossier de tests", command=self.load_root).grid(row=0, column=2, padx=10)
        ttk.Label(top_frame, textvariable=self.root_dir).grid(row=1, column=0, columnspan=3, sticky="w")

        self.notebook = None
        self.save_button = None

    def load_root(self):
        path = filedialog.askdirectory()
        if not path:
            return
        self.root_dir.set(path)
        subfolders = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        if not subfolders:
            messagebox.showerror("Erreur", "Aucun sous-dossier trouvé dans le dossier sélectionné.")
            return

        # Clear and rebuild notebook
        if self.notebook:
            self.notebook.destroy()
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill="both", expand=True)

        for folder in sorted(subfolders):
            full_folder = os.path.join(path, folder)
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=folder)
            self.build_folder_tab(tab, full_folder, folder)

        if self.save_button:
            self.save_button.destroy()
        self.save_button = ttk.Button(self.master, text="Enregistrer les résultats", command=self.save_results)
        self.save_button.pack(pady=10)

    def build_folder_tab(self, parent, folder_path, folder_name):
        files = [f for f in os.listdir(folder_path) if f.lower().endswith('.wav')]
        if not files:
            messagebox.showwarning("Attention", f"Aucun fichier WAV dans {folder_name}")
            return
        files = sorted(files)

        # Detect correct reference ending with '_1' or numeric suffix '1'
        ref = None
        for f in files:
            name, _ = os.path.splitext(f)
            m = re.match(r"(.+?)(?:_)?1$", name)
            if m:
                ref = f
                break
        if not ref:
            ref = files[0]

        # Scrollable frame setup
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollable.columnconfigure(0, weight=1)

        # Reference: play and stop buttons aligned next to label
        frame_ref = ttk.Frame(scrollable, padding=5)
        frame_ref.grid(row=0, column=0, sticky="w", pady=(0,10))
        frame_ref.columnconfigure(0, weight=1)
        ttk.Label(frame_ref, text="Référence:").grid(row=0, column=0, sticky="w")
        ttk.Label(frame_ref, text=ref).grid(row=1, column=0, sticky="w")
        ttk.Button(frame_ref, text="▶", width=3,
                   command=lambda p=os.path.join(folder_path, ref): self.play_audio(p)).grid(row=1, column=1, padx=(5,2))
        ttk.Button(frame_ref, text="■", width=3,
                   command=self.stop_audio).grid(row=1, column=2)

        # Test samples
        for idx, f in enumerate(files):
            if f == ref:
                continue
            frame = ttk.Frame(scrollable, padding=5)
            frame.grid(row=idx+1, column=0, sticky="ew")
            frame.columnconfigure(0, weight=1)
            ttk.Label(frame, text=f).grid(row=0, column=0, sticky="w")
            ttk.Button(frame, text="▶", width=3,
                       command=lambda p=os.path.join(folder_path, f): self.play_audio(p)).grid(row=0, column=1, padx=(5,2))
            ttk.Button(frame, text="■", width=3,
                       command=self.stop_audio).grid(row=0, column=2)
            var = tk.IntVar(value=50)
            self.ratings[(folder_name, f)] = var
            slider = tk.Scale(frame, from_=0, to=100, orient="horizontal",
                               variable=var, length=400, resolution=1)
            slider.grid(row=0, column=3, padx=5)
            ttk.Label(frame, textvariable=var, width=3).grid(row=0, column=4)

    def play_audio(self, path):
        try:
            if pygame.mixer.get_busy():
                pygame.mixer.stop()
            sound = pygame.mixer.Sound(path)
            sound.play()
        except Exception as e:
            messagebox.showerror("Erreur audio", str(e))

    def stop_audio(self):
        """Arrête la lecture audio en cours"""
        if pygame.mixer.get_busy():
            pygame.mixer.stop()

    def save_results(self):
        if not self.subject_id.get():
            messagebox.showerror("Erreur", "Entrez l'ID du sujet avant d'enregistrer.")
            return
        csv_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV','*.csv')])
        if not csv_path:
            return
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['subject_id','folder','file','score'])
            for (folder,f), var in self.ratings.items():
                writer.writerow([self.subject_id.get(), folder, f, var.get()])
        messagebox.showinfo("Sauvegarde", f"Résultats enregistrés dans {csv_path}")

if __name__ == '__main__':
    root = tk.Tk()
    app = AudioTestApp(root)
    root.mainloop()
