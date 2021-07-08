locals {
  ssh_user         = "ubuntu"
  private_key_path = "./TerraformAnsible/keys/ssh/id_rsa"
  public_key_path  = "./TerraformAnsible/keys/ssh/id_rsa.pub"
}

provider "aws" {
  region = "us-east-2"
}

resource "aws_key_pair" "jenkins" {
  key_name   = "devopsproject_jenkins_vm"
  public_key = file(local.public_key_path)
}

resource "aws_security_group" "jenkins_vm" {
  name   = "Jenkins VM security group"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
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

resource "aws_instance" "jenkins_vm" {
  ami                         = "ami-00399ec92321828f5"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.jenkins_vm.id]
  key_name                    = aws_key_pair.jenkins.key_name

  tags = {
    Name = "Jenkins VM"
  }

  provisioner "remote-exec" {
    inline = ["echo 'Wait until SSH is ready'"]

    connection {
      type        = "ssh"
      user        = local.ssh_user
      private_key = "${file(local.private_key_path)}"
      agent       = "false"
      host        = aws_instance.jenkins_vm.public_ip
    }
  }

  provisioner "local-exec" {
    command = "export ANSIBLE_HOST_KEY_CHECKING=False && ansible-playbook -u ${local.ssh_user} -i ${aws_instance.jenkins_vm.public_ip}, --private-key ${local.private_key_path} jenkins.yml"
  }
}

output "jenkins_vm_ip" {
  value = aws_instance.jenkins_vm.public_ip
}
