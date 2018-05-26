import pefile, hashlib, peutils, os, datetime, string, json

class Peview :
    __BLOCK_SIZE = 8192
    __USER_DB = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'signatures', 'userdb.txt')
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'signatures', 'stringsmatch.json'), 'r') as f :
        __STRING_MATCH = json.load(f)

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

    def get_section_number(self):
        return self.__pe.FILE_HEADER.NumberOfSections

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

    def get_compile_time(self) :
        # timestamp
        tstamp = self.__pe.FILE_HEADER.TimeDateStamp
        try:
            tsdate = datetime.datetime.fromtimestamp(tstamp)
        except:
            tsdate = str(tstamp) + " [Invalid date]"
        return tsdate

    def get_resources_info(self):
        res_array = []
        try:
            for resource_type in self.__pe.DIRECTORY_ENTRY_RESOURCE.entries:
                if resource_type.name is not None:
                    name = "%s" % resource_type.name
                else:
                    name = "%s" % pefile.RESOURCE_TYPE.get(resource_type.struct.Id)

                if name == None:
                    name = "%d" % resource_type.struct.Id

                if hasattr(resource_type, 'directory'):
                    for resource_id in resource_type.directory.entries:
                        if hasattr(resource_id, 'directory'):
                            for resource_lang in resource_id.directory.entries:
                                try:
                                    data = self.__pe.get_data(resource_lang.data.struct.OffsetToData,
                                                       resource_lang.data.struct.Size)
                                except:
                                    pass
                                lang = pefile.LANG.get(resource_lang.data.lang, '*unknown*')
                                sublang = pefile.get_sublang_name_for_lang(resource_lang.data.lang,
                                                                           resource_lang.data.sublang)

                                data = filter(lambda x: x in string.printable, data)

                # print name, data, lang, sublang, hex(resource_lang.data.struct.OffsetToData), resource_lang.data.struct.Size
                res_array.append({"name": name, "data": data, "offset": hex(resource_lang.data.struct.OffsetToData),
                                  "size": resource_lang.data.struct.Size, "language": lang, "sublanguage": sublang})
        except:
            pass
        return res_array

    def get_import_function(self):
        array = []
        library = []
        libdict = {}
        try:
            for entry in self.__pe.DIRECTORY_ENTRY_IMPORT:
                dll = entry.dll
                for imp in entry.imports:
                    address = hex(imp.address)
                    function = imp.name

                    if dll not in library:
                        library.append(dll)
                    array.append({"library": dll, "address": address, "function": function})

            for key in library:
                libdict[key] = []

            for lib in library:
                for item in array:
                    if lib == item['library']:
                        libdict[lib].append({"address": item['address'], "function": item['function']})
        except:
            pass

        return libdict

    def get_mutex_info(self):
        mutexs = self.__STRING_MATCH['mutex']
        array = []
        if hasattr(self.__pe, 'DIRECTORY_ENTRY_IMPORT'):
            for lib in self.__pe.DIRECTORY_ENTRY_IMPORT:
                for mutex in mutexs :
                    if mutex :
                        for imp in lib.imports:
                            if imp.name.decode().startswith(mutex) :
                                array.append(imp.name.decode())

        return sorted(set(array))

    def get_api_alert_info(self):
        alerts = self.__STRING_MATCH['apialert']
        array = []
        if hasattr(self.__pe, 'DIRECTORY_ENTRY_IMPORT'):
            for lib in self.__pe.DIRECTORY_ENTRY_IMPORT:
                for alert in alerts:
                    if alert:  # remove 'null'
                        for imp in lib.imports:
                            if imp.name.decode().startswith(alert):
                                array.append(imp.name.decode())

        return sorted(set(array))
