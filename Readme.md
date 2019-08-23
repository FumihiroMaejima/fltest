# Sample ToDo Site by Python

### 構成

-Python:3.7
-MySQL:5.7
-Nginx:1.13


## 開発環境構築

### コンテナのビルド

```
docker-compose up -d
```

### アプリケーションのコンテナにアクセス

```
docker exec -it fltest_uwsgi /bin/bash
```

### DBの初期化

```
flask db init
```

### マイグレーション実行

```
flask db migrate
```
### DBのアップグレード

```
flask db upgrade
```