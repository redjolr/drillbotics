from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User, Group, Permission
from django.template.defaulttags import register
from django.http import HttpResponse
from django.http import Http404
from enum import Enum
import json
@register.filter
def get_item(dictionary, key):

    if key in dictionary:
        return dictionary[key]

def login(request):
    if request.user.is_authenticated and request.user.id is not None:
        return redirect('home')
    if request.method=='POST':

        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error':'Username or password is incorrect!'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')

def allgroups(request):
    groups = Group.objects.all()
    user_count = {}
    for group in groups:
        nr_users = len(User.objects.filter(groups = group))
        user_count[group] = nr_users
    return render(request, 'accounts/groups.html', {'groups':groups, 'user_count':user_count})


def group(request, id):
    group = Group.objects.get(id=id)

    if request.method=="POST":
        if(request.POST["name"]=="" or request.POST["description"]=="" or request.POST["permissions"]==""):

            raise Http404
        group.name = request.POST['name']
        group.description = request.POST['description']
        group.save()
        group.permissions.clear()
        new_permissions = json.loads(request.POST['permissions'])
        for permission in new_permissions:
            permission = Permission.objects.get(id=permission['id'])
            group.permissions.add(permission)
        return redirect( 'allgroups')
    elif request.method=="GET":
        permissions = json.dumps(list(group.permissions.values('id', 'name')))
        return render(request, 'accounts/group.html', {'group':group, 'permissions':permissions})

def addgroup(request):
    if request.method=="POST":
        if(request.POST["name"]=="" or request.POST["description"]=="" or request.POST["permissions"]==""):
            raise Http404
        group = Group()
        group.name = request.POST['name']
        group.description = request.POST['description']
        group.save()
        permissions = json.loads(request.POST['permissions'])
        for permission in permissions:
            permission = Permission.objects.get(id=permission['id'])
            group.permissions.add(permission)
        return redirect( 'allgroups')
    elif request.method=="GET":
        return render(request, 'accounts/addgroup.html')


def delete_group(request, id):
    group = Group.objects.get(id=id)
    #group.permissions.clear()
    group.delete()
    return HttpResponse('deleted')



def get_permissions(request):
    permission_ids = list(range(1,9)) + list(range(21, 25)) + list(range(29,37))  #Database ids on table auth_permissions
    permissions = list(Permission.objects.filter(id__in=permission_ids).values('id', 'name'))

    return HttpResponse(json.dumps(permissions))


def allusers(request):
    users = User.objects.all()

    if 'view' not in request.GET or request.GET['view']=='list':
        return render(request, 'accounts/users/allusers_list.html', {'users':users})
    elif request.GET['view']=='tabular':
        return render(request, 'accounts/users/allusers_tabular.html', {'users':users})

def adduser(request):


    if request.method=="POST":
        pass
    #     if(request.POST["name"]=="" or request.POST["description"]=="" or request.POST["permissions"]==""):
    #
    #         raise Http404
    #     group.name = request.POST['name']
    #     group.description = request.POST['description']
    #     group.save()
    #     group.permissions.clear()
    #     new_permissions = json.loads(request.POST['permissions'])
    #     for permission in new_permissions:
    #         permission = Permission.objects.get(id=permission['id'])
    #         group.permissions.add(permission)
    #     return redirect( 'allgroups')
    elif request.method=="GET":

        return render(request, 'accounts/users/adduser.html')
