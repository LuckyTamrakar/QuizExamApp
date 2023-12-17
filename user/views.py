from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import QuesModel, QuesModel1
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
import random
from django.conf import settings
from django.contrib.auth.hashers import make_password
#################### index#######################################


def index(request):
	return render(request, 'user/index.html', {'title':'index'})
def About(request):
    return render(request, 'user/about.html', {'title':'about'})

########### register here #####################################
def Register(request):
    if request.method == "POST":
        fm = UserRegisterForm(request.POST)
        up = UserProfileForm(request.POST)
        if fm.is_valid() and up.is_valid():
            e = fm.cleaned_data['email']
            n = fm.cleaned_data['name']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password1']
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = up.cleaned_data['phone_number']
            request.session['number'] = p_number
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            message = f'your wecare Login otp is {otp}'
            send_mail(
                'Email Verification OTP',
                message,
                settings.EMAIL_HOST_USER,
                [e],
                fail_silently=False,
            )
            return redirect('/registration/otp/')

    else:
        fm = UserRegisterForm()
        up = UserProfileForm()
    context = {'fm': fm, 'up': up}
    return render(request, 'user/registration.html', context)


def otpRegistration(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        user = request.session['username']
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email')

        if int(u_otp) == otp:
            User.objects.create(
                username=user,
                email=email_address,
                password=hash_pwd
            )
            user_instance = User.objects.get(username=user)
            Profile.objects.create(
                user=user_instance, phone_number=p_number, email_verified=True
            )
            Userdata.objects.create(user=user_instance)

            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('email')
            request.session.delete('password')
            #request.session.delete('phone_number')

            messages.success(request, 'Registration Successfully Done !!')

            return redirect('/login/')

        else:
            messages.error(request, 'Wrong OTP')

    return render(request, 'user/email-verified.html')

################ login forms###################################################


def Login(request):

    if request.method == 'POST':

        # AuthenticationForm_can_also_be_used__
        
        username = request.POST['username']
        request.session['username']=username
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)

            messages.success(request, f' wecome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title': 'log in'})


# Create your views here.


def forget_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            uid = User.objects.get(email=email)
            url = f'http://127.0.0.1:8000/change-password/{uid.profile.uuid}'
            send_mail(
                'Reset Password',
                url,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('/forget-password/done/')
        else:
            messages.error(request, 'email address is not exist')
    return render(request, 'user/forget-password.html')


def change_password(request, uid):
    try:
        if Profile.objects.filter(uuid=uid).exists():
            if request.method == "POST":
                pass1 = 'password1' in request.POST and request.POST['password1']
                pass2 = 'password2' in request.POST and request.POST['password2']
                if pass1 == pass2:
                    p = Profile.objects.get(uuid=uid)
                    u = p.user
                    user = User.objects.get(username=u)
                    user.password = make_password(pass1)
                    user.save()
                    messages.success(
                        request, 'Password has been reset successfully')
                    return redirect('/login/')
                else:
                    return HttpResponse('Two Password did not match')

        else:
            return HttpResponse('Wrong URL')
    except:
        return HttpResponse('Wrong URL')
    return render(request, 'user/change-password.html')


def home(request):

    if request.method == 'POST':
        username = request.session.get('username')
        print(username)
        userdatas=Userdata.objects.get(user=username)
        
        #userdatas.user=username
        ###print(username)
        questions = QuesModel.objects.all()
        
        score = 0
        wrong = 0
        correct = 0
        total = 0
        i=0
        

        for q in questions:
            total += 1
            #userdatas.ques=q.question
            
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
                #userdatas.ans1=q.ans
                #userdatas.save()
            else:
                wrong += 1
        percent = score/(total*10) * 100
        userdatas.type="python"
        userdatas.correct=correct
        userdatas.wrong=wrong
        userdatas.total=total
        userdatas.percent=percent
        userdatas.save()
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'user/result.html', context)
    else:
        questions = QuesModel.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'user/home.html', context)


def ques1(request):
    if request.method == 'POST':

        questions = QuesModel1.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            
            if q.ans == request.POST.get(q.question1):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score/(total*10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'user/result.html', context)
    else:
        questions = QuesModel1.objects.all()
        context = {
            'question1': questions
        }
        return render(request, 'user/ques1.html', context)


def ques2(request):
    if request.method == 'POST':

        questions = QuesModel2.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            ##print(request.POST.get(q.question2))
            ##print(q.ans)
            ##print()
            if q.ans == request.POST.get(q.question2):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score/(total*10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'user/result.html', context)
    else:
        questions = QuesModel2.objects.all()
        context = {
            'question2': questions
        }
        return render(request, 'user/ques2.html', context)


def ques3(request):
    if request.method == 'POST':

        questions = QuesModel3.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            ##print(request.POST.get(q.question3))
            ##print(q.ans)
            ##print()
            if q.ans == request.POST.get(q.question3):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score/(total*10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'user/result.html', context)
    else:
        questions = QuesModel3.objects.all()
        context = {
            'question3': questions
        }
        return render(request, 'user/ques3.html', context)


def ques4(request):
    if request.method == 'POST':

        questions = QuesModel4.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            ##print(request.POST.get(q.question4))
            ##print(q.ans)
            ##print()
            if q.ans == request.POST.get(q.question4):
                score += 10
                correct += 1
            else:
                wrong += 1
        
        percent = score/(total*10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'user/result.html', context)
    else:
        questions = QuesModel4.objects.all()
        context = {
            'question4': questions
        }
        return render(request, 'user/ques4.html', context)


def ques5(request):
    if request.method == 'POST':

        questions = QuesModel5.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            ##print(request.POST.get(q.question5))
            ##print(q.ans)
            ##print()
            if q.ans == request.POST.get(q.question5):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score/(total*10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'user/result.html', context)
    else:
        questions = QuesModel5.objects.all()
        context = {
            'question5': questions
        }
        return render(request, 'user/ques5.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        contact = Contact(name=name, email=email, phone=phone,
                          desc=desc, address=address, city=city, state=state)
        contact.save()
    return render(request, 'user/contact.html')

def userdata(request):
    if request.method=='GET':
        
        username = request.session.get('username')
        #print(username)
        userdatas=Userdata.objects.get(user=username)
        #print(userdatas.type)
        context={
            'type':userdatas.type,
            'correct':userdatas.correct,
            'wrong':userdatas.wrong,
            'percent':userdatas.percent
        }
        
        
            #userdatas.user=data
            #userdatas.save()
        return render(request,'user/userdata.html',context)