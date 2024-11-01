import urllib
import os
import giphypop
from troll_bot.utils import generate_random_string

def send_gif(bot, chat_id, text):
    gif_path = get_gif_file_path(text)

    try:
        with open(gif_path, 'rb') as gif_file:
            bot.send_document(chat_id, gif_file)
    except Exception as e:
        logging.error(f"Error sending GIF: {e}")
        raise
    finally:
        os.remove(gif_path)

def get_gif_file_path(text):
    giphy = giphypop.Giphy()
    tmp_file_path = f'/tmp/{generate_random_string(20)}.gif'
    gif_url = giphy.translate(text).media_url
    try:
        urllib.request.urlretrieve(gif_url, tmp_file_path)
    except Exception as e:
        os.remove(tmp_file_path)
        logging.error(f"Error retrieving GIF: {e}")
        raise

    return tmp_file_path
