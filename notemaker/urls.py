"""notemaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

import noteapp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',noteapp.views.index,name='index_url'),# home page
    # cancelled view
    # path('login_signup/',noteapp.views.login_signup,name='login_signup_url'),#both login_signup input data

    path('signup/',noteapp.views.signup,name='signup_url'),# signup logic
    path('login/',noteapp.views.loginpage,name='login_url'), # login logic
    path('logout/',noteapp.views.logoutpage,name='logout_url'), # logout logic
    path('update/<int:pk>',noteapp.views.update,name='update_url'), # update logic
    path('delete/<int:pk>',noteapp.views.delete,name='delete_url'), # delete logic
    path('userdashboard/',noteapp.views.user_dashboard,name='userdashboard_url'), # user dashboard logic
]
