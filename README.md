**Konlpy 작업하면서 오류 처리 내용**

- java jdk 설치
- 환경변수 설정
  - 시스템 변수에 JAVA_HOME: C:\Program Files\Java\"jdk version"\bin 추가
  - 시스템 변수 path 항목에 C:\Program Files\Java\"jdk version"\bin 추가
    - cmd 창에서 set JAVA_HOME 입력하여 설정 확인.
- python 3.9 버전에 맞는 JPype 설치
  - https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype 접속
  - JPype1‑1.3.0‑cp39‑cp39‑win_amd64.whl 설치 (x64 용)
- Konlpy 설치
  - pip install konlpy
  - konlpy의 jvm.py 내용 수정
   - konlpy가 설치된 경로(ex))...\Lib\site-packages\konlpy)에 있음.
  ```python
              folder_suffix = [
              # JAR
              '{0}',
              # Java sources
              '{0}{1}bin',
              '{0}{1}*',-------------------------------> 여기 * 제거
              # Hannanum
              '{0}{1}jhannanum-0.8.4.jar',
              # Kkma
              '{0}{1}kkma-2.0.jar',
              # Komoran3
              '{0}{1}aho-corasick.jar',
              '{0}{1}shineware-common-1.0.jar',
              '{0}{1}shineware-ds-1.0.jar',
              '{0}{1}komoran-3.0.jar',
              # Twitter (Okt)
              '{0}{1}snakeyaml-1.12.jar',
              '{0}{1}scala-library-2.12.3.jar',
              '{0}{1}open-korean-text-2.1.0.jar',
              '{0}{1}twitter-text-1.14.7.jar',
              '{0}{1}*'-------------------------------> 여기 * 제거
              ]
  ```
- tweety 버전이 4.0 이상이 설치되어 있는 경우, 낮춰주어야 한다.
  - pip install tweepy==3.10.0 
    