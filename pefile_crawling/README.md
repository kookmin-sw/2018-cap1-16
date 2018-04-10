# Benign Crawling

### Update Log
#### Version 2018.03.24
* exe 파일을 32bit, 64bit로 구분해서 `<md5>.vir` 형태로 저장하는 크롤러 제작
* dll 파일을 32bit, 64bit로 구분해서 `<md5>.vir` 형태로 저장하는 기능 추가
* path 확인 오류 수정

#### Version 2018.03.26
* `DESTINATION_PATH` 가 없을경우 생성 하도록 수정

#### Version 2018.04.10
* main.py 제거
* benign_crawling.py 이름 pefile_crawling.py 로 수정
* pefile_crawling.py 를 독립적으로 실행 가능하게 수정

### Requirement
* [pefile](https://github.com/erocarrera/pefile)
* [python 3](https://www.python.org/downloads/)

### Usage
```bash
$ python pefile_crawling.py <디렉토리> : <디렉토리> 에 있는 pefile을 크롤링 한다.
```