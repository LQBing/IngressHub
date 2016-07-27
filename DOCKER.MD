
docker compose need docker, and pip

# dependency
## install docker

there is some ways to install docker, official site page : [https://www.docker.com/products/docker/](https://www.docker.com/products/docker/)

## install pip

debian or ubuntu:

    sudo apt-get install -y python-pip

red hat or centos:

    sudo yum -y install epel-release
    sudo yum -y install python-pip git

windows:

for windows, python install package include pip

get python install .msi file from [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

## install docker-compose

    pip install docker-compose


# run docker compose file

save `docker-compose.yaml` and run

    docker-compose up -d

# services

## mysql

maybe you can run it with docker compose with blow docker-compose.yaml, define default password & .etc with node environment

    mysql:
        image: mysql:5.6
        volumes:
            - ./mysql:/var/lib/mysql
        ports:
            - 3306:3306
        environment:
            - MYSQL_ROOT_PASSWORD=fff
            - character-set-server=utf8mb4
            - collation-server=utf8mb4_unicode_ci
            - character_set_server=utf8mb4
            - character_set_client=utf8mb4
            - character_set_connection=utf8mb4
            - character_set_results=utf8mb4
            - character_set_system=utf8mb4

## rabbitmq

maybe you can run it with docker compose with blow docker-compose.yaml, define default user, password & .etc with node environment

    rabbitmq:
        image: rabbitmq:3-management
        hostname: rabbit-dev
        ports:
            - 15672:15672
            - 5672:5672
        environment:
            HOSTNAME: rabbit-dev
            RABBITMQ_NODENAME: rabbit-dev
            RABBITMQ_DEFAULT_USER: dev
            RABBITMQ_DEFAULT_PASS: fff
            RABBITMQ_LOG_BASE: /var/log/rabbitmq
        volumes:
            - ./rabbitmq/mnesia:/var/lib/rabbitmq/mnesia
            - ./rabbitmq/logs/:/var/log/rabbitmq/
