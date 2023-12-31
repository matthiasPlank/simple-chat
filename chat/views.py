
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from chat.models import Message, Chat
from chat.functions import getUsernameFromEmail, username_exists

"""
Chat View - Login is required an redirects to login page if user is not logged in. Anywhere user gets Chat HTML Page for a GET request. For a POST request user creates a new message in 
DB and returns the message Object as an JSO. 
"""
@login_required(login_url='/login/')
def index(request): 
    if request.method == 'POST':
        try:
            myChat = Chat.objects.get(id=1)
        except: 
            myChat = Chat.objects.create(id=1)
        newMessage = Message.objects.create(text=request.POST['textmessage'] , chat=myChat , author=request.user , receiver=request.user); 
        serializedObject = serializers.serialize('json' , [newMessage]); 
        return JsonResponse(serializedObject[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html' , {'messages':chatMessages})


"""
Login View - Returns the HTML Login Template for a GET request. For a POST request user try to loggin in. If sucessfull, user redirects to chat. 
"""
def login_view(request): 
    if request.user.is_authenticated:
        return HttpResponseRedirect("/chat/")
    redirect = request.GET.get('next')
    if request.method == 'POST':
        if '@' in request.POST['username']: 
            username_for_login = getUsernameFromEmail(request.POST['username'])
        else: 
            username_for_login = request.POST['username']
        if username_exists(username_for_login):
            user = authenticate(username=username_for_login, password=request.POST['password'])
            if user: 
                login(request, user)
                return HttpResponseRedirect("/chat/")
            else: 
                print("Wrong password")
                loginFailed =   {'wrongPassword' : True , 
                                'errorMessage' : 'Password is not correct!'}
                return JsonResponse(loginFailed, safe=False)
        else: 
            loginFailed =   {'wrongPassword' : True , 
                            'errorMessage' : 'User does not exists!'}
            return JsonResponse(loginFailed, safe=False)
    return render(request, 'auth/login.html',  {'redirect':redirect})


"""
Register View - Returns the HTML register template for a GET request. For a POST request user try to register. If sucessfull, user logged in and  redirects to chat. 
"""
def register_view(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirmPassword']:
            username = getUsernameFromEmail(request.POST['email'])
            if username_exists(username):
                loginFailed = {'wrongPassword' : True , 
                                'errorMessage' : 'User already exists' }
                return JsonResponse(loginFailed, safe=False)   
            else:
                user = User.objects.create_user(username, request.POST['email'], request.POST['password'])
                user.last_name = request.POST['lastName']; 
                user.first_name = request.POST['firstName']; 
                user.save()
                if user: 
                    login(request, user)
                    return HttpResponseRedirect("/chat/")
        else: 
            loginFailed = {'wrongPassword' : True , 
                            'errorMessage' : 'Passwords are not same' }
            return JsonResponse(loginFailed, safe=False)        
    return render(request, 'auth/register.html')


def logout_func(request): 
    logout(request) 
    return HttpResponseRedirect("/chat/")