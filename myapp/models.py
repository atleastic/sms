from django.db import models

# Create your models here.

def generate_filename(self,filename):
    url=url = "files/users/%s/%s" % (self.status, filename)
    return url


class Document(models.Model):
    docfile=models.FileField(upload_to=generate_filename)
    status=models.CharField(max_length=100,default='No Status')
    def __str__(self):              # __unicode__ on Python 2
        return self.status

class Doc(models.Model):
    user=models.CharField(max_length=100,default='No name')
    def __str__(self):
        return self.user