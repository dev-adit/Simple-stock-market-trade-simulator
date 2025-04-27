import time
import uuid


def generate_unique_id():
    timestamp = str(int(time.time()))
    unique_id = timestamp + '-' + str(uuid.uuid4())
    return unique_id