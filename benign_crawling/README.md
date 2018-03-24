# Benign Crawling

### Update Log
#### Version 2018.03.24
* exe 파일을 32bit, 64bit로 구분해서 `<md5>.vir` 형태로 저장하는 크롤러 제작
* dll 파일을 32bit, 64bit로 구분해서 `<md5>.vir` 형태로 저장하는 기능 추가
* path 확인 오류 수정

### 사용법
1. `run(<PATH>)` : `<PATH>` 를 기준으로 하위 폴더에 있는 모든 pe파일을 32bit 와 64bit로 구분해서 저장 한다.