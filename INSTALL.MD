

# mysql & rabbitmq

install them with yum or apt-get or [docker](https://github.com/LQBing/IngressHub/blob/master/DOCKER.md)

# python

install python 2.7+ or python 3.4+ and git

install pip with

debian or ubuntu:

    sudo apt-get install -y python-pip git

red hat or centos:

    sudo yum -y install epel-release
    sudo yum -y install python-pip git


# mysql

PS: please create db with character set `utf8mb4`, or error will caused by emoji character in message.

install mysql as you want, maybe you can run it with docker compose with blow docker-compose.yaml, define init root password with `MYSQL_ROOT_PASSWORD`

    mysql:
        image: mysql:5.6
        volumes:
            - ./mysql:/var/lib/mysql
        ports:
            - 3306:3306
        environment:
            - MYSQL_ROOT_PASSWORD=Aa123456
            - character-set-server=utf8mb4
            - collation-server=utf8mb4_unicode_ci
            - character_set_server=utf8mb4
            - character_set_client=utf8mb4
            - character_set_connection=utf8mb4
            - character_set_results=utf8mb4
            - character_set_system=utf8mb4

# rabbitmq

# python package install

change direct to project folder

    pip install -r requirements.txt

# clone project

# celery worker & celery beat

change direct to project folder, run celery worker & celery beat system backend

    nohup python manage.py celery worker &
    nohup python manage.py celery baet &




