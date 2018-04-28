import hashlib

def get_hash_str(upload_file, block_size = 8192 ) :
    md5 = hashlib.md5()
    f = upload_file
    while True :
        buf = f.read(block_size)
        if not buf :
            break
        md5.update(buf)
    return md5.hexdigest()
