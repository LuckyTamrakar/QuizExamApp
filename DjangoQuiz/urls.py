"""DjangoQuiz URL Configuration

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
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth
from django.views.generic import TemplateView
urlpatterns = [
 
    path('admin/', admin.site.urls),
    path(r'captcha/', include('captcha.urls')),
    path('registration/otp/',user_view.otpRegistration, name="otp-Registration"),
    ##### user related path##########################
    path('', include('user.urls')),
    path('home/', user_view.home, name ='home'),
    path('ques1/', user_view.ques1, name ='ques1'),
    path('ques2/', user_view.ques2, name ='ques2'),
    path('ques3/', user_view.ques3, name ='ques3'),
    path('ques4/', user_view.ques4, name ='ques4'),
    path('ques5/', user_view.ques5, name ='ques5'),
    path('login/', user_view.Login, name ='login'),
   
    path('contact/', user_view.contact, name ='contact'),
    path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    path('register/', user_view.Register, name ='register'),
    path('forget-password/',user_view.forget_password,name="forger-password"),
    path('forget-password/done/',TemplateView.as_view(template_name='user/forget-password-done.html')),
    path('change-password/<slug:uid>/',user_view.change_password,name="change-password"),
    path('userdata/',user_view.userdata,name='user-data'),
    path('about/', user_view.About, name ='about'),
    
 
]