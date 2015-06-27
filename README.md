# 준비
```
$ cd metasearch
$ pip install -r requirements.txt
$ sass static/css/_main.scss:static/css/main.css
$ bower install
```

# Flask 실행
```
$ PYTHONUNBUFFERED=1 python ./metasearch.py
```

# 크롤링
```
cd crawl
./run.sh
```
ex) scrapy crawl coupang -a keyword=세탁기


# 회고? 변명? 아쉬운점?
* `scrapy 0.24.x`를 사용함. 몇일전 릴리즈된 1.0 버전 사용하다 GG
* `scrapyd`, `celery beat`사용해 작성 하다 인코딩문제가 발목. 간단하게 가기로함.
* `qbox` http_auth 안되서 알고보니 노드가 죽어있음. 그런데 인증 실패라고 나옴. :watch:
* ES 벌크 인스트 안함
* ES ngram 토큰하지 않아 `냉장고` -> `장고`같은걸로 검색 안됨
* 크롤러에 qbox 정보가 코드에 남겨둠
* 토요일 스터디 못감. :sob:
* 로그파일 생성 안함
* 쿠팡 크롤링 판매개수 관련 오류가 남아있음
* 항상 그랬지만 출발은 간단하게 만들고 개선해야.. :scream:
* 크롤했을때 아이템이 없으면 아마도 인코딩 문제..
* 평소 안쓰던 unicode_literals 사용함.
* `qbox`에 쿼리하는건 아무래도 `celery`로 뺐어야 하는데...
* WSGI 서버로 동작하는지 테스트 안함
* static/vendor/* static/css/main.css 파일들 일부러 커밋함
