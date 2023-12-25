def getUsernameFromEmail(username): 
    subIndex = username.find('@')
    username = username[0:subIndex]; 
    username = re.sub('[\W_]+', '', username)
    return username