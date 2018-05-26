import pefile, hashlib, peutils, os

class Peview :
    __BLOCK_SIZE = 8192
    __USER_DB = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'signatures', 'userdb.txt')

    def __init__(self, file_path) :
        self.__file_path = file_path
        self.__pe = pefile.PE(file_path)
    def get_hash(self):
        with open(self.__file_path, 'rb') as f :
            md5 = hashlib.md5()
            sha1 = hashlib.sha1()
            sha256 = hashlib.sha256()
            while True:
                data = f.read( self.__BLOCK_SIZE )
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
                sha256.update(data)
            try:
                return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest(), self.__pe.get_imphash()
            except:
                return md5, sha1, sha256, ''

    def get_packer_info(self) :
        signatures = peutils.SignatureDatabase(self.__USER_DB)
        matches = signatures.match_all(self.__pe, ep_only=True)
        array = []
        if matches:
            for item in matches:
                if item[0] not in array:
                    array.append(item[0])
        return array

    def get_sections_info(self) :
        array = []
        for section in self.__pe.sections:
            section.get_entropy()
            if section.SizeOfRawData == 0 or (
                    section.get_entropy() > 0 and section.get_entropy() < 1) or section.get_entropy() > 7:
                suspicious = True
            else:
                suspicious = False

            scn = section.Name
            md5 = section.get_hash_md5()
            sha1 = section.get_hash_sha1()
            spc = suspicious
            va = hex(section.VirtualAddress)
            vs = hex(section.Misc_VirtualSize)
            srd = section.SizeOfRawData

            array.append({"name": scn, "hash_md5": md5, "hash_sha1": sha1, "suspicious": spc, "virtual_address": va,
                          "virtual_size": vs, "size_raw_data": srd})

        return array

