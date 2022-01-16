import os
import random
from flask import session


def get_environment():
    return os.environ.get("my_env", "local")


def short_code_generator():
    result = ""
    char_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    for i in range(6):
        result += random.choice(char_list)
    return result


def is_visitor():
    if 'cus_id' in session:
        return True
    else:
        return False


def is_customer():
    if 'cus_id' and 'Registered' in session:
        return True
    else:
        return False
