import os
import subprocess
from overjoyed.espeak import ESpeak
from overjoyed.utils import generate_random_string

def send_audio(bot, chat_id, text):
    audio_file_path = get_text_to_speech_file(text)
    try:
        with open(audio_file_path, 'rb') as audio_file:
            bot.send_voice(chat_id=chat_id, voice=audio_file)
    except Exception as e:
        logging.error(f"Error sending audio: {e}")
        raise
    finally:
        os.remove(audio_file_path)

def get_text_to_speech_file(text):
    tmp_file_path = f'/tmp/{generate_random_string(20)}.wav'
    espeak = ESpeak(voice='es+m2')

    espeak.save(text, tmp_file_path)
    ogg_tmp_file_path = transcode_to_ogg(tmp_file_path)
    return ogg_tmp_file_path

def transcode_to_ogg(file_path):
    output_file_path = f'{remove_extension(file_path)}.ogg'
    oggenc_cmd = ['oggenc', '-q3', '-o', output_file_path, file_path]
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.check_call(oggenc_cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    except Exception as e:
        logging.error(f"Error transcoding to OGG: {e}")
        raise
    finally:
        os.remove(file_path)

    return output_file_path

def remove_extension(file_path):
    file_path_without_extension, _ = os.path.splitext(file_path)
    return file_path_without_extension
