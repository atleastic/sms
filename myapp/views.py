# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import py2neo
from myapp.Neomodels import User, Photos

from myapp.models import Document,Doc
from myapp.Forms import DocumentForm,DocForm

@csrf_exempt
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            abc="abcd"
            newdoc = Document(docfile = request.FILES['docfile'],status=request.POST['status'])
            newdoc.save()
            newNode(newdoc.status,newdoc.docfile.name)

            # Redirect to the document list after POST
            return JsonResponse({"abcd":abc})# HttpResponseRedirect(reverse('list'))
    if request.method == 'GET':
        url='http://192.168.0.108:8000/media/'
        image_array=[]
        final_object={}
        image_data={}
        newdoc=Doc(user = request.GET['userid'])
        photos=retrieveImage(newdoc.user)
        for photo in photos:
            """image_data['name']=url+photo.name
            image_array.append(image_data)
            print image_data
            print image_array"""
            image_data=url+photo.name
            record={"name":image_data}
            print record
            image_array.append(record)
        final_object["photos"]=image_array
        return JsonResponse(final_object)

    else:
        form = DocumentForm() # A empty, unbound form

#method to create relatioships
def newNode(user,photo):
    py2neo.authenticate("localhost:7474", "neo4j", "porkunja")
    Photos(name=photo).save()
    if(not existUser(user)):
        User(name=user).save()
    usernode=User.nodes.get(name=user)
    photonode=Photos.nodes.get(name=photo)
    usernode.uploader.connect(photonode)
    photonode.uploaded.connect(usernode)
    return

#method to retrive content from the users
def retrieveImage(user):
    usernode = User.nodes.get(name=user)
    photos = usernode.getAllImages()
    return photos

#method to check if user already exists
def existUser(user):
    exists=[]
    query = 'MATCH (a:User{name: {no_name}}) return a'
    results , columns=db.cypher_query(query,{'no_name':user})
    for row in results:
        exists=User.inflate(row[0])
    if not exists:
        return False
    else:
        return True