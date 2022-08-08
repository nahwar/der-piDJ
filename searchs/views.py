from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Search, Details, LogEntry
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
# from datetime import timedelta, datetime
import re
import json
import urllib.request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xml.dom import minidom
from .tasks import createSearch, updateSearch
# Create your views here.

def kollog(request):

    entry = request.GET.get('q', '')
    if entry != "":

        search = LogEntry.objects.create(entry=entry)
        return HttpResponse('')
    else:
        kollog = reversed(LogEntry.objects.all())

        return render(request, 'kollog.html', {'kollog':kollog})

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('userindex', args=(request.user.id,)))
        else:

            return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('userindex', args=(request.user.id,)))
                #return HttpResponseRedirect(request.POST.get('next'))
            else:
                error_message = "You have been banned"
                return render(request, 'login.html', {'error_message':error_message, 'username':username})

        else:
            error_message = "User or password wrong"
            return render(request, 'login.html', {'error_message':error_message, 'username':username})


@login_required
def logout_path(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def index(request):
    user = request.user
    # Agrega OneToOneField "details" al user (Para contener Api Key)
    if not hasattr(user, 'details'):
        i = Details(user=user)
        i.save()
    return HttpResponseRedirect(reverse('userindex', args=(request.user.id,)))


@login_required
def userindex(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Check si user es dueño del index o admin
    if request.user.id == user.id or request.user.is_staff:
        searchs = user.search_set.all()
        return render(request, 'index.html', {'searchs' : searchs})
    return HttpResponseRedirect(reverse('index'))


@login_required
def new(request):
    return render(request, 'new.html')


@login_required
def create(request):
    # Consigue details del usuario para saber apikey
    userdetails = Details.objects.get(user=request.user)
    tags = request.POST['Tags']
    website = request.POST['website']
    # Crea "Search" object
    search = Search.objects.create(searchtext=tags,owner=request.user,website=website)

    createSearch.delay(search, userdetails)
    return HttpResponseRedirect("/")

def update(request, user_id, search_id):

    user = User.objects.get(id=user_id)
    search = Search.objects.get(id=search_id)
    tags = search.searchtext
    website = search.website

    if website == "1":
        lastid = ",id.gte:0"
    else:
        lastid = " id:>0"

    updateSearch.delay(website, user, search, lastid)

    return HttpResponseRedirect(reverse('show', args=(request.user.id,search.id)))


@login_required
def show(request, search_id, user_id):
    search = get_object_or_404(Search, id=search_id)
    if str(request.user.id) == user_id:
        images_list = search.image_set.order_by('-id')
        paginator = Paginator(images_list, 40) # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            images = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            images = paginator.page(paginator.num_pages)
        # if not images_list:
        #     return HttpResponseRedirect(reverse('delete', args=(request.user.id,search_id)))
        return render(request, 'show.html', {'images' : images, 'working' : search.working})
    else:
        return HttpResponseRedirect(reverse('index'))


@login_required
def showimage(request, search_id, image_id, user_id):
    search = get_object_or_404(Search, id=search_id)
    print(search)
    website = search.website
    print(website)
    if str(request.user.id) == user_id:
        image = search.image_set.get(id=image_id)
        
        if website == "3":
            image.artist = image.artist.replace("'","")
            image.artist = image.artist.replace('[',"")
            image.artist = image.artist.replace(']',"")

        url = image.url
        if request.is_ajax():
            return JsonResponse({'url' : url})
        else:
            return render(request, 'showimage.html', {'image':image, 'website':website})


@login_required
def delete(request, search_id, user_id):
    search = get_object_or_404(Search, id=search_id)
    if str(request.user.id) == user_id or request.user.is_staff:
        search.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required
def apikey(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(User, id=user_id)
        if request.user.id == user.id:
            return render(request, 'apikey.html', {'user':user})
    if request.method == "POST":
        apikeytoset = request.POST['apikey']
        userdetails = Details.objects.get(user=request.user)
        userdetails.apikey = apikeytoset
        userdetails.save()
        return HttpResponseRedirect(reverse('index'))


@login_required
def deleteimage(request, user_id, search_id, image_id):
    search = get_object_or_404(Search, id=search_id)
    image = search.image_set.get(id=image_id)
    if str(request.user.id) == user_id:
        image.delete()
    return HttpResponseRedirect(reverse('show', args=(request.user.id,search_id)))
