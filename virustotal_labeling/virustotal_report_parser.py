import json, os

class Parser :
    def __init__(self, path) :
        self.path = path
        with open(path, 'r') as f :
            self.json_obj = json.loads(f.read())
    def md5(self) :
        try :
            return self.json_obj['md5']
        except :
            return 'no-md5-result'
    def sha256(self):
        try :
            return self.json_obj['sha256']
        except :
            return 'no-sha256-result'
    def sha1(self):
        try:
            return self.json_obj['sha1']
        except :
            return 'no-sha1-result'
    def result(self, antivirus_name):
        try :
            return self.json_obj['scans'][antivirus_name]['result']
        except :
            return 'no-label-result'
    def detected(self, antivirus_name):
        try :
            return self.json_obj['scans'][antivirus_name]['detected']
        except :
            return 'no-detected-result'
    def positives(self):
        try :
            return self.json_obj['positives']
        except :
            return 'no-positives-result'
    def total(self):
        try :
            return self.json_obj['total']
        except :
            return 'no-total-result'
    def scan_date(self):
        try :
            return self.json_obj['scan_date']
        except :
            return 'no-scan_date-result'
    def positive_engine_list(self) :
        try :
            ret_list = []
            for engine, result in self.json_obj['scans'].items() :
                if result['detected'] :
                    ret_list.append(engine)
            return ret_list
        except :
            return []
    def negative_engine_list(self) :
        try :
            ret_list = []
            for engine, result in self.json_obj['scans'].items() :
                if not result['detected'] :
                    ret_list.append(engine)
            return ret_list
        except :
            return []
