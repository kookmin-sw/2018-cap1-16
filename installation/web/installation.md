# Installation
### Prerequisition
* python3
* pip3
* See [MongoDB installation](./installation/mongodb/installation.md)
* See [Tensorflow insatllation](./installation/tensorflow/abc.md)
* See [Cuckoo Sandbox installation](./installation/cuckoo/cuckoo.md)

### Install package
```
$ pip install django
$ pip install pymongo
$ pip install elasticsearch
$ pip install requests
```

### Build DB
```
cd <Project_ROOT>/web
$ python manage.py makemigrations upload_app
$ python manage.py migrate
```

### Configuration
* Goto web/upload_app/mongodb
 - modify md5_search.py
 - client = SeclabMongoClient([your db server ip], 27017, [DB name])


* Goto web/upload_app/es
 - modify es_view.py
 - es = Elasticsearch([{'host':[your elasticsearch ip],'port':9200}])

### How to run server
```
cd <Project_ROOT>/web
$ python manage.py runserver <ip>:<port>
ex) python manage.py runserver 192.168.0.1:80
```
