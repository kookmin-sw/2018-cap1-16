import hashlib

def get_hash_str(buf, block_size = 8192 ) :
    md5 = hashlib.md5()
    md5.update(buf)
    return md5.hexdigest()
