import ssdeep, os, json

DIR = '/home/jun/similarity_files_ops/'
OUT_DIR = '/home/jun/similarity_files_report/'
files = os.listdir(DIR)
for file in files:
	abs_url = os.path.join(DIR,file)
	abs_out_url = os.path.join(OUT_DIR,file.replace('.ops',"json"))

	file_md5 = file.replace('.ops',"")
	ssdeep_str = ssdeep.hash_from_file(abs_url)

	out_file = open(abs_out_url,'w',encoding='utf-8')
	report = dict()
	report['MD5'] = file_md5
	report['SSDeep'] = ssdeep_str
	json.dump(report, out_file, ensure_ascii=False, indent = '\t')

