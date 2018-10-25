# dmhy-RESTfulAPI
動漫花園 RESTful API
## 安裝
安裝必要套件  
```bash
$ python -m pip insatll -r requirements.txt
```
## 使用
  - ### GET /v1
       - 首頁，顯示API相關資訊
  - ### GET /v1/list/
       - 顯示動漫花園首頁動畫列表
  - ### GET /v1/list/{anime keyword}
       - 查詢動畫列表  
    
      |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
  - ### GET /v1/list/{lang}
       - 查詢字幕語言的所有動畫
  - ### GET /v1/list/p{page}
       - 
  - ### GET /v1/list/team{fansub ID}
       - 
  - ### GET /v1/list/{anime keyword}/p{page}
       - 
  - ### GET /v1/list/{anime keyword}/{lang}
       - 
  - ### GET /v1/list/{anime keyword}/ep{episode}
       - 
  - ### GET /v1/list/{anime keyword}/team{fansub ID}
       - 
  - ### GET /v1/list/{anime keyword}/{lang}/p{page}
       - 
  - ### GET /v1/list/{anime keyword}/{lang}/ep{episode}
       - 
  - ### GET /v1/list/{anime keyword}/{lang}/team{fansub ID}
       - 
  - ### GET /v1/list/{lang}/p{page}
       - 
  - ### GET /v1/list/{lang}/team{fansub ID}
       - 
  - ### GET /v1/fansubs
       - 
