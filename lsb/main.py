import logging
import os
from lsb import lsb_encode, lsb_decode

logging.basicConfig(level=logging.INFO)

input_file = "test_audio/sample01.wav"
output_file = "test_audio/sample01_output_8.wav"
message = "Le rendez-vous est à minuit"
lsb_count = 8

if not os.path.exists(input_file):
    raise FileNotFoundError(f"Fichier d'entrée {input_file} introuvable.")

try:
    lsb_encode(input_file, output_file, message, lsb_count=lsb_count)
    logging.info(f"Encodage terminé dans : {output_file}")

    decoded_message = lsb_decode(output_file, lsb_count=lsb_count)
    logging.info(f"Message décodé : {decoded_message}")

except Exception as e:
    logging.error(f"Erreur pendant le traitement : {e}")
