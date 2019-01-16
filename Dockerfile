FROM ubuntu:17.10
MAINTAINER ramon.rdm <ramon.rdm@ufsc.br>
RUN apt-get update
RUN apt-get install -y apache2 libapache2-mod-wsgi python-mysqldb python-pip && apt-get clean

RUN pip install django==1.10.01

ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

RUN mkdir /var/www/html/agendador/
WORKDIR /var/www/html/agendador/

#COPY requirements.txt /var/www/html/agendador/
#RUN pip install -r requirements.txt

COPY deploy/agendador.conf /etc/apache2/sites-enabled/000-default.conf
COPY . /var/www/html/agendador
#RUN python /var/www/html/agendador/manage.py migrate
RUN chmod -R 755 /var/www/html/agendador

EXPOSE 80



# rm -r static/
#RUN python /var/www/html/agendador/manage.py collectstatic

ENTRYPOINT service apache2 start && /bin/bash
#CMD ["bash", "service apache2 start"]

#docker build -t ramonufsc/agendador:0.9.2