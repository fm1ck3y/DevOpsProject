import sys
import os

if len(sys.argv) < 2:
    print("Invalid count arguments.")
    exit(0)

PATH_TO_TEMPLATE_CONF = "/opt/TerraformAnsible/aws-agent.xml.template"
PATH_TO_NODE = "/var/lib/jenkins/nodes/AWS-Agent/config.xml"

with open(PATH_TO_TEMPLATE_CONF,'r') as f:
    text_file = f.read()

text_file = text_file.replace('${HOST_IP}', sys.argv[1])

with open(PATH_TO_NODE,'w') as f:
    f.write(text_file)
