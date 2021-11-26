from django.http import response
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import User
import random
import os
from twilio.rest import Client
import requests

import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

configuration = clicksend_client.Configuration()
configuration.username = 'lokendra.singh@indianacademyofrobotics.com'
configuration.password = 'CE988987-6F5E-79C1-DF73-B3DD22CF4589'

def index(request):
    if request.method=='POST':
        username=request.POST.get('username')
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')

        check_user = User.objects.filter(email = email).first()

        otp=str(random.randint(1000,9999))
        user=User(email=email,first_name=name,username=username,otp=otp,phone_number=phone,password=password)
        user.save()
        
        
        api_key='be15db33-4aab-11ec-b710-0200cd936042'
        try:
            url=f"https://2factor.in/API/V1/{api_key}/SMS/+91{phone}/{otp}"
            response=requests.get(url)
            
        except:
            HttpResponse("Unable to send Msg please check Internet Connection or Try agian Later")

        print(url)
        request.session['phone'] = phone
        return redirect('otp')
    return render(request,'index.html')
#return render(request,'index.html')S

def otp(request):
    if request.method=='POST':
        OTP=request.POST.get('otp')
        phone=request.session['phone']
        user=User.objects.filter(phone_number=phone).first()
        if OTP is not None:
            if OTP==user.otp:
                user.is_phone_verified = True
                user.save()
                return HttpResponse("profile created")
            else:
                return HttpResponse("wrong")
    return render(request,'otp.html')


def login(request):
    if request.method == 'POST':
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        try:
            user=User.objects.get(phone_number=phone)
            if user.is_phone_verified == True:
                if user.phone_number == phone and user.password == password:
                    return HttpResponse("you are loged In !")
                return HttpResponse("Phone Number Or password wrong")
            return HttpResponse("please Verify Phone or  Create Id")
        except:
            return HttpResponse("please Sign Up first")
    return render(request,'login.html')