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
```

### Build DB
```
cd <Project_ROOT>/web
$ python manage.py makemigrations upload_app
$ python manage.py migrate
```
