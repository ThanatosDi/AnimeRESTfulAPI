# dmhy-RESTfulAPI
動漫花園 RESTful API
## 安裝
安裝必要套件  
```bash
$ python -m pip insatll -r requirements.txt
```
## 使用
 [V1](https://github.com/ThanatosDi/dmhy-RESTfulAPI/blob/master/README.md#v1)
 [V2](https://github.com/ThanatosDi/dmhy-RESTfulAPI/blob/master/README.md#v2)
 ## v1
  - ### GET /v1
       - 首頁，顯示API相關資訊
  - ### GET /v1/list/
       - 動漫花園首頁動畫列表
  - ### GET /v1/list/{anime keyword}
       - 查詢動畫列表  
    
      |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
  - ### GET /v1/list/{lang}
       - 查詢字幕語系的所有動畫
     
      |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |lang             |動畫字幕語系       |string|tc     |
      |                 |                  |      |sc     |
      |                 |                  |      |繁     |
      |                 |                  |      |簡     |
  - ### GET /v1/list/p{page}
       - 動漫花園首頁動畫列表第 {page} 頁，預設值為 1
     
      |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |page             |頁數               |int  |2      |
  - ### GET /v1/list/team{fansub ID}
       - 動漫花園首頁字幕組之動畫列表，詳細字幕組 ID 使用下方 fansubs 查詢
     
      |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |fansub ID        |字幕組ID           |int  | 117   |
  - ### GET /v1/list/{anime keyword}/p{page}
       - 查詢動畫列表，並顯示第 {page} 頁的列表
       
       |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
      |page             |頁數               |int  |2      |
  - ### GET /v1/list/{anime keyword}/{lang}
       - 查詢某語系的動畫列表
       
       |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
      |lang             |動畫字幕語系       |string|tc     |
      |                 |                  |      |sc     |
      |                 |                  |      |繁     |
      |                 |                  |      |簡     |
  - ### GET /v1/list/{anime keyword}/ep{episode}
       - 查詢動畫第 episode 集(話)之列表
       
       |target           |Description       |type  |example|
      |---------------  |------------------|------|-------|
      |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
      |episode          |動畫集數           |int   |5      |
  - ### GET /v1/list/{anime keyword}/team{fansub ID}
       - 查詢某字幕組發布的動畫列表  

       |target           |Description       |type  |example|
       |---------------  |------------------|------|-------|
       |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
       |fansub ID        |字幕組ID           |int  | 117   |
  - ### GET /v1/list/{anime keyword}/{lang}/p{page}
       - 查詢某語系動畫的第 page 頁列表  
       
       |target           |Description       |type  |example|
       |---------------  |------------------|------|-------|
       |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
       |lang             |動畫字幕語系       |string|tc     |
       |                 |                  |      |sc     |
       |                 |                  |      |繁     |
       |                 |                  |      |簡     |
       |page             |頁數               |int  |2      |
  - ### GET /v1/list/{anime keyword}/{lang}/ep{episode}
       - 查詢某語系動畫的第 episode 集(話)列表  
       
       |target           |Description       |type  |example|
       |---------------  |------------------|------|-------|
       |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
       |lang             |動畫字幕語系       |string|tc     |
       |                 |                  |      |sc     |
       |                 |                  |      |繁     |
       |                 |                  |      |簡     |
       |episode          |動畫集數           |int   |5      |
  - ### GET /v1/list/{anime keyword}/{lang}/team{fansub ID}
       - 查詢某字幕組且某語系動畫的列表  
       
       |target           |Description       |type  |example|
       |---------------  |------------------|------|-------|
       |anime keyword    |動畫名稱關鍵字     |string|哥布林  |
       |lang             |動畫字幕語系       |string|tc     |
       |                 |                  |      |sc     |
       |                 |                  |      |繁     |
       |                 |                  |      |簡     |
       |fansub ID        |字幕組ID           |int  | 117   |
  - ### GET /v1/list/{lang}/p{page}
       - 查詢某語系的第 page 頁列表  
       
       |target           |Description       |type  |example|
       |---------------  |------------------|------|-------|
       |lang             |動畫字幕語系       |string|tc     |
       |                 |                  |      |sc     |
       |                 |                  |      |繁     |
       |                 |                  |      |簡     |
       |page             |頁數               |int  |2      |
  - ### GET /v1/list/{lang}/team{fansub ID}
       - 查詢某字幕組發布的某語系列表
       
       |target           |Description       |type  |example|
       |---------------  |------------------|------|-------|
       |lang             |動畫字幕語系       |string|tc     |
       |                 |                  |      |sc     |
       |                 |                  |      |繁     |
       |                 |                  |      |簡     |
       |fansub ID        |字幕組ID           |int  | 117   |
  - ### GET /v1/fansubs
       - 回傳全部字幕組 ID
## v2    
  - ### GET /v2
       - 首頁，顯示API相關資訊
  - ### GET /v2/list
       - 動漫花園首頁動畫列表
  - ### GET /v2/list/{keyword}
       - 執行搜索功能，每個關鍵字之間用空白隔開或使用+相連，關鍵字越詳細回傳的資料越符合所需
