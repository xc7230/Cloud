# 쿠버네티스
- 가상머신 준비
```
		cpu(vt)	mem	프로그램
	centos8	2	4	master     ip : 192.168.197.100
	centos8	2	4	node1      ip : 192.168.197.110
	centos8	2	4	node2      ip : 192.168.197.120
```

- 네트워크 연동(master, node1, node2)
```shell
vi /etc/hosts
```
```shell
# 맨 밑에 추가
192.168.197.100 master
192.168.197.110 node1
192.168.197.120 node2
```
## 쿠버네티스 설치 및 설정
### 공용(master, node1, node2)
- 방화벽 설정
```shell
firewall-cmd --permanent --add-port=6443/tcp
firewall-cmd --permanent --add-port=2379-2380/tcp
firewall-cmd --permanent --add-port=10250/tcp
firewall-cmd --permanent --add-port=10251/tcp
firewall-cmd --permanent --add-port=10252/tcp
firewall-cmd --permanent --add-port=10255/tcp
firewall-cmd --reload
modprobe br_netfilter
echo '1' > /proc/sys/net/bridge/bridge-nf-call-iptables

setenforce 0

sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux

init 6  # 재시작
```

- 도커 설치
```shell
yum install -y yum-utils
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum-config-manager --enable docker-ce-nightly
yum-config-manager --enable docker-ce-test
yum install -y docker-ce docker-ce-cli containerd.io --allowerasing

mkdir /etc/docker

cat <<EOF | sudo tee /etc/docker/daemon.json
{
"exec-opts": ["native.cgroupdriver=systemd"],
"log-driver": "json-file",
"log-opts": {
"max-size": "100m"
},
"storage-driver": "overlay2"
}
EOF

systemctl daemon-reload
systemctl restart docker
systemctl enable docker
```

- k8s 설치
```shell
firewall-cmd --add-masquerade --permanent
firewall-cmd --reload

cat <<EOF > /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

sysctl --system # 위의 명령어가 제대로 기입됐는지 확인
```
![image](./image/kubernetes/1.png)<br/>

```shell
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

# 쿠버네티스 1.22.5 버전 다운
dnf install -y kubelet-1.22.5 kubeadm-1.22.5 kubectl-1.22.5 --disableexcludes=kubernetes

systemctl enable kubelet
systemctl start kubelet

```
- k8s swap 설정
```shell
swapoff -a

vi /etc/fstab
#/dev/mapper/cl-swap none swap defaults 0 0 주석 처리해야 함
```
![image](./image/kubernetes/2.png)<br/>

### master 설정
```shell
kubeadm init --pod-network-cidr 192.168.1.0/24
# 만약 에러가 나면 kubeadm reset로 리셋 후 다시 시작한다.


#나오는 명령어 따로 저장해둔다. 사람마다 다름 실행x
kubeadm join 192.168.197.100:6443 --token 5b2pjz.sf4632azhzpcp7f7 \
        --discovery-token-ca-cert-hash sha256:a624bb31c56ec6595a9c8adfe4a7ce5721aae18bd78150ac457bc6f5ca109b20  
```
![image](./image/kubernetes/6.png)<br/>
```shell
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config

kubectl get nodes
```
![image](./image/kubernetes/3.png)<br/>

- 컨테이너 네트워크 설정
```shell
dnf -y install wget
wget https://docs.projectcalico.org/manifests/calico.yaml
vi calico.yaml  #4551 주석 제거하고 줄 맞추기
```
![image](./image/kubernetes/4.png)<br/>
![image](./image/kubernetes/5.png)<br/>

```shell
kubectl apply -f calico.yaml
```

### node 설정
- 방화벽 설정
```shell
firewall-cmd --zone=public --permanent --add-port={10250,30000-32767}/tcp
firewall-cmd --reload
```
- master와 연결
```shell
kubeadm join 192.168.197.100:6443 --token 5b2pjz.sf4632azhzpcp7f7 \
        --discovery-token-ca-cert-hash sha256:a624bb31c56ec6595a9c8adfe4a7ce5721aae18bd78150ac457bc6f5ca109b20  #사람마다 다름
```

### 확인(master)
- 컨테이너 확인
```shell
kubectl get pod -n kube-system  # 다 Running 뜨는지 확인
```
![image](./image/kubernetes/7.png)<br/>

- 노드 연결 확인
```shell
kubectl get nodes   # 다 Ready뜨는지 확인
```
![image](./image/kubernetes/8.png)<br/>

설정을 다 했으면 스냅샷을 남겨 백업해둔다.<br/>

