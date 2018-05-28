# Installation
### install Elasticsearch
* www.elastic.co -> download -> elasticsearch -> .deb file download
* sudo dpkg -i <'deb file path'>

### Configuration
* sudo vim /etc/elasticsearch/elasticsearch.yml
```
  network.host: <set your host ip>
  http.port: 9200
```
* restart elasticsearch service
```
  $ sudo service elasticsearch restart
```

* if you operate multiple node
```
  discovery.zen.ping.unicast.hosts: ["host1 ip", "host2 ip", ...]
```
if you want more information, See the www.elastic.co documnetation

### setting various index
* setting main index
```  
  $ curl -XPUT <hostIP>:<Port>/<input index name you want use main>
```

* setting ssdeep index
```
  $ sh <Project_ROOT>/elasticsearch/script/settings_ssdeep.sh
```

* if you want delete index
```
  $ curl -XDELETE <hostIP>:<Port>/<Index you want delete>
```

### setting configuration file
* modify mask_elasticsearch/settings.py
```
  IP = '<set your host ip>'
  Port = <set your master node http port>
  
  main_index = '< set your main index >'
  cuckoo_index = '< update your cuckoo sandbox's elasticsearch index >'
```

### How to Upload your report
* upload peviewer report or ssdeep report
```
  open the upload_<???>.py in management_script and change Directory path to your report Directory PATH 
```


