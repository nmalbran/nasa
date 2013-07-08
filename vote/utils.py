import hashlib

def sha1(val):
    h = hashlib.sha1()
    h.update(val)
    return h.hexdigest()