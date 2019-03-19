"""drillbotics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .import settings
import accounts.views
import dashboard.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard.views.home, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('sensors/', include('sensors.urls')),
    path('experiments/', include('experiments.urls')),
    path('rocks/', include('rocks.urls')),
    path('groups/', include('accounts.groups_urls')),
    path('users/', include('accounts.users_urls')),
    path('login/', accounts.views.login, name='login' ),
    path('logout/', accounts.views.logout, name='logout' ),
    path('profile/<int:id>', accounts.views.profile, name='profile' ),
    path('first_login_password/', accounts.views.first_login_password, name='first_login_password' ),
    path('update_profile/', accounts.views.update_profile, name='update_profile' ),

    path('api/', include('api.urls')),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
