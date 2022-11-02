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
