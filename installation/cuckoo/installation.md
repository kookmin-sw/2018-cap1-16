# Cuckoo Sandbox 2.0.x Settings Manual

### 0. 설치 환경
#### 1) 호스트 스펙
##### (1) server1 : Cuckoo sandbox 2.0.5
* Xeon® CPU E5-2630v2
* 4T HDD * 5, 1T HDD * 1
* 56G RAM
* Ubuntu 16.04

##### (2) server2 : Cuckoo sandbox 2.0.4
* Xeon® CPU E5-2620 v3
* 2T HDD * 5
* 64G RAM
* Ubuntu 16.04

#### 2) 게스트 스펙 - Sandbox
* Win7 enterprise SP1 32bit
* VirtualBox
* 2048 MB
* ip : 192.168.0.2 ~ 192.168.0.9

* * *
### 1. 기본 패키지 / C 라이브러리 설치
```bash
$ sudo apt-get install -y python-pip python-dev libssl-dev libjpeg-dev zlib1g-dev tcpdump apparmor-utils libffi-dev swig python-setuptools
$ sudo pip install pyopenssl
```

![Imgur](https://i.imgur.com/KqkVFsH.png)

```bash
# 쿠쿠 코어가 네트워크 패킷을 수집할 수 있게끔 하는 과정.
# tcpdump를 보호하는 apparmor(aa)를 disable하고,
# setcap 명령어로 일반 사용자가 루트 권한 없이 tcpdump를 사용할 수 있게끔 함.
$ sudo aa-disable /usr/sbin/tcpdump
$ sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
# setcap 명령어를 사용할 수 없으면 아래와 같이 libcap2-bin 패키지 설치
$ sudo apt-get install libcap2-bin
```
* 샌드박스로 사용될 virtualbox 설치
```bash
# “deb http://download.virtualbox.org/virtualbox/debian xenial contrib”라는 명령어를 터미널에 출력함과 동시에 “/etc/apt/sources.list.d/virtualbox.list” 경로의 파일에 write
# Tee : 리눅스 화면과 파일에 동시에 출력하는 명령어
$ echo deb http://download.virtualbox.org/virtualbox/debian xenial contrib | sudo tee -a /etc/apt/sources.list.d/virtualbox.list
# " https://www.virtualbox.org/download/oracle_vbox_2016.asc “ 경로의 파일을 다운로드 후 이 파일 안의 키값을 apt의 키 리스트에 추가
$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add –
# /etc/apt/sources.list 를 읽어 apt를 업데이트 해줌
$ sudo apt-get update
$ sudo apt-get install -y virtualbox
```
* * *
### 2. 쿠쿠 코어 설치하기
```bash
# pip가 python3과 연동될 경우 pip2 명령어를 이용하여 설치하기
$ sudo pip install cuckoo
```
![Imgur](https://i.imgur.com/y4UxQzM.png)

위와 같은 에러가 날 경우
https://cuckoo.sh/docs/installation/host/requirements.html 에서 setuptools 최신 버전 설치

* * *
### 3. 샌드박스 구성
* 가상머신 다운로드 및 가져오기
![Imgur](https://i.imgur.com/hKSPo32.png)
https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/

윈도우 7 32비트 운영체제 선택
가상머신은 virtualbox로
```bash
$ unzip IE8.Win7.For.Windows.VirtualBox.zip
```
![Imgur](https://i.imgur.com/a0C0JL3.png)

필자는 RAM 2GB 할당
가상 시스템 이름 기억하고 있어야함. -> 추후에 쿠쿠 설정에 필요

![Imgur](https://i.imgur.com/N8wQUYp.png)

시작 > Command Prompt 아이콘에서 우클릭한 후 Run as administrator를 선택하여 관리자모드로 윈도우 프롬프트에 접근
```bash
$ slmgr /ato
```

* 가상머신에서 파이썬 다운로드 및 설치
  - Python2.7 설치 -> Windows x86 MSI installer 선택
   https://www.python.org
  - pillow 라이브러리 설치 : 악성코드 분석을 진행할 때 윈도우 운영체제의 화면의 스크린샷을 찍어 상태를 파악하기 위해

  ![Imgur](https://i.imgur.com/xB4pnbO.png)

  ```bash
  $ cd c:\Python27\Scripts
  $ pip install pillow
  ```
* 네트워크 구성 및 아이피 고정
```bash
$ vboxmanage hostonlyif create
$ vboxmanage hostonlyif ipconfig vboxnet0 --ip 192.168.56.1
```

![Imgur](https://i.imgur.com/CmGzQHv.png)

설정 -> 네트워크 -> 호스트 전용 어댑터 vboxnet0 선택

![Imgur](https://i.imgur.com/o6zMsai.png)
![Imgur](https://i.imgur.com/YBOsnc3.png)

ipconfig, ping으로 네트워크 설정 잘 되었는지 확인

* 방화벽/업데이트 비활성화
![Imgur](https://i.imgur.com/QOhiVsc.png)

시작 > Control Panel > System and Security > windows Firewall > Customize settings
Turn off windows Firewall 선택
![Imgur](https://i.imgur.com/btuevpo.png)

시작 > Control Panel > System and Security > Windows Update > Change settings
Window update 비활성화

* Administrator 계정 활성화 및 로그인
```bash
$ Net user administrator /active:yes
```
![Imgur](https://i.imgur.com/Lb16M1J.png)

관리자 계정을 활성화하고 로그인하는 이유? -> 악성코드가 동작하는데 방해가 없어야 하기 때문
Log off 후 Administrator 계정으로 다시 로그인
만약 패스워드가 걸려있다면? -> 바탕화면의 패스워드를 확인하기

* UAC 비활성화
UAC(User Account Control) :사용자 계정을 제어하는데 사용
![Imgur](https://i.imgur.com/1FIjuTG.png)


* agent.py 실행과 스냅샷 구성
![Imgur](https://i.imgur.com/RObszP8.png)

장치 > 공유 폴더
![Imgur](https://i.imgur.com/q5k7bbb.png)

폴더 경로 : /home/’<계정>’/.cuckoo/agent

![Imgur](https://i.imgur.com/2K6YSnk.png)

시작 > Computer > Network > 공유 폴더 > agent.py 파일을 바탕화면에 복사하기
바탕화면에서 agent.py 실행하기

![Imgur](https://i.imgur.com/Honpk1l.png)

스냅샷 이름 : Snapshot1(추후 설정에 필요)


```bash
$ sudo vi ~/.cuckoo/conf/virtualbox.conf
```
guest OS에 맞게 설정 바꿔주기(ip, snapshot...)
![Imgur](https://i.imgur.com/LUPWtMF.png)

```bash
$ sudo vi ~/.cuckoo/conf/cuckoo.conf
```
샌드박스(가상머신)에서 default gateway에 적은 ip를 resultserver ip에 적기

![Imgur](https://i.imgur.com/GwjTL0W.png)

* * *
### 4. MongoDB 설치 및 설정
```bash
$ sudo apt-get install mongodb
$ sudo vi /etc/mongodb.conf #bind_ip 확인
$ mongo [bind_ip] #127.0.0.1일 경우 생략
> use cuckoo
> db.createUser({user:"cuckoo",pwd:"[password]",roles:[{role:"readWrite",db:"cuckoo"}]})
```
```bash
$ sudo vi ~/.cuckoo.conf/reporting.conf
```
아래와 같이 바꿔주기

![Imgur](https://i.imgur.com/51lRQtD.png)

* * *
### 5. MySQL 설정
```bash
$ sudo apt-get install mysql-server python-mysqldb -y #패스워드 설정
$ sudo myhsql -u root -p #패스워드 입력하기
> create database cuckoo;
> grant all privileges on cuckoo.* to cuckoo@localhost identified by 'Cuck00@n@lyst!';
> flush privileges;
```
```bash
$ sudo vi ~/.cuckoo/conf/cuckoo.conf
```
아래와 같이 설정해주기

![Imgur](https://i.imgur.com/4KrAWo8.png)


* * *
### 6. 샌드박스를 여러 개 구성할 경우
```bash
$ sudo vi ~/.cuckoo/conf/virtualbox.conf
```
샌드박스 추가 후 machines에 샌드박스 이름 추가하고 각 머신에 대한 label, platform, ip 추가하기

![Imgur](https://i.imgur.com/0Yamlfr.png)
![Imgur](https://i.imgur.com/ceZ7Ajy.png)

* * *
### 7. 기타 추가 설정
```bash
sudo vi ~/.cuckoo/conf/memory.conf
```
Guest profile을 guest OS에 맞게 수정하기

![Imgur](https://i.imgur.com/W9jNd5w.png)
