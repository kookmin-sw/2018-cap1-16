# Installation
### Prerequisition
* python 3.6.2
* pip3
* See [MongoDB installation](./installation/mongodb/installation.md)
* See [Tensorflow insatllation](./installation/tensorflow/abc.md)
* See [Cuckoo Sandbox installation](./installation/cuckoo/cuckoo.md)
* see [ElasticSearch installation](./installation/elasticsearch.installation.md)

### Install package
```
$ pip install django
$ pip install pymongo
$ pip install elasticsearch
$ pip install requests
$ pip install peutils
$ install ssdeep for windows -> https://github.com/MacDue/ssdeep-windows-32_64
```

### Build DB
```
cd <Project_ROOT>/web
$ python manage.py makemigrations anlaysisapp
$ python manage.py migrate
```

### Configuration
* setting cuckoo-mongodb 
 1. modify web/analysisapp/mongodb/settings.py
 ```
   Host = <your mongodb's ip which is connected cuckoo >
   Port = <your mongodb's ip which is connected cuckoo >
   CuckooDB = <your mongodb's cuckoo db name>
```
* how to set kibana dashboard
 1. get iframe source from your kibana dashboard's share button
 2. modify web/statisticsapp/templates/statistics.html
 ```
   <div class="panel-body">
      insert your iframe source
   </div>
 ```
 
## How to run server
```
cd <Project_ROOT>/web
$ python manage.py runserver <ip>:<port>
ex) python manage.py runserver 192.168.0.1:80
```
