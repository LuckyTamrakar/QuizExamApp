from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import CaptchaField

def email_exist(value):
    if User.objects.filter(email=value).exists():
        return forms.ValidationError("Profile with this Email Address already exists")
class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=17,validators=[phone_regex])
    
    
    class Meta:
        model = Profile
        fields = ['phone_number']

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(validators=[email_exist])
	phone_no = forms.CharField(max_length = 20)
	name = forms.CharField(max_length = 20)
	
	#enroll_no = forms.CharField(max_length = 20)
	captcha = CaptchaField()
	class Meta:
		model = User
		fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class createuserform(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','password'] 

class addQuestionform(ModelForm):
    class Meta:
        model=QuesModel
        fields="__all__"

