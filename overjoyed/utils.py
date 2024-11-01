import os
import binascii
import random
import logging

def generate_random_string(length):
    """Генерирует случайную строку заданной длины в шестнадцатичном формате."""
    random_bits = os.urandom(length)
    random_string = binascii.hexlify(random_bits)
    return random_string.decode('utf-8')

def return_true_by_percentage(percentage):
    """Возвращает True с заданной вероятностью."""
    case = random.randint(1, 100)
    return case <= percentage

def random_item(list_):
    """Возвращает случайный элемент из списка."""
    if not list_:
        return None
    items = len(list_)
    id_ = random.randint(0, items - 1)
    logging.debug('Item chosen: %s', list_[id_])
    return list_[id_]

def remove_word(words):
    """Удаляет самое короткое слово из списка."""
    removed_word = get_shortest_word(words)
    logging.debug('Removing: %s', removed_word)
    return [word for word in words if word != removed_word]

def get_shortest_word(words):
    """Возвращает самое короткое слово из списка."""
    return min(words, key=len)
