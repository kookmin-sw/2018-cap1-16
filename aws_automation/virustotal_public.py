import requests, json, os

def retrieving_file_scan_report( hash_str, dst_path, key ) :
    try:
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': key, 'resource': hash_str}
        response = requests.get(url, params=params)
        if response.status_code == 200 :
            response_json = response.json()
            response_code = response_json['response_code']
            print(response_json['verbose_msg'])
            if response_code == 1 :
                with open(os.path.join(dst_path, hash_str + '.json'), 'w', encoding='utf8') as f :
                    json.dump(response.json(), f, ensure_ascii=False, indent=4)
            return response_code
        elif response.status_code == 204 :
            print('Request rate limit exceeded. You are making more requests than allowed.')
        elif response.status_code == 400 :
            print('Bad request. Your request was somehow incorrect. This can be caused by missing arguments or arguments with wrong values.')
        elif response.status_code == 403 :
            print('Forbidden. You don\'t have enough privileges to make the request. You may be doing a request without providing an API key or you may be making a request to a Private API without having the appropriate privileges.')
        else:
            print("HTTP Request Error : {}".format(response.status_code))
        return response.status_code
    except Exception as e:
        print(e)

def sending_and_scanning_file( src_path, key ) :
    if os.path.getsize(src_path) >= 32000000 :
        print('File size limit is 32MB')
        return 1
    try :
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = {'apikey': key}
        src_path = src_path.replace(os.sep, '/')
        with open(src_path, 'rb') as f :
            files = {'file': (src_path, f)}
            response = requests.post(url, files=files, params=params)
        if response.status_code == 200:
            response_json = response.json()
            print(src_path, response_json['verbose_msg'])
            return response_json['response_code']
        elif response.status_code == 204 :
            print('Request rate limit exceeded. You are making more requests than allowed.')
        elif response.status_code == 400 :
            print('Bad request. Your request was somehow incorrect. This can be caused by missing arguments or arguments with wrong values.')
        elif response.status_code == 403 :
            print('Forbidden. You don\'t have enough privileges to make the request. You may be doing a request without providing an API key or you may be making a request to a Private API without having the appropriate privileges.')
        else:
            print("HTTP Request Error : {}".format(response.status_code))
        return response.status_code
    except Exception as e:
        print(e)


def rescanning_already_submitted_files( hash_str, key ) :
    params = {'apikey': key, 'resource': hash_str}
    try :
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/rescan', params=params)
        json_response = response.json()
        if response.status_code == 200:
            response_json = response.json()
            response_code = response_json['response_code']
            if response_code == 1:
                print('The file corresponding to the given hash was successfully queued for rescanning.')
            elif response_code == 0:
                print('The file was not present in our file store.')
            else :
                print('The event of some unexpected error')
            return response_code
        elif response.status_code == 204 :
            print('Request rate limit exceeded. You are making more requests than allowed.')
        elif response.status_code == 400 :
            print('Bad request. Your request was somehow incorrect. This can be caused by missing arguments or arguments with wrong values.')
        elif response.status_code == 403 :
            print('Forbidden. You don\'t have enough privileges to make the request. You may be doing a request without providing an API key or you may be making a request to a Private API without having the appropriate privileges.')
        else:
            print("HTTP Request Error : {}".format(response.status_code))
        return response.status_code
    except Exception as e:
        print(e)