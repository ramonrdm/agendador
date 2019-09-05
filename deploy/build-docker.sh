#!/usr/bin/bash
docker build -t agendador:1.2.0 ../.

docker tag ramonufsc/agendador:1.2.0 ramonufsc/agendador:latest

docker push ramonufsc/agendador:1.2.0

docker push ramonufsc/latest



# ./manage.py shell

# from django.contrib.auth.models import User, Group
 
# # Option 1
# group = Group.objects.get(name='group_name')
# users = group.user_set.all()
 
# # Option 2
# User.objects.filter(groups__name='group_name')

# emails = User.objects.filter(is_active=True, groups__name='responsables').exclude(email='').values_list('email', flat=True)