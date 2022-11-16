# NEVER CLOUD
## VPC 생성 및 Subnet 생성
### VPC 생성
![image](./image/ncloud/1.png)<br/>
![image](./image/ncloud/2.png)<br/>
![image](./image/ncloud/3.png)<br/>
![image](./image/ncloud/4.png)<br/>
![image](./image/ncloud/5.png)<br/>
![image](./image/ncloud/6.png)<br/>
![image](./image/ncloud/7.png)<br/>
![image](./image/ncloud/8.png)<br/>
![image](./image/ncloud/9.png)<br/>
![image](./image/ncloud/10.png)<br/>
![image](./image/ncloud/11.png)<br/>
![image](./image/ncloud/12.png)<br/>

### Subnet 생성
![image](./image/ncloud/13.png)<br/>
![image](./image/ncloud/14.png)<br/>
![image](./image/ncloud/15.png)<br/>
![image](./image/ncloud/16.png)<br/>

### Network ACL 생성
![image](./image/ncloud/17.png)<br/>
![image](./image/ncloud/18.png)<br/>
![image](./image/ncloud/19.png)<br/>
![image](./image/ncloud/20.png)<br/>
![image](./image/ncloud/21.png)<br/>
![image](./image/ncloud/22.png)<br/>
![image](./image/ncloud/23.png)<br/>
![image](./image/ncloud/24.png)<br/>

### Init Script 생성
![image](./image/ncloud/25.png)<br/>
![image](./image/ncloud/26.png)<br/>

```shell
#!/bin/bash
yum -y install http php
systemctl enable httpd
cd /var/www/html
wget http://211.249.50.207/lab/lab.tgz
tar xvfz lab.tgz
cat phpadd >> /etc/httpd/conf/httpd.conf
systemctl restart httpd
echo 'ncp!@#123' | passwd -stdin root
```

## Server 생성
### Web server 생성
![image](./image/ncloud/27.png)<br/>
![image](./image/ncloud/28.png)<br/>
![image](./image/ncloud/29.png)<br/>
![image](./image/ncloud/30.png)<br/>
![image](./image/ncloud/31.png)<br/>
![image](./image/ncloud/32.png)<br/>

### DB server 생성
![image](./image/ncloud/33.png)<br/>
![image](./image/ncloud/34.png)<br/>

### Server 확인
- public ip 할당받기<br/>
![image](./image/ncloud/35.png)<br/>
![image](./image/ncloud/36.png)<br/>
![image](./image/ncloud/37.png)<br/>

- 확인<br/>
![image](./image/ncloud/38.png)<br/>

### 유사서버 생성
![image](./image/ncloud/39.png)<br/>
![image](./image/ncloud/40.png)<br/>
![image](./image/ncloud/41.png)<br/>

### 이미지 생성
![image](./image/ncloud/42.png)<br/>
![image](./image/ncloud/43.png)<br/>
![image](./image/ncloud/44.png)<br/>

### 이미지를 이용해 서버 생성
![image](./image/ncloud/45.png)<br/>
![image](./image/ncloud/46.png)<br/>

### Web server 추가 스토리지 생성
![image](./image/ncloud/47.png)<br/>
![image](./image/ncloud/48.png)<br/>
![image](./image/ncloud/49.png)<br/>

### Web server 스냅샷 생성
![image](./image/ncloud/50.png)<br/>
![image](./image/ncloud/51.png)<br/>

### 스냅샷을 다른 서버의 추가 스토리지로 생성
![image](./image/ncloud/52.png)<br/>
![image](./image/ncloud/53.png)<br/>

## Load Balancer
### Target Group 생성
![image](./image/ncloud/54.png)<br/>
![image](./image/ncloud/55.png)<br/>
![image](./image/ncloud/56.png)<br/>
![image](./image/ncloud/57.png)<br/>
![image](./image/ncloud/58.png)<br/>

### Load Balancer 생성
![image](./image/ncloud/59.png)<br/>
![image](./image/ncloud/60.png)<br/>
![image](./image/ncloud/61.png)<br/>
![image](./image/ncloud/62.png)<br/>
![image](./image/ncloud/63.png)<br/>

## Auto Scaling
### Launch Configuration
![image](./image/ncloud/64.png)<br/>
![image](./image/ncloud/65.png)<br/>
![image](./image/ncloud/66.png)<br/>
![image](./image/ncloud/67.png)<br/>

### Auto Scaling Group 구성
![image](./image/ncloud/68.png)<br/>
![image](./image/ncloud/69.png)<br/>
![image](./image/ncloud/70.png)<br/>
![image](./image/ncloud/71.png)<br/>
![image](./image/ncloud/72.png)<br/>
![image](./image/ncloud/73.png)<br/>

### Event Rule
![image](./image/ncloud/91.png)<br/>
![image](./image/ncloud/92.png)<br/>
![image](./image/ncloud/93.png)<br/>
![image](./image/ncloud/94.png)<br/>
![image](./image/ncloud/95.png)<br/>
![image](./image/ncloud/96.png)<br/>
![image](./image/ncloud/97.png)<br/>
![image](./image/ncloud/98.png)<br/>

## Object Storage
### Object Storage 구성
![image](./image/ncloud/74.png)<br/>
![image](./image/ncloud/75.png)<br/>

### Bucket
![image](./image/ncloud/76.png)<br/>
![image](./image/ncloud/77.png)<br/>
![image](./image/ncloud/78.png)<br/>
![image](./image/ncloud/79.png)<br/>
![image](./image/ncloud/80.png)<br/>
![image](./image/ncloud/81.png)<br/>

### NAS
![image](./image/ncloud/82.png)<br/>
![image](./image/ncloud/83.png)<br/>
![image](./image/ncloud/84.png)<br/>
![image](./image/ncloud/85.png)<br/>

## DB
### Cloud DB 구성
![image](./image/ncloud/86.png)<br/>
![image](./image/ncloud/87.png)<br/>
![image](./image/ncloud/88.png)<br/>
![image](./image/ncloud/89.png)<br/>
![image](./image/ncloud/90.png)<br/>

### ACG 인바운드 규칙 편집
![image](./image/ncloud/99.png)<br/>
![image](./image/ncloud/100.png)<br/>