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


### apply setting script
```
  $ sh <Project_ROOT>/elasticsearch/script/settings_seclab.sh
```
