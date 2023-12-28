from django.contrib.auth.models import User
import re

def getUsernameFromEmail(username): 
    subIndex = username.find('@')
    username = username[0:subIndex]; 
    username = re.sub('[\W_]+', '', username)
    return username


def username_exists(username):
    return User.objects.filter(username=username).exists()