from django.shortcuts import render, redirect
from django.contrib import auth

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
