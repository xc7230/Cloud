# AWS
# 로드벨런싱
서버에 들어오는 부하를 분산시킨다.

## 리눅스 실습
- centos를 이용해서 가상머신 3대 생성
- 3대 네트워크 설정(NAT)
- 2대는 apache 웹서버 설정

### 순서
1. 두 개의 웹서버를 로드벨런싱 하기
2. DB 서버 만들고 연결하기
3. 워드프레스 다운, 압축풀기
4. 두 번째 웹서버 멈추고 로드벨런싱한 가상머신에 워드프레스 연결하기
5. 서버는 첫 번째 웹서버만 연결되었기 때문에 첫 번째 가상머신에만 생성된 워드프레스 파일이 생김
6. 그걸 두 번째 웹서버 가상머신에 옮기고 다시 서버 실행하기

## 구현

1. 설정하기

```shell
cd /var/www/html
touch test.html
vi test.html  내용은 web1, web2로 각각 변경
```

2. HAPROXY(서버 가상머신 말고 남은 1개로)

- 다운
``` shell
yum install -y haproxy
```



- 편집
```shell
vi /etc/haproxy/haproxy.cfg
```

실행되는 문서 맨 밑에 추가
```
 listen stats
            bind :9000
            stats enable
            stats realm Haproxy\ Statistics
            stats uri /haproxy_stats


        frontend  http-in
            bind *:80
            mode                        http
            default_backend             webserver


        backend webserver
            balance     roundrobin
            server  home1 [192.168.197.10]:80 check
            server  home2 [192.168.197.20]:80 check
```

- 확인
```shell
systemctl stop firewalld
systemctl restart haproxy
netstat -anlp | grep :80
```
http://[haproxy 서버의 IP주소]:9000/haproxy_stats 로 접속해서 확인

![image](./image/aws2/1.png)

http://192.168.197.30/test.html 계속 접속해보면 web1, web2가 순서대로 나옴

### 워드프레스 연결

- db용 가상머신 생성

#### Mysql
- 다운
``` shell
 yum install -y mysql-server
```
- 실행 및 설정
```shell
systemctl restart mysqld
mysql_secure_installation
NO
qwer1234
qwer1234
y
y
y
y
```
```mysql
CREATE DATABASE wordpress;
CREATE USER 'kjg'@'%'IDENTIFIED BY 'qwer1234';
GRANT ALL PRIVILEGES ON wordpress.* TO 'kjh'@'%';
FlUSH PRIVILEGES;
EXIT;
```
- DB서버 접속 확인
```shell
yum install -y mysql
mysql -u [DB아이디] -p -h [DB아이피]
```

### wordpress 연결하기

- 두 번째 서버 닫고 하나부터 시작한다.
```shell
systemctl stop httpd
```

- PHP설치
``` shell
 yum install -y php php-common php-opcache php-cli php-gd php-curl php-mysqlnd php-mysqli

yum install wget
```
- wordpress 다운로드

```shell
wget https://ko.wordpress.org/latest-ko_KR.tar.gz
```

- 압축 해제 및 경로 이동
``` shell
tar zxvf latest-ko_KR.tar.gz
mv wordpress /var/www/html
```

- 권한 부여, 방화벽 제거
``` shell
chmod -R 755 /var/www/html/wordpress

systemctl stop firewalld
setenforce 0

```

- 두 번째 가상 머신에 워드 프레스 파일 옮기기
```shell
scp /var/www/html/wordpress/wp-config.php 192.168.197.20:/var/www/html/wordpress/wp-config.php

systemctl restart httpd
```



- 워드프레스 실행, 설정
http://192.168.197.30/wordpress

![image](./image/aws2/2.png)

### DB 삭제하기
```shell
mysql -u root -p
```

```mysql
DROP DATABASE wordpress;
CREATE DATABASE wordpress;
```

### 워드프레스 파일 삭제하기
```shell
rm -rf /var/www/html/wordpress/wp-config.php
```

## aws 실습
우선 인스턴스 2개를 만든 다음 우분투 웹서버

### 로드벨런싱
![image](./image/aws2/3.png)
![image](./image/aws2/4.png)
![image](./image/aws2/5.png)
![image](./image/aws2/6.png)
![image](./image/aws2/7.png)
![image](./image/aws2/8.png)
![image](./image/aws2/9.png)
![image](./image/aws2/10.png)
![image](./image/aws2/11.png)

### 이미지 만들기
기존 OS에 셋팅된 그대로 이미지 파일을 만든다.
![image](./image/aws2/12.png)
![image](./image/aws2/13.png)
![image](./image/aws2/14.png)


### 만든 이미지를 활용해 Auto scaling그륩 만들기
#### 시작 구성 만들기
![image](./image/aws2/17.png)
![image](./image/aws2/15.png)
![image](./image/aws2/16.png)

#### Auto scaling
![image](./image/aws2/18.png)
![image](./image/aws2/19.png)
![image](./image/aws2/20.png)
![image](./image/aws2/22.png)
![image](./image/aws2/23.png)
![image](./image/aws2/24.png)

### 부하를 줘서 확인 해보기
한개의 가상머신에 putty를 두 개 만든다.

```shell
apt update
apt install stress

한쪽은 top

다른쪽은 stress -c 1
```
- 부하를 주고 난 뒤
![image](./image/aws2/25.png)
새로운 인스턴스가 생긴다. 최대 3개까지 설정해 인스턴스가 3개 까지 나온다.

- 인스턴스가 늘어나고 부하를 끄면 인스턴스가 사라진다.

