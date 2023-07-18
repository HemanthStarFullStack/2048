"""
URL configuration for mygame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views


# print(auth_views.LoginView.as_view());

from mygame.controllers import home_page
from mygame.controllers import moveup


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('login/',),
    # path('logout/'),
     path('accounts/signup/', auth_views.FormView.as_view(
        template_name='registration/signup.html',
        form_class=UserCreationForm,
        success_url='/accounts/login/'
    ), name='signup'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

    path('', home_page.home_page,name = 'home_page'),
    
    path('moveup/',moveup.moveup,name='moveup')
]
