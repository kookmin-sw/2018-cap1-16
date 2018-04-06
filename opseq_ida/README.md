# Opseq IDA

### Update Log
#### Version 2018.04.06
* IDA Pro를 이용한 opcode seq 및 피쳐해싱을 하는 코드 작성

### Requirement
* IDA Pro
* Python 3.6.x
* Python 2.7.x

### Test environment
* Microsoft Windows 10 Pro 64 bit
* Python 3.6.4
* Python 2.7.13
* IDA Pro 7.0.17.914

### Usage
1. [settings.py](./settings.py) 에서 `IDA_PATH`, `CPU_COUNT` 등을 자신의 환경에 맞게 수정한다.
2. [main.py](./main.py) 를 실행한다.