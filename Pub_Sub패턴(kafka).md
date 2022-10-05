# Kafka

## 용어
- Topic
- Partiton
- Producer
- Consumer
- Broker
- Zookeeper
- Consumer Group
- Replication

## 설치
### 가상 OS 3개 설치
- broker : 192.168.197.10
- producer : 192.168.197.20
- consumer : 92.168.197.30

- 방화벽 해제(모두다)
```shell
systemctl stop firewalld
systemctl disable firewalld
setenforce 0
```

- jdk설치(모두다)
```shell
yum -y install java-1.8.0-openjdk-devel.x86_64
```

- Kafka 설치(모두다)
```shell
yum install -y wget 
wget https://archive.apache.org/dist/kafka/3.1.0/kafka_2.13-3.1.0.tgz
tar -xzvf kafka_2.13-3.1.0.tgz
mv kafka_2.13-3.1.0 /opt/kafka
```
- 호스트 이름설정
    - 각 컴퓨터
```shell
vi /etc/hostname #각자 이름으로 바꾸고 재부팅
```

- 호스트 끼리 연결하기
```shell
vi /etc/hosts
```
```shell
192.168.197.10 broker
192.168.197.20 producer
192.168.197.30 consumer
```
- 확인
1. broker
```shell
#broker 터미널을 두개 만들어 동시에 해야한다.
/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties # 쥬키퍼 실행

/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties # 카프카 실행
```
![image](./image/Pub_Sub패턴(kafka)/1.png)<br/>
다음과 같이 화면이 출력되면 카프카 서버와 주키퍼 서버가 연결이 성공적으로 된것이다.<br/>

- 토픽 생성하기
```shell
/opt/kafka/bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server broker:9092 # 토픽생성
/opt/kafka/bin/kafka-topics.sh --describe --topic quickstart-events --bootstrap-server broker:9092  # 토픽 클러스터 확인
```
![image](./image/Pub_Sub패턴(kafka)/2.png)<br/>


- 메세지 보내보기(producer)
```shell
/opt/kafka/bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server broker:9092   # producer의 콘솔이 하나 생성된다. 아무 거나 적고 엔터를 눌러 메세지를 카프카에 보내본다.
```
![image](./image/Pub_Sub패턴(kafka)/3.png)<br/>

- 메세지 확인하기(consumer)
```shell
/opt/kafka/bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server broker:9092
```
![image](./image/Pub_Sub패턴(kafka)/4.png)<br/>
다음과 같이 producer에 입력했던 메세지들을 확인 할 수 있다.