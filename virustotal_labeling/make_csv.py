import csv, os
from virustotal_report_parser import *
from settings import *

def load_jsons(json_path):
    json_dict = dict()
    for root, dirs, files in os.walk(json_path):
        for filename in files:
            md5, ext = os.path.splitext(filename)
            if ext == '.json':
                json_dict[md5] = Parser(os.path.join(root, filename))
    return json_dict

def write_csv(json_dict, antivirus_name):
    with open('report.csv', 'w', newline = '') as f:
        csvWriter = csv.writer(f)
        for md5 in json_dict:
            if json_dict[md5].detected(antivirus_name):
                csvWriter.writerow([md5, 1, json_dict[md5].result(antivirus_name).split('.')[0]])
            else:
                csvWriter.writerow([md5, 0, 'None'])

if __name__ == '__main__':
    write_csv(load_jsons(JSON_PATH), ANTIVIRUS_NAME)


