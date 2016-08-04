FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		libmysqlclient-dev \
		libpq-dev \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

RUN pip install supervisor

EXPOSE 8000
COPY supervisor.conf /etc/supervisord.conf

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD ["supervisord"]