#!/usr/bin/env bash

export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
terraform init
terraform apply -auto-approve -lock=False
echo "Jenkins = http://$(terraform output -raw jenkins_vm_ip):8080"
