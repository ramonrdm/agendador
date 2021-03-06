Agendador
=========

Agendador de espaço físico

+ Cria espaço físico para agendamento de horário.
+ Interface simples de uma agenda por Mês e em cada dia mostra as reservas
+ Permite o usuário logado agendar uma reserva pela agenda.
    + Verifica choque de horário com outras reservas no mesmo espaço físico.
    + Envia e-mail avisando do sucesso da Reserva.
+ Interface Admin para controle das reservas, usuários, grupos, Tipos de eventos e espaços físocos.

 + Apache + Modulo python 
 + Django 
 + Django-cas-ng
     Integração com o CAS-UFSC, ou seja, utiliza o IdUFSC para login.
 + Django-material:
    https://github.com/viewflow/django-material/

Reponsavel Ramon Dutra Miranda

Executando projeto via docker-compose:
```
$ docker-compose -f deploy/docker-compose.debug.yml up
```

Executando o projeto localmente:
+ Instale a virtualenv, execute:
```
    $ pip install virtualenv
```
+ Crie uma localenv
```
    $ mkdir my_project_env
    $ cd my_project_env
    $ virtualenv -p /usr/bin/python2.7 my_project
    $ source my_project/bin/activate
    $ cd my_project
```
+ se não conseguir criar a virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/
+ Criada a virtualenv, execute para instalar dependências:
```
    $ pip install -r requirements.txt
```
+ Faça o download do projeto executando:
```
    $ git clone https://github.com/ramonrdm/agendador
```
+ Execute:
```
    $ cd agendador
```
+ Execute: 
```
    $ python manage.py makemigrations
    $ python manage.py migrate
```
+ Por fim, execute:
```
    $ python manage.py loaddata auth.json
    $ python manage.py loaddata agenda.json
```
