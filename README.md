<div align="center">
  <img src="https://i.imgur.com/RuYuzTJ.png" width="40%" height="40%">
</div>

### 프로젝트 소개
글로벌 보안제품 인증 기관 [AV-TEST](https://www.av-test.org/)에 통계에 따르면, 해마다 총 악성코드의 개수가 늘어나고 있습니다.
<div align="center">
  <img src="https://www.av-test.org/typo3temp/avtestreports/malware-all-years_sum_en.png" width="70%" height="70%">
</div>

하지만, 악성코드 전문가의 수는 한정적이기 때문에 효율적으로 악성코드를 분석하기 위해서는 자동화된 분석 시스템이 필요합니다. 따라서 악성코드 분석에 대한 새로운 접근 없이는 이러한 추세를 해결하기 어렵습니다. 우리는 4차 산업 혁명이 대두되면서 각광받고 있는 인공지능과 빅데이타 기술을 적용하여
이 문제를 해결하고자 합니다.

MASK(Malware Analysis System in Kookmin)는 파일을 동적, 정적 분석 기술을 사용하여 분석하고 결과를 보여주는 오픈소스 소프트웨어입니다.
우리는 IDA를 이용하여 정적 정보를, Cuckoo Sandbox를 이용하여 동적 정보를 추출한 뒤
tensorflow 이용하여 탐지 모델을 학습하고 분석 결과를 보여줍니다.
추가로 우리의 데이터베이스에 있는 데이터의 검색을 위해 Elastic Search를 도입하였습니다.

### 프로젝트 소개영상

[![MASK](https://img.youtube.com/vi/dztAI8KKLW8/0.jpg)](https://www.youtube.com/watch?v=dztAI8KKLW8)


### Abstract
Recently, the number of newly discovered malwares has increased exponentially.
However, the number of experts analyzing malware is significantly lacking.
Therefore, it is difficult to solve this trend without a new approach to malware analysis.
We tried to solve this problem by applying artificial intelligence and Big Data technology, which are becoming popular with the rise of the 4th industrial revolution.

 Therefore, MASK (Malware Analysis System in Kookmin) is open source software
that analyzes files and displays results using dynamic and static analysis techniques.
We use IDA to extract static analysis information, Cuckoo Sandbox to extract dynamic analysis information,
then use tensorflow to learn the detection model and show the analysis results.
In addition, Elastic Search was introduced to retrieve similar data.

### Installation

[Cuckoo Sandbox](./installation/cuckoo/installation.md)  
[Tensorflow](./installation/tensorflow/installation.md)  
[Web](./installation/web/installation.md)

### Contributors
<img src="https://i.imgur.com/2WTxfI9.jpg" width="200px">

```Python
member_1 = {
  "name" : "한채연",
  "position" : "팀 리더",
  "role" : [
    "동적 분석 시스템 최적화, 자동화",
    "리포트로부터 유용한 피쳐들 추출",
    "논문 분석 및 연구"
  ]
}
```
<img src="https://i.imgur.com/1BKQzug.jpg" width="200px">

```Python
member_2 = {
  "name" : "김영재",
  "position" : "개발자",
  "role" : [
    "정적 분석 자동화",
    "정적 및 동적 피쳐 가공",
    "딥러닝 모델 설계 및 구축",
    "악성코드 크롤러 제작"
  ]
}
```
<img src="https://i.imgur.com/yCDBMRV.jpg" width="200px">

```Python
member_3 = {
  "name" : "명준우",
  "position" : "개발자",
  "role" : [
    "VirusTotal 분석 리포트 수집",
    "파일 간 유사도 추출",
    "딥러닝 모델 설계 및 구축",
    "악성코드 라벨링"
  ]
}
```
<img src="https://i.imgur.com/XTcxVog.jpg" width="200px">

```Python
member_4 = {
  "name" : "이유정",
  "position" : "디자이너",
  "role" : [
    "웹 프론트엔드 제작",
    "포스터 등 디자인"
  ]
}
```
<img src="https://i.imgur.com/QeXONTh.jpg" width="200px">

```Python
member_5 = {
  "name" : "허준녕",
  "position" : "DB 및 시스템 관리자",
  "role" : [
    "프로젝트 인프라 관리",
    "데이터베이스 설계 및 SQL 작성, 관리, 검색엔진 구축",
    "ssdeep를 이용한 파일 유사도 분석",
    "웹서버 구축 및 관리"
  ]
}
```


### License

 [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
