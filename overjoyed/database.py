import logging
from pymongo import MongoClient

log = logging.getLogger(__name__)

MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client['troll_bot_db']
collection = db['messages']

def save_message(message):
    try:
        collection.insert_one({
            'chat_id': message.chat.id,
            'user_id': message.from_user.id,
            'text': message.text,
            'date': message.date,
        })
        log.info('Message saved: %s', message.text)
    except Exception as e:
        log.error('Error saving message: %s', e)

def search_messages(chat_id, user_id=None):
    query = {'chat_id': chat_id}
    if user_id:
        query['user_id'] = user_id

    try:
        messages = list(collection.find(query))
        return messages
    except Exception as e:
        log.error('Error searching messages: %s', e)
        return []
