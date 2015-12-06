# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import py2neo
from myapp.Neomodels import User, Photos
from myapp.models import Document,Doc,AddFriendRequest,GetFriendRequests,Dp, AcceptFriendRequest,RejectFriendRequest
from myapp.Forms import DocumentForm,DocForm

#to handle direct image upload requests
#html file on desktop myhtml.html for POST and mygetrequest.html for GET
@csrf_exempt
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            abc="abcd"
            newdoc = Document(docfile = request.FILES['docfile'],userid=request.POST['userid'])
            if not existPhoto(newdoc.docfile.name,newdoc.userid):
                newdoc.save()#This need to be looked into
            newNode(newdoc.userid,newdoc.docfile.name)

            # Redirect to the document list after POST
            return JsonResponse({"abcd":abc})# HttpResponseRedirect(reverse('list'))
    #Handle file retrieval
    if request.method == 'GET':
        url='http://192.168.0.108:8000/media/'
        image_array=[]
        final_object={}
        newdoc=Doc(user = request.GET['userid'])
        photos=retrieveImage(newdoc.user)
        for photo in photos:
            """image_data['name']=url+photo.name
            image_array.append(image_data)
            print image_data
            print image_array"""
            image_data=url+photo.name
            record={"name":image_data}
            #print record
            image_array.append(record)
        final_object["photos"]=image_array
        return JsonResponse(final_object)

    else:
        form = DocumentForm() # A empty, unbound form
#handling friend requests
#relevant html file on desktop friendRequest.html for POST and getFriendRequest.html for GET
@csrf_exempt
def f_req(request):
    if request.method== 'POST':
        new_request=AddFriendRequest(current_user=request.POST['current_user'],request_user=request.POST['request_user'])
        createRequest(new_request.current_user,new_request.request_user)
        return JsonResponse({'abcd':'reached_here'})

    if request.method=='GET':
        url='http://192.168.0.108:8000/media/'
        #print("iam here")
        get_request=GetFriendRequests(current_user=request.GET['current_user'])
        friend_requests=getFriendRequests(get_request.current_user)
        request_user_array=[]
        final_user_array_object={}
        for friend_request in friend_requests:
            user=User.inflate(friend_request[0])
            request_user_data=user.name
            request_user_image_url=getDp(user.name).name
            record={"uid":request_user_data,"url":url+request_user_image_url}
            print record
            request_user_array.append(record)
            #print user.name
        final_user_array_object["req_users"]=request_user_array
        return JsonResponse(final_user_array_object)
#handling user accepted requests
#related html desktop file AcceptRequest.html
@csrf_exempt
def acc_req(request):
    if request.method=='POST':
        acceptreq=AcceptFriendRequest(current_user=request.POST['current_user'],request_user=request.POST['request_user'])
        removeRequest(acceptreq.request_user,acceptreq.current_user)
        acceptFriend(acceptreq.request_user,acceptreq.current_user)
    return JsonResponse({"abcd":"Friendship Accepted"})

#handling user rejected requests
@csrf_exempt
def rej_req(request):
    if request.method=='POST':
        acceptreq=RejectFriendRequest(current_user=request.POST['current_user'],request_user=request.POST['request_user'])
        removeRequest(acceptreq.request_user,acceptreq.current_user)
    return JsonResponse({"abcd":"Friendship Rejected"})

#handling display picture changes
#relevant html file on desktop mydp.html
@csrf_exempt
def dp(request):
    if request.method == 'POST':
        abc="abcd"
        newdp = Dp(dp = request.FILES['dp'],userid=request.POST['userid'])
        print(newdp.dp.name)
        if(existPhoto(newdp.dp.name,newdp.userid)):
            print("iam here")
            url=getUrl(newdp.userid)+newdp.dp.name
            changeDp(newdp.userid,url)
        else:
            print("iam here too")
            newdp.save()#This needs to be looked into
            newDp(newdp.userid,newdp.dp.name)

        # Redirect to the document list after POST
        return JsonResponse({"abcd":abc})# HttpResponseRedirect(reverse('list'))

#handling relationship status between various users
#related desktop file is getStatus.html
@csrf_exempt
def get_status(request):
    print("inside get_status")
    if request.method== 'GET':
        rel_status=AcceptFriendRequest(current_user=request.GET['current_user'],request_user=request.GET['request_user'])
        print("inside get_status if")
        if(isFriend(rel_status.current_user,rel_status.request_user)):
            return JsonResponse({"status":"Friend"})
        if(isRequest(rel_status.current_user,rel_status.request_user)):
            return JsonResponse({"status":"Requested"})
        else:
            return JsonResponse({"status":"Add Friend"})

#helper method to check if the users are friends
def isFriend(current_user,request_user):
    query="Match (a:User {name:{name1}})-[:Friend]-(b:User {name:{name2}}) return a,b"
    result,columns=db.cypher_query(query,{'name1':current_user,'name2':request_user})
    if(result):
        return True
    else:
        return False

#helper method to check if the user has sent a friend request
def isRequest(current_user,request_user):
    query="Match (a:User {name:{name1}})-[:Request]->(b:User {name:{name2}}) return a,b"
    result,columns=db.cypher_query(query,{'name1':current_user,'name2':request_user})
    if(result):
        return True
    else:
        return False


#helper method that returns the Photos object for the current dp of a particular user
def getDp(user):
    query="Match (a:User {name:{no_name}})-[:Dp]->(c) return c"
    value=""
    result ,columns=db.cypher_query(query,{'no_name':user})
    for row in result:
        value=Photos.inflate(row[0])
        #print value
    return value

#helper method that changed the current Dp of the User
def changeDp(user,photo):
    usernode=User.nodes.get(name=user)
    photonode=Photos.nodes.get(name=photo)
    query="match (a:User {name:{no_node}})-[b:Dp]->(c) delete b"
    db.cypher_query(query,{'no_node':user})
    usernode.currentdp.connect(photonode)
    return

#helper method that sets a new dp for the User
def newDp(user,photo):
    Photos(name=photo).save()
    if(not existUser(user)):
        User(name=user).save()
    usernode=User.nodes.get(name=user)
    photonode=Photos.nodes.get(name=photo)
    usernode.uploader.connect(photonode)
    photonode.uploaded.connect(usernode)
    usernode.currentdp.connect(photonode)
    return

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

#helper method to check if a photo already exists in database
def existPhoto(photo,user):
    url=getUrl(user)+photo
    print url
    exists=[]
    query = 'MATCH (a:Photos{name: {no_name}}) return a'
    results , columns=db.cypher_query(query,{'no_name':url})
    if not results:
        return False
    else:
        return True

#helper method to get the folder directory of a particular user
def getUrl(user):
    url="files/users/"
    return url+user+"/"

#method to create a friend request between 2 users
def createRequest(current_user,request_user):
    user1=User.nodes.get(name=current_user)
    user2=User.nodes.get(name=request_user)
    user1.friend_req.connect(user2)
    """query = 'match (a:User {name :{user1}}),(b:User {name:{user2}}) create a-[:Request]->b'
    db.cypher_query(query,{'user1':user1.name,'user2':user2.name})"""
    #print("Reached here")
    return

def removeRequest(current_user,request_user):
    query="match (a:User {name:{user1}})-[b:Request]->(c:User {name:{user2}}) delete b"
    db.cypher_query(query,{'user1':current_user,'user2':request_user})
    return

def acceptFriend(current_user,request_user):
    query="match (a:User {name:{user1}}),(c:User {name:{user2}}) create a-[:Friend]-> c"
    db.cypher_query(query,{'user1':current_user,'user2':request_user})
    return

#helper method that checks for pending friend requests
def getFriendRequests(current_user):
    query='MATCH (A:User)-[:Request]->(:User{name:{no_name}}) RETURN A'
    rows, columns =db.cypher_query(query,{'no_name':current_user})
    return rows