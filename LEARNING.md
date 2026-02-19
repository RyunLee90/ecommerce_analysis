# 📚 데이터 관리자 학습 노트

### 1. 효율적인 파일 관리
- `ni [파일명]` : PowerShell용 명령어. 마우스 없이 새 파일을 생성함. (예: `ni test.py`)
- 주의사항: `ni` 뒤에 반드시 한 칸의 공백(띄어쓰기)이 있어야 함.

### 2. 환경 동기화 (컴퓨터 간 연동)
- `pip freeze > requirements.txt` : 현재 설치된 라이브러리 목록을 파일로 추출함.
- `pip install -r requirements.txt` : 다른 컴퓨터에서 이 파일에 적힌 도구들을 한꺼번에 설치함.
- 업데이트: 새로운 도구를 설치했을 때 다시 `pip freeze > requirements.txt`를 실행하면 최신 상태로 덮어쓰기됨.

[가장 추천] 마우스 없이 파일 10개도 1초 만에 만드는 법
윤경 님이 시간을 아끼실 수 있도록, 전문가들이 실제로 가장 많이 쓰는 '멀티 생성' 비법입니다. 쉼표(,)를 쓰면 여러 파일을 한 번에 만들 수 있습니다.

###PowerShell
ni 04_data_cleaning.py, 05_visualization.py, 06_final_report.py