# 택시 프로젝트

## 프로젝트 폴더 구조

* /main : 아래 세 가지 작업을 합친 코드입니다.
* /dynamic : 동적 페이지(채팅방)에 대한 Django 프로젝트입니다.
* /static : 정적 페이지에 대한 Django 프로젝트입니다.
* /templates : html + css 디자인 코드입니다.



## 사용법
1. django 설치 
```
pip install django
```

2. /main/taxi폴더에서 다음 명령어로 서버 실행
```
python ./manage.py runserver
```

127.0.0.1:8000에서 접속이 가능해집니다.

3. 
기본 관리자 계정은
http://127.0.0.1:8000/admin 페이지에서 사용 가능하며, 기본 로그인 계정은

계정id : 0
비밀번호 : 관리자

로 로그인 하면 됩니다.

http://127.0.0.1:8000/admin/chat/customuser 페이지에서 가능합니다.
