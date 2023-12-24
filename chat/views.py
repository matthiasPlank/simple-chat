
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import re

from chat.models import Message, Chat

# Create your views here.
@login_required(login_url='/login/')
def index(request): 
    print(request.method)
    if request.method == 'POST':
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'] , chat=myChat , author=request.user , receiver=request.user); 
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html' , {'messages':chatMessages})


def login_view(request): 
    redirect = request.GET.get('next')
    if request.method == 'POST':
        print("Received Data:" + request.POST['username'] + request.POST['password'])
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user: 
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else: 
            print("Wroing password")
            return render(request, 'auth/login.html', {'wrongPassword' : True , 'redirect':redirect})
    return render(request, 'auth/login.html',  {'redirect':redirect})


def register_view(request):

    if request.method == 'POST':
        print("Received Data:" + request.POST['email'] + request.POST['password'] + request.POST['confirmPassword'])
        if request.POST['password'] == request.POST['confirmPassword']:
            passwordCheck = True; 
        else:
            passwordCheck = False;
        if passwordCheck: 
            username = getUsernameFromEmail(request.POST['email'])
            user = User.objects.create_user(username, request.POST['email'], request.POST['password'])
            user.last_name = request.POST['lastName']; 
            user.first_name = request.POST['firstName']; 
            user.save()
            if user: 
                login(request, user)
                return HttpResponseRedirect("/chat/")
        else: 
            return render(request, 'auth/register.html', {'wrongPassword': not passwordCheck })
    return render(request, 'auth/register.html')




def getUsernameFromEmail(username): 
    subIndex = username.find('@')
    username = username[0:subIndex]; 
    username = re.sub('[\W_]+', '', username)
    return username