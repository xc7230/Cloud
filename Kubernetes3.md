# Helm
## Helm 설치 (master)
- 방화벽 해제
```shell
systemctl stop firewalld
systemctl disable firewalld
setenforce 0
```

- 파일 다운 및 설치
```shell
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
## Helm을 이용해서 모니터링 환경 구축
- 네임스페이스 생성
```shell
kubectl create namespace monitoring
```
- Helm 레토지토리 추가
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```
- 레포지토리 업데이트
```shell
helm repo update
```

- 프로메테우스 + 그라파나 설치
```shell
wget https://raw.githubusercontent.com/grafana/helm-charts/main/charts/grafana/values.yaml
helm install prometheus prometheus-community/kube-prometheus-stack -f "values.yaml" --namespace monitoring
```

- 설치확인


