import random
import string


def create_key():
    lenght_key = 20
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(lenght_key))
    return key

    