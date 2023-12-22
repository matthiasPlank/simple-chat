from django.shortcuts import render

from chat.models import Message, Chat

# Create your views here.
def index(request): 
    print(request.method)
    if request.method == 'POST':
        print("Received Data:" + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'] , chat=myChat , author=request.user , receiver=request.user); 
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html' , {'messages':chatMessages})