import hashlib

def createMD5sum(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest()