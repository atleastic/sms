from django.db import models

# Create your models here.

def generate_filename(self,filename):
    url=url = "files/users/%s/%s" % (self.userid, filename)
    return url


class Document(models.Model):
    docfile=models.FileField(upload_to=generate_filename)
    userid=models.CharField(max_length=100,default='No Status')
    def __str__(self):              # __unicode__ on Python 2
        return self.userid

class Dp(models.Model):
    dp=models.FileField(upload_to=generate_filename)
    userid=models.CharField(max_length=100)
    def __str__(self):
        return self.userid

class Doc(models.Model):
    user=models.CharField(max_length=100,default='No name')
    def __str__(self):
        return self.user

class AddFriendRequest(models.Model):
    current_user=models.CharField(max_length=100)
    request_user=models.CharField(max_length=100)
    def __str__(self):
        return self.current_user,self.request_user

class AcceptFriendRequest(models.Model):
    current_user=models.CharField(max_length=100)
    request_user=models.CharField(max_length=100)
    def __str__(self):
        return self.current_user,self.request_user

class RejectFriendRequest(models.Model):
    current_user=models.CharField(max_length=100)
    request_user=models.CharField(max_length=100)
    def __str__(self):
        return self.current_user,self.request_user

class GetFriendRequests(models.Model):
    current_user=models.CharField(max_length=100)
    def __str__(self):
        return self.current_user

