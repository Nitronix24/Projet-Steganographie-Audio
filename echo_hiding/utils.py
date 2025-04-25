from tkinter import filedialog

def selectAudioFile():
    return filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])

def selectTextFile():
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

def saveOutputFile():
    return filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])

def readTextFile(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
