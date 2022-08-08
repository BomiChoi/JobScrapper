# 💼 Job Scrapper

## 프로젝트 소개
여러 채용 사이트에 올라오는 공고들을 스크랩하여 한 번에 모아보는 웹 어플리케이션 프로젝트입니다.</br>
👉 사이트 바로가기: http://13.209.17.43:5000/

## 사용 기술
<section>
	<img src="https://img.shields.io/badge/HTML5-E34F26?logo=HTML5&logoColor=white"/>
	<img src="https://img.shields.io/badge/CSS3-1572B6?logo=CSS3&logoColor=white"/>
	<img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=JavaScript&logoColor=black"/>
	<img src="https://img.shields.io/badge/Flask-000000?logo=Flask&logoColor=white"/>
	<img src="https://img.shields.io/badge/SQLite-003B57?logo=SQLite&logoColor=white"/>
	<img src="https://img.shields.io/badge/Amazon%20AWS-232F3E?logo=Amazon%20AWS&logoColor=white"/>
</section>

* `Flask`: 파이썬으로 간단하게 웹 어플리케이션을 개발하기 위해 사용하였습니다.
* `Beautifulsoup`: 채용 사이트를 크롤링하기 위해 사용하였습니다.
    - requests 라이브러리로  HTML 코드를 받아온 후 Beautifulsoup 라이브러리로 필요한 데이터를 추출합니다.
* `SQLite`: 검색결과 데이터를 관리하기 위해 사용하였으며, 프로젝트 규모가 작기 때문에 가벼운 데이터베이스인 SQLite를 선택하였습니다.
    - sqlite3 라이브러리를 사용하여 Flask와 연동하였습니다.
    - 처음에는 임시로 딕셔너리에 저장하는 방식을 사용했다가 나중에 SQLite를 연동하여 데이터를 관리하였습니다.
* `AWS EC2`: 개발한 웹 어플리케이션을 배포하기 위해 사용하였습니다.
    - SSH 연결이 끊겨도 백그라운드에서 프로세스가 계속 동작하도록 하였습니다.

## 기능 상세설명
* 키워드를 입력하면 채용사이트에서 채용공고를 크롤링합니다. (Job Korea, Stack Overflow, We Work Remotely)
    - 크롤링 하는 중에는 화면에 대기 메세지가 뜹니다.
* 한 번 검색한 결과는 검색화면의 키워드 목록에 뜨게 됩니다.
    - 키워드를 클릭하면 대기시간 없이 바로 검색결과 페이지로 이동할 수 있습니다.
* 크롤링이 완료되면 검색결과 페이지로 이동합니다.
    - 제목, 기업명, 위치, 마감일, 공고 링크 등을 볼 수 있습니다.
    - 검색 결과를 csv 파일로 내보낼 수 있습니다.

👇 검색 페이지</br>
<img src="https://i.imgur.com/wE63UN2.jpg" width='600'/>

👇 결과 페이지</br>
<img src="https://i.imgur.com/n88dYGB.png" width='600'/>

👇 csv로 내보내기</br>
<img src="https://i.imgur.com/I90acqY.png" width='600'/>

## 앞으로 개선할 점
* SQLAlchemy를 사용하여 더 편하게 DB에 접근하기
* 저장된 키워드들을 한 번에 삭제하는 기능 추가
* 다른 채용사이트 추가
* 크롤링 중일 때 진행 상황 보여주기
* 도메인 연결하기