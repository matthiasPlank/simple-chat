
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from chat.models import Message, Chat
from chat.functions import getUsernameFromEmail

"""
Chat View 
"""
@login_required(login_url='/login/')
def index(request): 
    if request.method == 'POST':
        myChat = Chat.objects.get(id=1)
        newMessage = Message.objects.create(text=request.POST['textmessage'] , chat=myChat , author=request.user , receiver=request.user); 
        serializedObject = serializers.serialize('json' , [newMessage]); 
        return JsonResponse(serializedObject[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html' , {'messages':chatMessages})


"""
Login View 
"""
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


"""
Register View 
"""
def register_view(request):
    if request.method == 'POST':
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