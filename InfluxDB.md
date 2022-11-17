# InfluxDB
## 설치
```shell
cat <<EOF | sudo tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdb.key
EOF

sudo yum -y install influxdb2
```

### 실행 및 확인
```shell
systemctl start influxdb    # 실행
```
http://내아이피:8086 를 입력해 실행되는지 확인해준다.<br/>
![image](./image/influxdb/1.png)<br/>


## Grafana와 연동
![image](./image/influxdb/2.png)<br/>
![image](./image/influxdb/3.png)<br/>

http://192.168.197.100:8086/orgs/f5d7a5138bb12d5a/members
G7s84Pv64NNOiSyBQDg01_VNNzUF2U-7GgpYv5n_OUGHfeVtVzSRF01NLKoCp2-obcNunMuqhxwGfOgn2mGFUg==


