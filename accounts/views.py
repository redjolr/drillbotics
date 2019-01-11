from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.password_validation  import validate_password
from django.core.exceptions import ValidationError
from .models import   Occupation, Specialization
from django.template.defaulttags import register
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .accounts_utils import user_changed_password
from enum import Enum
import json



@register.filter
def get_item(dictionary, key):
    if key in dictionary:
        return dictionary[key]

def login(request):
    if request.method=='GET':
        if request.user.is_authenticated and request.user.id is not None:
            auth.login(request, request.user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html')
    if request.method=='POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            password_changed = False if User.objects.filter(id=user.id).values('password_changed')[0]['password_changed']=='f' else True
            if password_changed==False:
                auth.login(request, user)
                return redirect('/first_login_password/') #+str(user.id)  )
            else:
                auth.login(request, user)
                if 'remember-me' not in request.POST:
                    request.session.set_expiry(0) #Value 0 means that the session expires at browser close
                return redirect('home')

        else:
            return render(request, 'accounts/login.html', {'error':'Username or password is incorrect!'})



@login_required(login_url='/login/')
def first_login_password(request):
    user = User.objects.get(id=request.user.id)
    invalid_password_messages = None

    if request.method=='GET':
        password_changed = False if User.objects.filter(id=user.id).values('password_changed')[0]['password_changed']=='f' else True
        if password_changed:
            return redirect('home')
        else:
            return render(request, 'accounts/first_login.html', {'user':user})
    if request.method=='POST':
        if request.POST['password1']=="" or request.POST['password2']=="":
            return render(request, 'accounts/first_login.html', {'user':user, 'missing_password':True})
        elif request.POST['password1'] != request.POST['password2']:
            return render(request, 'accounts/first_login.html', {'user':user, 'passwords_dont_match':True})
        try:
            validate_password(request.POST["password1"], user=user)
        except ValidationError as error:
            invalid_password_messages = list(error)

        if invalid_password_messages is not None:
            return render(request, 'accounts/first_login.html', {'user':user, 'invalid_password_messages':invalid_password_messages})
        user.set_password(request.POST['password1'])
        user.password_changed = 't'
        user.save()
        auth.login(request, user)
        return redirect('home')

@login_required(login_url='/login/')
def change_password(request):
    user = request.user
    invalid_password_messages = None

    if request.method=='POST':

        if request.POST['password1']=="" or request.POST['password2']=="" or request.POST['current_password']=="":
            return HttpResponse("passwords_missing")
        elif request.POST['password1'] != request.POST['password2']:
            return HttpResponse("passwords_dont_match")
        if user.check_password(request.POST['current_password'])==False:
            return HttpResponse("wrong_current_password")
        try:
            validate_password(request.POST["password1"], user=user)
        except ValidationError as error:
            invalid_password_messages = json.dumps(list(error))
        if invalid_password_messages is not None:
            return HttpResponse(invalid_password_messages)
        user.set_password(request.POST['password1'])
        user.save()
        user = auth.authenticate(username=user.username, password=request.POST['password1'])
        auth.login(request, user)
        return HttpResponse('success')




def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')




@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('auth.view_group', login_url='home')
def allgroups(request):
    groups = Group.objects.all()
    user_count = {}
    for group in groups:
        nr_users = len(User.objects.filter(groups = group))
        user_count[group] = nr_users

    return render(request, 'accounts/groups.html', {'groups':groups, 'user_count':user_count})


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def group(request, id):
    group = Group.objects.get(id=id)

    if request.method=="POST":
        if request.user.has_perm('auth.change_group')==False:
            return redirect('allgroups')
        if(request.POST["name"]=="" or request.POST["description"]=="" or request.POST["permissions"]==""):
            return HttpResponse(status=500)
        group.name = request.POST['name']
        group.description = request.POST['description']
        group.save()
        group.permissions.clear()
        new_permissions = json.loads(request.POST['permissions'])
        for permission in new_permissions:
            permission = Permission.objects.get(id=permission['id'])
            group.permissions.add(permission)
        return redirect( '/groups/'+str(id)+"?update_successful=True")
    elif request.method=="GET":
        if request.user.has_perm('auth.view_group')==False:
            return redirect('home')
        permissions = json.dumps(list(group.permissions.values('id', 'name')))
        if 'update_successful' in request.GET and request.GET['update_successful']=='True':
            return render(request, 'accounts/group.html', {'group':group, 'permissions':permissions, 'update_successful':True})
        else:
            return render(request, 'accounts/group.html', {'group':group, 'permissions':permissions})

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('auth.add_group', login_url='allgroups')
def addgroup(request):
    if request.method=="POST":
        if(request.POST["name"]=="" or request.POST["description"]=="" or request.POST["permissions"]==""):
            return HttpResponse(status=500)
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

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('auth.delete_group')
def delete_group(request, id):
    group = Group.objects.get(id=id)
    nr_of_users = len(User.objects.filter(groups=group).values())
    if nr_of_users>0:
        return HttpResponse('group has users')
    else:
        group.delete()
        return HttpResponse('deleted')


@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def get_permissions(request):
    perm_codenames = ['add_material', 'view_rock', 'add_rock', 'change_rock', 'delete_rock', 'view_sensor', 'add_sensor', 'change_sensor', 'delete_sensor',
                      'view_user', 'add_user','change_user','delete_user', 'add_group', 'view_group','change_group','delete_group']
    permissions = list(Permission.objects.filter(codename__in=perm_codenames).values('id', 'name'))
    return HttpResponse(json.dumps(permissions))

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('auth.view_user', login_url='home')
def allusers(request):
    users = User.objects.all()
    if 'view' not in request.GET or request.GET['view']=='list':
        return render(request, 'accounts/users/allusers_list.html', {'users':users})
    elif request.GET['view']=='tabular':
        return render(request, 'accounts/users/allusers_tabular.html', {'users':users})



@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
@permission_required('auth.add_user', login_url='allusers')
def adduser(request):
    if request.method=="POST":
        invalid_password_messages = None
        if request.POST["username"]=="" or request.POST["password1"]=="" or request.POST["password2"]=="" or request.POST["groups"]=="" or request.POST["first_name"]=="" or request.POST["last_name"]=="":
            return HttpResponse(status=500)
        if request.POST["password1"]!=request.POST["password2"]:
            return HttpResponse(status=500)
        username_exists = User.objects.filter(username=request.POST['username']).exists()

        user = User()
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        occupations = Occupation.objects.all()
        specializations = Specialization.objects.all()
        user.set_password(request.POST['password1'])
        if 'occupation' in request.POST:
            user.occupation = Occupation.objects.get(id=request.POST['occupation'])
        if 'specialization' in request.POST:
            user.specialization = Specialization.objects.get(id=request.POST['specialization'])
        try:
            validate_password(request.POST["password1"], user=user)
        except ValidationError as error:
            invalid_password_messages = list(error)

        if username_exists or invalid_password_messages:
            return render(request, 'accounts/users/adduser.html', {'occupations': occupations, 'specializations':specializations,
                                                                   'form_filled_data':request.POST, 'invalid_password_messages':invalid_password_messages,
                                                                   'username_exists':username_exists})
        user.save()
        groups = json.loads(request.POST['groups'])
        for group in groups:
            group = Group.objects.get(name=group['name'])
            user.groups.add(group)
        return redirect( 'allusers')
    elif request.method=="GET":
        occupations = Occupation.objects.all()
        specializations = Specialization.objects.all()
        return render(request, 'accounts/users/adduser.html', {'occupations': occupations, 'specializations':specializations})

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def profile(request, id):
    user = User.objects.get(id=id)
    # occupation = Occupation.objects.get(id=user.occupation.id)
    # print(occupation)
    groups = list( user.groups.all())
    group_permissions = {}
    for group in groups:
        permissions = group.permissions.values('name')
        group_permissions[group.name]= permissions
    if(id==request.user.id):
        occupations = Occupation.objects.all()
        specializations = Specialization.objects.all()
        return render(request, 'accounts/profile.html', {'user':user, 'group_permissions':group_permissions, 'own_profile':True, 'occupations': occupations, 'specializations':specializations})
    else:
        return render(request, 'accounts/profile.html', {'user':user, 'group_permissions':group_permissions})

def update_profile(request):
    user = request.user
    if request.method=="POST":
        if  request.POST["first_name"]=="" or request.POST["last_name"]=="":
            return HttpResponse("missing_field")
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        if 'birthday' in request.POST:
            user.birthday = request.POST["birthday"]
        if 'email' in request.POST:
            user.email = request.POST["email"]
        if 'occupation' in request.POST:
            user.occupation = Occupation.objects.get(id=request.POST['occupation'])
        if 'specialization' in request.POST:
            user.specialization = Specialization.objects.get(id=request.POST['specialization'])

        if len(request.FILES)!=0:
            print("YOYOYO")
            user.picture = request.FILES['picture']
        user.save()
        return redirect("/profile/"+str(request.user.id))



@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def user(request, id):
    user = User.objects.get(id=id)
    if request.method=="POST":
        if request.user.has_perm('auth.change_user')==False:
            return redirect('allusers')
        invalid_password_messages = None
        if request.POST["username"]==""  or request.POST["groups"]=="" or request.POST["first_name"]=="" or request.POST["last_name"]=="":
            return HttpResponse(status=500)
        if request.POST["password1"]!=request.POST["password2"]:
            return HttpResponse(status=500)

        username_exists = True if User.objects.get(username=request.POST['username'])!=None and User.objects.get(username=request.POST['username'])!=user  else False

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        occupations = Occupation.objects.all()
        specializations = Specialization.objects.all()

        if 'occupation' in request.POST:
            user.occupation = Occupation.objects.get(id=request.POST['occupation'])
        if 'specialization' in request.POST:
            user.specialization = Specialization.objects.get(id=request.POST['specialization'])

        if request.POST['password1']!="":
            try:
                validate_password(request.POST["password1"], user=user)
                user.set_password(request.POST['password1'])
            except ValidationError as error:
                invalid_password_messages = list(error)

        if username_exists or invalid_password_messages:
            return render(request, 'accounts/users/user.html', {'existing_user':user, 'occupations': occupations, 'specializations':specializations,
                                                                   'form_filled_data':request.POST, 'invalid_password_messages':invalid_password_messages,
                                                                   'username_exists':username_exists, 'updating_user':True})
        user.save()
        user.groups.clear()
        groups = json.loads(request.POST['groups'])
        for group in groups:
            group = Group.objects.get(name=group['name'])
            user.groups.add(group)
        return redirect('/users/'+str(id)+"?update_successful=True")

    if request.method=="GET":
        if request.user.has_perm('auth.view_user')==False:
            return redirect('home')
        occupations = Occupation.objects.all()
        specializations = Specialization.objects.all()
        groups_json = json.dumps(list(user.groups.values('id', 'name')))
        occupation = None if user.occupation is None else str(user.occupation.id)
        specialization = None if user.specialization is None else str(user.specialization.id)
        form_filled_data = {'first_name':user.first_name, 'last_name':user.last_name, 'username':user.username, 'email':user.email,
                            'occupation': occupation, 'specialization':specialization, 'groups':groups_json}
        if 'update_successful' in request.GET and request.GET['update_successful']=='True':
            return render(request, 'accounts/users/user.html', {'existing_user':user,'occupations': occupations, 'specializations':specializations,
                                                               'form_filled_data':form_filled_data, 'updating_user':True, 'update_successful':True})
        else:
            return render(request, 'accounts/users/user.html', {'existing_user':user,'occupations': occupations, 'specializations':specializations,
                                                                'form_filled_data':form_filled_data, 'updating_user':True})

@login_required(login_url='/login/')
@user_passes_test(user_changed_password, login_url='/first_login_password/')
def get_groups(request):
    groups = json.dumps(list(Group.objects.values('id', 'name')))
    return HttpResponse(groups)
