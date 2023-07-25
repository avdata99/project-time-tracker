# Simple deploy

This notes are to deploy this as simple as possible.  

## Clone the repository

```
git clone git@github.com:avdata99/project-time-tracker.git
```

## Install nginx

Install Nginx

```bash
sudo apt install nginx
```

Create your nginx conf file. Usually at `/etc/nginx/sites-available/your-domain.com`.  
Do enable it alreadt.  

```
server {
    server_name your-domain.com;
    
    client_max_body_size 20M;
    
    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_http_version 1.1;
    gzip_proxied any;
    gzip_min_length 1000;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;

    access_log /var/log/nginx/ptt-access.log;
    error_log /var/log/nginx/ptt-error.log;

    client_body_timeout 30;
    client_header_timeout 30;

    location /static {
        limit_conn addr 256;
        access_log off;
        alias /your/app/folder/static;
    }

    location /media {
        limit_conn addr 256;
        access_log off;
        alias /your/app/folder/media;
    }

    location / {

        proxy_connect_timeout 30;
        proxy_send_timeout 30;
        proxy_read_timeout 30;

        proxy_pass http://localhost:8142;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $http_x_forwarded_proto;
	    proxy_set_header Range $http_range;
        proxy_set_header If-Range $http_if_range;
	    proxy_set_header REMOTE_ADDR $remote_addr; 

    }

    listen 80;

}
```

This will be updated by Certbot later.  

## Create a virtual environment

Create a Python 3.10 virtual environment

```bash
python3 -m venv /some/path/pttenv
# activate it
source /some/path/pttenv/bin/activate
# Install reqs
cd project-time-tracker
pip install -r dev/requirements.txt
```

## Install gunicorn

Install gunicorn

```bash
pip install gunicorn
```
Create the file `/etc/gunicorn/ptt.conf.py` with the following content:

```python
import multiprocessing

bind = '127.0.0.1:8142'
workers = multiprocessing.cpu_count() * 2
```

## Install supervisor

Install supervisor

```bash
sudo apt install supervisor
```

Create a supervisor config file at `/etc/supervisor/conf.d/ptt.conf`

```bash
[program:ptt]
command=/some/path/pttenv/bin/gunicorn ptt.wsgi -c /etc/gunicorn/ptt.conf.py --timeout 30
directory=/your/app/folder/ptt
user=some-user
autostart=true
autorestart=true
stdout_logfile=/var/log/ptt-supervisor.log
stderr_logfile=/var/log/ptt-supervisor.err.log
``` 

Add this new supervidor process

```
sudo supervisorctl reread
sudo supervisorctl update
```

# Finish nginx settings

Enable the nginx conf file

```
ln -s /etc/nginx/sites-available/your-domain.com /etc/nginx/sites-enabled/your-domain.com
```

Reload nginx

```
sudo service nginx reload
# test new settings
sudo nginx -t
```

# Prepare the Django app

Create the custom settings file at /your/app/folder/ptt/ptt/local_settings.py

```
DEBUG = False
SECRET_KEY = "XXXXXXXXXXXXXXXXXXXxx"
ALLOWED_HOSTS = ["your-domain.com"]
CSRF_TRUSTED_ORIGINS = ['your-domain.com']
```

Prepare and restart the app

```
python manage.py collectstatic
# prepare your custom database and ...
python manage.py migrate
python manage createsuperuser
# Restart the app to read the new custom settings
sudo supervisorctl restart ptt
```

Add

```
sudo certbot --nginx
```