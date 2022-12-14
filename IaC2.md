# Tarraform
## 반복문
### count
```tf
resource "aws_instance" "app_server" {
  count = 3 # 내가 생성할 EC2 갯수
  ami           = var.app_server_ami
  instance_type = var.app_server_type
  vpc_security_group_ids = ["sg-04edad22127a399a2"]

  tags = {
    Name = "web_${count.index}"
  }
}
```
![image](./image/IaC2/1.png)<br/>

### for_each
- EC2
`variables.tf`
```tf
variable "server_name" {
  type = list(any)
  default = ["web_1", "web_2", "web_3"] 
}
```

`main.tf`
```tf
resource "aws_instance" "app_server" {
  ami           = var.app_server_ami
  instance_type = var.app_server_type
  vpc_security_group_ids = ["sg-04edad22127a399a2"]
  for_each = toset(var.server_name)
  tags = {
    Name = "${each.value}"
  }
}

 output "app_server_public_ip" {
  description = "aws instance public_ip"
  value = [for server in aws_instance.app_server : server.public_ip]
}

```
![image](./image/IaC2/2.png)<br/>

- security_group
`variables.tf`
```tf
variable "sg_list" {
  type = map
  default = {"ssh_sg":22, "web_sg":80, "was_sg":8000} 
}
```
`main.tf`
```tf
resource "aws_security_group" "ec2_allow_rule" {
  for_each = var.sg_list
  ingress {
    
    description = "sg"
    from_port   = each.value
    to_port     = each.value
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "${each.key}"
  }
}

 output "ec2_allow_rule" {
  description = "ec2_allow_rule_ip"
  value = [for sg in aws_security_group.ec2_allow_rule : sg.id]
}
```
![image](./image/IaC2/3.png)<br/>

- security_group 한곳에 여러 규칙 집어넣기
`variables.tf`
```tf
variable "ec2_ingress_ports_default" {
  description = "Allowed Ec2 ports"
  type        = map
  default     = {
    "22"  = ["192.168.1.0/24"]
    "443" = ["0.0.0.0/0"]
  }
}
```
`main.tf`
```tf
resource "aws_security_group" "ec2_allow_rule" {
  dynamic ingress {
    for_each = var.ec2_ingress_ports_default
    content {
      from_port   = ingress.key
      to_port     = ingress.key
      cidr_blocks = ingress.value
      protocol    = "tcp"
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "ec2_allow_rule"
  }
}
output "ec2_allow_rule" {
  description = "ec2_allow_rule_id"
  value = aws_security_group.ec2_allow_rule.id
}
```
![image](./image/IaC2/4.png)<br/>

### 실습
- vpc 생성 : a, c 가용 영역에 각 서브넷 생성
  - ssh_sg : 0.0.0.0/0에 대해 22번 포트 허용
  - web_sg : 0.0.0.0/0에 대해 80, 443 허용
  - was_sg : a, c 가용영역에 대해 8080, 8009
- ec2 생성
  - web : ssh_sg, web_sg
  - was : ssh_sg, was_sg


1. VPC 및 네트워크 생성 및 설정
- vpc 생성
`vpc.tf`
```tf
resource "aws_vpc" "my-vpc2" {
  cidr_block       = "200.200.0.0/16"
  instance_tenancy = "default"
  enable_dns_hostnames = true #DNS 호스트 네임 활성화
  tags = {
    Name = "my-vpc2"
  }
}
```
- 서브넷 생성<br/>
`vpc_variables.tf`
```tf
variable "subnet_name" {
  type        = map
  default     = {
    "a" : "200.200.10.0/24"
    "c" : "200.200.30.0/24"
  }
}
```
`vpc.tf`
```tf
resource "aws_subnet" "my2-subnet-1" {
  for_each = var.subnet_name
  vpc_id     = aws_vpc.my-vpc2.id
  cidr_block = each.value
  availability_zone = "ap-northeast-2${each.key}"
  map_public_ip_on_launch = true
  tags = {
    Name = "my-subnet-${each.key}"
  }
}
```

- 게이트웨이, 라우팅테이블 생성<br/>
`vpc.tf`
```tf
resource "aws_internet_gateway" "my-gw2" {
  vpc_id = aws_vpc.my-vpc2.id


  tags = {
    Name = "my-gw2"
  }
}

## 라우팅 테이블 연결
resource "aws_default_route_table" "my2-route-table" {
  default_route_table_id = aws_vpc.my-vpc2.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my-gw2.id # 게이트웨이와 연결
  }

  tags = {
    Name = "my2-route-table"
  }
}
```

2. 보안그룹 생성<br/>
`sc_variables.tf`
```tf
variable "ec2_ingress_ports_default" {
  description = "Allowed Ec2 ports"
  type        = map
  default     = {
    "ssh_sg"  = {"22": ["0.0.0.0/0"]},
    "web_sg"  = {"80": ["0.0.0.0/0"], "443": ["0.0.0.0/0"]},
    "was_sg"  = {"8080":["200.200.10.0/24", "200.200.20.0/24"], "8009":["200.200.10.0/24", "200.200.20.0/24"]}
  }
}
```
`sc.tf`
```tf
resource "aws_security_group" "ec2_allow_rule2" {
    vpc_id      = aws_vpc.my-vpc2.id
    for_each = var.ec2_ingress_ports_default
  dynamic ingress {
    for_each = each.value
    content {
        description = "${each.key}"
        from_port   = ingress.key
        to_port     = ingress.key
        protocol    = "tcp"
        cidr_blocks = ingress.value
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${each.key}"
  }  
}
```

3. EC2 생성<br/>
`variables.tf`
```tf
variable "app_server_ami" {
  type = string
  default = "ami-068a0feb96796b48d"  
}

variable "app_server_type" {
  type = string
  default = "t2.micro"  
}

variable "my_ec2_keyname" {
  type = string
  default = "cloudcamp"
}
```

`main.tf`
```tf
resource "aws_instance" "app_server2" {
  for_each = toset(var.app_list)
  ami           = var.app_server_ami
  instance_type = var.app_server_type
  vpc_security_group_ids = [for sg in aws_security_group.ec2_allow_rule2: sg.id]
  subnet_id = aws_subnet.my2-subnet-1["a"].id  # 서브넷 연결
  key_name = var.my_ec2_keyname  # key 추가
  tags = {
    Name = "${each.value}"
  }
}
```
## 조건문
`main.tf`
```tf
provider "aws" {
  region  = "ap-northeast-2"
}

# 조건을 준다.
variable "create_ec2" {
  type = bool
  default = true
}

resource "aws_instance" "app_server" {
  count = var.create_ec2 ? 1 : 0  # 삼항연산자 추가
  ami           = "ami-068a0feb96796b48d"
  instance_type = "t2.micro"
  key_name = "cloudcamp"

  tags = {
    Name = "server"
  }
}
```

```shell
terraform apply -var create_ec2=true  # ec2가 생성된다.
terraform apply -var create_ec2=false # ec2가 삭제된다.
```

- 추가 명령어를 입력하면 다른 OS의 EC2가 생성되게 하기<br/>
`main.tf`
```shell
variable "ami" {
    type = string
    default = "ubuntu"  
}

resource "aws_instance" "app_server" {
  count = var.create_ec2 ? 1 : 0
  ami           = var.ami == "ubuntu" ? "ami-0e9bfdb247cc8de84":"ami-09cf633fe86e51bf0"   # ubuntu를 입력하면 우분투 이미지 아이디가 출력되고 아니면 아마존 이미지가 출력되서 EC2를 생산한다.
  instance_type = "t2.micro"
  key_name = "cloudcamp"

  tags = {
    Name = "server"
  }
}

```
```shell
terraform apply -var ami=ubuntu # 우분투 이미지 생성
terraform apply -var ami=아무거나 # 아마존 이미지 생성
```

### 조건문으로 실습<br/>
방금전 반복문 실습에서 생성하던 EC2 보안그륩을 `was` 는 `ssg_sg`, `was_sg` 만 연결, `web`은 `ssg_sg`, `web_sg`만 연결해준다.<br/>

`main.tf`
```tf
resource "aws_instance" "app_server2" {
  for_each = toset(var.app_list)
  ami           = var.app_server_ami
  instance_type = var.app_server_type
  vpc_security_group_ids = each.value == "web" ? [aws_security_group.ec2_allow_rule2["ssh_sg"].id, aws_security_group.ec2_allow_rule2["web_sg"].id] : [aws_security_group.ec2_allow_rule2["ssh_sg"].id, aws_security_group.ec2_allow_rule2["was_sg"].id]  # 조건추가
  subnet_id = aws_subnet.my2-subnet-1["a"].id  # 서브넷 연결
  key_name = var.my_ec2_keyname  # key 추가
  tags = {
    Name = "${each.value}"
  }
}