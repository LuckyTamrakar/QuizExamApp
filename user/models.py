from email.policy import default
from logging import debug
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
class QuesModel(models.Model):
    
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")



class QuesModel1(models.Model):
    
    question1 = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question1
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
    email_verified = models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    
    def __str__(self):
        return str(self.phone_number)
class QuesModel2(models.Model):
    question2 = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question2
    
class QuesModel3(models.Model):
    question3 = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question3
    
class QuesModel4(models.Model):
    question4 = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question4
    
class QuesModel5(models.Model):
    question5 = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question5
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    address = models.CharField(max_length=500, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name


class Userdata(models.Model):
    user=models.CharField(max_length=255 ,default="")
    type=models.CharField(max_length=255,default="")
    correct=models.CharField(max_length=255,default="")
    wrong=models.CharField(max_length=255,default="")
    percent=models.CharField(max_length=255,default="")
    total=models.CharField(max_length=255,default="")
    def __str__(self):
        return self.user