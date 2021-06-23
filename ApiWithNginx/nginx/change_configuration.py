import sys
import os

if len(sys.argv) < 3:
    print("Invalid count arguments.")
    exit(0)

PATH_TO_TEMPLATE_NGINX_CONF = "/opt/ApiWithNginx/nginx/nginx.conf.template"
PATH_TO_NGINX_CONF_LOCAL = "/opt/ApiWithNginx/nginx/nginx.conf"

with open(PATH_TO_TEMPLATE_NGINX_CONF,'r') as f:
    text_file = f.read()

text_file = text_file.replace(
    '${WEIGHT_API_WITHOUT_JSON}', sys.argv[1]
).replace(
    '${WEIGHT_API_WITH_JSON}', sys.argv[2]
)

with open(PATH_TO_NGINX_CONF_LOCAL,'w') as f:
    f.write(text_file)
