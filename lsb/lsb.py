import wave
import logging

logging.basicConfig(level=logging.INFO)

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    text = ''
    for char in chars:
        if char == '00000011': 
            break
        text += chr(int(char, 2))
    return text

def lsb_encode(audio_input, audio_output, message, lsb_count=2):
    audio = wave.open(audio_input, mode='rb')
    if audio.getsampwidth() not in [1, 2]:
        raise ValueError("Seuls les fichiers WAV 8 ou 16 bits sont supportés.")
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    message += chr(3)
    bits = text_to_bits(message)
    padded_bits = bits + '0' * ((lsb_count - len(bits) % lsb_count) % lsb_count)

    if (len(padded_bits) // lsb_count) > len(frame_bytes):
        raise ValueError("Message trop long pour ce fichier audio")
    index = 0

    for i in range(0, len(padded_bits), lsb_count):
        chunk = padded_bits[i:i + lsb_count]
        frame_bytes[index] &= (255 << lsb_count)
        frame_bytes[index] |= int(chunk, 2)
        index += 1

    modified_audio = wave.open(audio_output, 'wb')
    modified_audio.setparams(audio.getparams())
    modified_audio.writeframes(bytes(frame_bytes))
    modified_audio.close()
    audio.close()
    logging.info("Encodage terminé avec succès.")

def lsb_decode(audio_input, lsb_count=2):
    audio = wave.open(audio_input, mode='rb')
    frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    bits = ''
    for byte in frame_bytes:
        bits += format(byte, '08b')[-lsb_count:]
    return bits_to_text(bits)

if __name__ == "__main__":
    input_file = "input.wav"
    output_file = "output_steg.wav"
    message = "Le rendez-vous est à minuit"
    lsb_count = 2
    lsb_encode(input_file, output_file, message, lsb_count)
    decoded = lsb_decode(output_file, lsb_count)
    print("Message décodé :", decoded)
