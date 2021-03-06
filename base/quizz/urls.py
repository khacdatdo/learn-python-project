"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.urls.conf import include
from . import views
from .api import urls as api_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('sign-up/', views.signup, name='sign-up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('api/', include(api_urls)),
    path('play/', views.play, name='play'),
    path('profile/',views.profile, name ='profile'),
    path('overview/',views.overview, name ='overview'),
    path('summary/<int:id>/',views.summary, name ='summary'),  
    path('rank/',views.rank, name ='rank'),
]
