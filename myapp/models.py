from django.db import models
##prtk
from neomodel import (StructuredNode, DateTimeProperty,BooleanProperty, StructuredRel ,StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom)
from uuid import uuid4
import pytz
from pytz import timezone
from datetime import datetime, date
##prtk
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

#prtk
class FriendRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    met = StringProperty()

class Post(StructuredNode):
    post_id = StringProperty(unique_index=True, default=uuid4)
    url=StringProperty(unique_index=True, default=uuid4)
    desc=StringProperty()
    owner=StringProperty(default="username@uuid4")#name of user

class Posted(StructuredRel):
    time = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    location = StringProperty()
    post_type = BooleanProperty()

class Person(StructuredNode):
    my_id=StringProperty(unique_index=True, default=uuid4)
    name = StringProperty()
    age = IntegerProperty(index=True, default=0)
    friends = RelationshipTo('Person', 'is_friend', model=FriendRel)
    posts = RelationshipTo('Post', 'post', model=Posted)
