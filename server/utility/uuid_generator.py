import uuid

def unique_id_generator():
    res = str( uuid.uuid4() )
    return res
