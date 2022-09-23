# 클라우드

## 클라우드란?
- 일반적으로 클라우드 컴퓨팅을 의미
- 인터넷을 통해 가상화된 컴퓨터의 다양한 자원과 어플리케이션을 온디맨드로 제공하는 서비스

## 클라우드 이용 모델
- 퍼블릭 클라우드 : 제공 업체를 이용
- 프라이빗 클라우드 : 자체적으로 클라우드 환경을 만듦
- 하이브리드 클라우드 : 퍼블릭 클라우드 + 프라이빗 클라우드 방식을 적절히 사용하는 방식

## 클라우드 관련 용어
- 인스턴스 : 클라우드 가상 컴퓨터
- 볼륨
- 스냅샷

## 아키텍쳐
- 서버를 어떻게 연결하고 배치할지 설계하는것

### 3계층 아키텍쳐
- 데이터를 보내줄때 용ㄹ

# Ubuntu 웹서버 만들기

1. Apache2 다운
```shell
apt install apache2
```

2. Apache2 실행
```shell
systemctl restart apache2
```

3. 확인
```shell
netstat -anlp | grep :80
```

4. 방화벽 설정
```shell
ufw off
```
aws 인스턴스 보안설정에 가서 http를 추가 해줘야 한다.


![image](./image/aws/24.png)


# DNS설정하기
https://xn--220b31d95hq8o.xn--3e0b707e/

## 내용 수정
```shell
cd /var/www/html
vi test.html
```

# DB서버 설정

## Mysql 서버 다운
```shell
apt install mysql-server
```

## 실행
```shell
systemctl restart mysql
```
## 설정

```shell
mysql_secure_installation

패스워드 설정

y

NO

y

y
```
## Mysql 접속
```shell
 mysql -u root -p
```
### Mysql 계정 만들기
```mysql
GRANT ALL ON wordpress.*TO 'kjh'@'localhost'IDENTIFIED BY 'qwer1234';

flush privileges;
```

## php파일과 연결
```shell
apt install php php-mysql
```

### php연결 확인
```shell
vi /var/www/html/info.php

<?php
phpinfo();
?>

```
## 워드프레스

### 다운 및 압축 풀기
```shell
wget https://ko.wordpress.org/latest-ko_KR.tar.gz

tar zxvf latest-ko_KR.tar.gz

mv wordpress /var/www/html/

권한부여
chmod -R 755 /var/www/html/wordpress


```

### 데이터 베이스 만들기
```mysql
 CREATE DATABASE wordpress
```

### 사이트 수정하기
http://www.cloudcampkjh.kro.kr/wordpress/ 접속 로그인
나오는 화면에 있는 코드 복사


```shell
vi /var/www/html/wp-config.php
```

```shell
chown  -R  www-data:www-data  /var/www/html/wordpress
```


- ID : kjh
- pass : 8#*J3MfUXbpwIFrcbt

## 요약
- DB 서버 필요
- wordpress 다운
- DevOPS 엔지니어
