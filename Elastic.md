# Elastic

## 설치
0. 가상머신 준비
```
		cpu	mem	프로그램
	centos8	2	4	엘라스틱서치    ip : 192.168.197.100
	centos8	1	2	로그스태시      ip : 192.168.197.110
	centos8	1	2	키바나          ip : 192.168.197.120
```

1. 엘라스틱 서치
- 레포지터리 추가
```shell
cat > /etc/yum.repos.d/elasticsearch.repo <<EOF
[elasticsearch-7.x]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
```
- 설치
```shell
dnf -y install elasticsearch
```
- 실행
```shell
systemctl enable elasticsearch
systemctl restart elasticsearch
```

- 확인
```shell
curl http://127.0.0.1:9200
```