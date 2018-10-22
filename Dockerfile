FROM ubuntu:17.10
MAINTAINER ramon.rdm <ramon.rdm@ufsc.br>
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y apache2 libapache2-mod-wsgi \
	python-dev python-mysqldb python-pip && \
	apt-get clean

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

 
COPY deploy/agendador.conf /etc/apache2/sites-enabled/000-default.conf
RUN mkdir /var/www/html/agendador
WORKDIR /var/www/html/agendador
COPY . /var/www/html/agendador


#run pip install --upgrade setuptools

RUN pip install -r requirements.txt
RUN rm -r /var/www/html/agendador/static/
RUN python /var/www/html/agendador/manage.py collectstatic --noinput

RUN chmod -R 755 /var/www/html/agendador

EXPOSE 80
ENTRYPOINT service apache2 start && /bin/bash

#RUN python /var/www/html/agendador/manage.py migrate
#docker build -t ramonufsc/agendador:0.9.2