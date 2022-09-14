import uuid

def unique_id_generator():
    res = str( uuid.uuid4() )
    return res


if __name__ == "__main__":
    print(unique_id_generator())
