# InfluxDB
## InfluxDB 설치
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


## Grafana 설치
```shell
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-9.2.5-1.x86_64.rpm
yum install -y grafana-enterprise-9.2.5-1.x86_64.rpm
systemctl restart grafana-server
```

### 실행 및 확인
http://내아이피:3000 을 입력해 실행되는지 확인해준다.<br/>
![image](./image/influxdb/4.png)<br/>

## InfluxDB, Grafana 연동
### InfluxDB 토큰 발급받기
![image](./image/influxdb/5.png)<br/>
![image](./image/influxdb/6.png)<br/>
![image](./image/influxdb/7.png)<br/>
발급된 토큰 저장<br/>
![image](./image/influxdb/8.png)<br/>

### InfluxDB Organization, Bucket 생성
![image](./image/influxdb/11.png)<br/>
![image](./image/influxdb/12.png)<br/>


### InfluxDB, Grafana에 연결
![image](./image/influxdb/2.png)<br/>
![image](./image/influxdb/3.png)<br/>
![image](./image/influxdb/9.png)<br/>
![image](./image/influxdb/10.png)<br/>




