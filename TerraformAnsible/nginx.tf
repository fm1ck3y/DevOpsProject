locals {
  ssh_user         = "ubuntu"
  private_key_path = "/opt/TerraformAnsible/keys/ssh/id_rsa"
  public_key_path  = "/opt/TerraformAnsible/keys/ssh/id_rsa.pub"
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_key_pair" "main_vm" {
  key_name   = "devopsproject_main_vm"
  public_key = file(local.public_key_path)
}


resource "aws_security_group" "main_vm" {
  name   = "Main VM security group"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5003
    to_port     = 5003
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "main_vm" {
  ami                         = "ami-00399ec92321828f5"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.main_vm.id]
  key_name                    = aws_key_pair.main_vm.key_name

  tags = {
    Name = "Nginx/Postgresql VM"
  }

  provisioner "remote-exec" {
    inline = ["echo 'Wait until SSH is ready'"]

    connection {
      type        = "ssh"
      user        = local.ssh_user
      private_key = "${file(local.private_key_path)}"
      agent       = "false"
      host        = aws_instance.main_vm.public_ip
    }
  }

  provisioner "local-exec" {
    command = "export ANSIBLE_HOST_KEY_CHECKING=False && ansible-playbook -u ${local.ssh_user} -i ${aws_instance.main_vm.public_ip}, --private-key ${local.private_key_path} /opt/TerraformAnsible/postgresql_nginx_docker.yml"
  }

  provisioner "local-exec" {
    command = "python3 /opt/TerraformAnsible/change_ip_node.py ${aws_instance.main_vm.public_ip}"
  }
}

output "main_vm_ip" {
  value = aws_instance.main_vm.public_ip
}
