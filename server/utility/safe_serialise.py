import json

def safe_serialize(obj):
    default = lambda o: f"<<non-serializable: {type(o).__qualname__}>>"
    res = json.dumps(obj, default=default)

    return res
