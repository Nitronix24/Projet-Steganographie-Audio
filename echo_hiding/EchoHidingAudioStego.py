import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, ifft
import warnings
from scipy.io.wavfile import WavFileWarning

def saveToLocation(path, rate, data):
    wavfile.write(path, rate, np.int16(data))

def convertToByteArray(text):
    """Convertit un texte en bits (liste d’entiers 0/1)."""
    return [int(bit) for char in text.encode() for bit in format(char, '08b')]

def convertBitsToText(bits):
    """Transforme une liste de bits en texte (par paquets de 8)."""
    chars = []
    for i in range(0, len(bits), 8):
        byte_str = ''.join(map(str, bits[i:i+8]))
        try:
            chars.append(chr(int(byte_str, 2)))
        except:
            chars.append('?')
    return ''.join(chars)

def generateMixer(L, bits, amp=1.0):
    """Génère un motif de mixage sinusoïdal pour chaque bit."""
    mixer = np.concatenate([
        amp * np.sin(2 * np.pi * np.arange(L) / L) if b == 1 else
        amp * np.cos(2 * np.pi * np.arange(L) / L) for b in bits
    ])
    return mixer

def echo_filter(signal, delay, alpha):
    """Applique un filtre de convolution type écho."""
    kernel = np.zeros(delay + 1)
    kernel[-1] = alpha
    return np.convolve(signal, kernel, mode='full')[:len(signal)]

def encodeAudio(input_path, output_path, message, d0=100, d1=2000, alpha=0.1, L=4096, embed_length=True):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", WavFileWarning)
        rate, data = wavfile.read(input_path)

    if data.ndim > 1:
        data = data[:, 0]  # Mono canal

    signal = data.astype(float)
    bits = convertToByteArray(message)
    original_length = len(bits)

    if embed_length:
        length_bits = [int(b) for b in format(len(message), '016b')]
        bits = length_bits + bits
        print(f"[ENCODE] Encodage de la longueur activé : {len(message)} octets")

    nframe = len(signal) // L
    N = nframe - (nframe % 8)
    print(f"[ENCODE] message en bits : {''.join(map(str, bits))}")
    print(f"[ENCODE] Nombre de bits à encoder : {len(bits)}")

    if len(bits) > N:
        print(f"[WARN] Message trop long, tronqué à {N} bits.")
        bits = bits[:N]
    elif len(bits) < N:
        print(f"[INFO] Message paddé avec des 0 à {N} bits.")
        bits += [0] * (N - len(bits))

    # Création des échos complets
    echo0 = echo_filter(signal, d0, alpha)
    echo1 = echo_filter(signal, d1, alpha)

    mixer = generateMixer(L, bits, amp=1.0)

    embedded = signal[:N*L] + echo0[:N*L] * np.abs(1 - mixer) + echo1[:N*L] * mixer
    out = np.concatenate((embedded, signal[N*L:]))

    saveToLocation(output_path, rate, out)
    print(f"[ENCODE] Fichier audio encodé sauvegardé : {output_path}")
    return True

def decodeAudio(stego_path, d0=100, d1=5000, L=8192, force_length=None):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", WavFileWarning)
        rate, data = wavfile.read(stego_path)

    if data.ndim > 1:
        data = data[:, 0]

    signal = data.astype(float)
    N = len(signal) // L
    frames = signal[:N*L].reshape(N, L).T  # chaque colonne est un frame

    bits = []
    for i in range(N):
        seg = frames[:, i]
        cep = np.real(ifft(np.log(np.abs(fft(seg)) + 1e-10)))
        bit = 0 if cep[d0 + 1] >= cep[d1 + 1] else 1
        bits.append(bit)

    print(f"[DECODE] Nombre de bits détectés : {len(bits)}")

    if force_length is None:
        len_bits = bits[:16]
        msg_length = int("".join(map(str, len_bits)), 2)
        bits = bits[16:16 + msg_length * 8]
        print(f"[DECODE] Longueur automatique détectée : {msg_length} octets")
    else:
        bits = bits[:force_length * 8]
        print(f"[DECODE] Longueur forcée : {force_length} octets")

    msg = convertBitsToText(bits)
    print(f"[DECODE] Message décodé : '{msg}'")
    print(f"[DEBUG] Bits : {''.join(map(str, bits))}")
    return msg

def compute_BER(hidden_text, decoded_text):
    """Calcule le taux d'erreur binaire entre deux messages texte."""
    h_bits = [int(bit) for char in hidden_text.encode() for bit in format(char, '08b')]
    d_bits = [int(bit) for char in decoded_text.encode() for bit in format(char, '08b')]

    L = min(len(h_bits), len(d_bits))
    h_bits, d_bits = h_bits[:L], d_bits[:L]

    errors = sum(h != d for h, d in zip(h_bits, d_bits))
    return (errors / L) * 100  # % d'erreurs


def compute_NC(hidden_text, decoded_text):
    """Calcule la corrélation normalisée entre deux messages texte."""
    h_bits = [int(bit) for char in hidden_text.encode() for bit in format(char, '08b')]
    d_bits = [int(bit) for char in decoded_text.encode() for bit in format(char, '08b')]

    L = min(len(h_bits), len(d_bits))
    x = np.array(h_bits[:L])
    y = np.array(d_bits[:L])

    numerator = np.sum(x * y)
    denominator = np.sqrt(np.sum(x**2) * np.sum(y**2))

    return numerator / denominator if denominator != 0 else 0
