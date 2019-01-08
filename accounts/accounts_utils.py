from django.contrib.auth.models import User
from django.shortcuts import  render, redirect

def user_changed_password(user):
    password_changed = False if User.objects.filter(id=user.id).values('password_changed')[0]['password_changed']=='f' else True
    return password_changed

def check_permissions(request, user, permission, redirect=None, message=None):
    if(user.has_perm(permission)):
        return True
    else:
        False
        # return False
