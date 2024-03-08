#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static folder

apt-get -y update
apt-get -y install nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello World" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Grant permissions to user and group
chown -R ubuntu /data/
chgrp -R ubuntu /data/

printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root   /etc/nginx/html;
    index  index.html index.htm;
    add_header X-Served-By \$hostname;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
    	root /etc/nginx/html;
	internal;
    }
}
" > /etc/nginx/sites-available/default

service nginx restart
