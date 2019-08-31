# Sample ToDo Site by Python

### 構成

-Python:3.7
-MySQL:5.7
-Nginx:1.17


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

### おまけ:Docker imageを作り直す時

```
$ docker-compose down --rmi all
$ sudo rm -rf mysql/mysql_data
$ sudo rm -rf app/src/__pycache__
$ sudo rm -rf app/src/migrations
$ sudo rm -rf app/src/models/__pycache__
```


## 本番環境構築

本番環境での手順を簡単にまとめる。

### 手順

```
・Gitのインストール
・Dockerのインストール
・certbotのインストール
・.well-knownディレクトリの作成
・コンテナのビルド
```
