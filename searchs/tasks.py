from celery import shared_task
from .models import Search
import re
import json
import urllib.request
from xml.dom import minidom
from django.contrib.auth.models import User


@shared_task
def add(search, userdetails):
	print(search + userdetails)

@shared_task
def createSearch(search, userdetails):

    page = 1
    links = []
    
    if search.website == "1":

        while True:

            source = urllib.request.urlopen("https://1.com/search.json?key="+str(userdetails.apikey)+"&q="+urllib.parse.quote_plus(search.searchtext)+"&page="+str(page)).read()
            print(page)
            data = json.loads(source.decode())
            # Si no hay mas resultados
            if len(data["search"]) == 0:
                break
            page += 1
            for i in data["search"]:
                links.append(i)
        # Reversed para que las imagenes mas viejas se agreguen primero
        for i in reversed(links):
            try:
                # Crear "Image" objects en el "search"
                search.image_set.create(thumb=i["representations"]["thumb"], url=i["representations"]["full"], urlpost=re.search('/(\d+)__', i["representations"]["full"]).group(1), artist=re.search('artist:(.+?),', i["tags"]).group(1), source=i["source_url"],tags=i["tags"])
            except:
                continue

    elif search.website == "2":
        
        while True:
            # Pide user agent asi que hay que hacerlo mas complicado
            url = urllib.request.Request("https://2.com/post/index.json?tags="+urllib.parse.quote_plus(search.searchtext)+"&page="+str(page))
            url.add_header('User-agent', 'Personal spider')
            source = urllib.request.urlopen(url).read()
            print(page)
            data = json.loads(source.decode())
            if not data:
                break
            page += 1
            for i in data:
                links.append(i)
        for i in reversed(links):
            try:
                search.image_set.create(thumb=i['preview_url'], url=i['file_url'], urlpost=i['id'],artist=i['artist'],source=i['source'],tags=i["tags"])
            except:
                continue


    elif search.website == "3":
        page = 0
        
        while True:
            # No usa JSON
            url = urllib.request.Request("http://3.com/index.php?page=dapi&s=post&q=index&tags="+urllib.parse.quote_plus(search.searchtext)+"&pid="+str(page))
            url.add_header('User-agent', 'Personal spider')
            source = urllib.request.urlopen(url)
            print(page)
            datau = minidom.parse(source)
            data = datau.getElementsByTagName('post')
            if not data:
                break
            page += 1
            for i in data:
                links.append(i)
        for i in reversed(links):
            null = "https://href.li/?http:"
            try:
                search.image_set.create(thumb=i.attributes['preview_url'].value, url=null+i.attributes['sample_url'].value, urlpost=i.attributes['id'].value,source=i.attributes["source"].value,tags=i.attributes["tags"].value)
            except:
                continue
    search.working = False
    search.save()


@shared_task
def updateSearch(website, user, search, lastid):



    page = 1
    links = []

    # Get Last 2 weeks of images
        # today = datetime.now()
        # time2weeks = timedelta(weeks=-8)
        # result = today + time2weeks
        # month = str(result.month)
        # day = str(result.day)
        # if len(month) == 1:
        #     month = "0"+month
        # if len(day) == 1:
        #     day = "0"+day
        # tag = ",created_at.gte:"+str(result.year)+"-"+month+"-"+day

    search.working = True
    search.save()
    if website == "1":


        while True:

            if lastid:
                source = urllib.request.urlopen("https://1.com/search.json?key="+str(user.details.apikey)+"&q="+urllib.parse.quote_plus(search.searchtext)+urllib.parse.quote_plus(lastid)+"&page="+str(page)).read()
            else:
                source = urllib.request.urlopen("https://1.com/search.json?key="+str(user.details.apikey)+"&q="+urllib.parse.quote_plus(search.searchtext)+"&page="+str(page)).read()

            print(page)
            data = json.loads(source.decode())
            if len(data["search"]) == 0:
                break
            page += 1
            for i in data["search"]:
                links.append(i)
        for i in reversed(links):
            if search.image_set.filter(thumb=i["representations"]["thumb"]).exists():
                continue
            try:
                search.image_set.create(thumb=i["representations"]["thumb"], url=i["representations"]["full"], urlpost=re.search('/(\d+)__', i["representations"]["full"]).group(1), artist=re.search('artist:(.+?),', i["tags"]).group(1), source=i["source_url"],tags=i["tags"])
            except:
                continue

    elif website == "2":

        while True:
            
            if lastid:
                url = urllib.request.Request("http://2.com/index.php?page=dapi&s=post&q=index&tags="+urllib.parse.quote_plus(search.searchtext)+urllib.parse.quote_plus(lastid)+"&pid="+str(page))
            else:
                url = urllib.request.Request("http://2.com/index.php?page=dapi&s=post&q=index&tags="+urllib.parse.quote_plus(search.searchtext)+"&pid="+str(page))

            url.add_header('User-agent', 'Personal spider')
            source = urllib.request.urlopen(url)
            print(page)
            datau = minidom.parse(source)
            data = datau.getElementsByTagName('post')
            if not data:
                break
            page += 1
            for i in data:
                links.append(i)
        for i in reversed(links):
            null = "https://href.li/?http:"
            if search.image_set.filter(thumb=i.attributes['preview_url'].value).exists():
                continue
            try:
                search.image_set.create(thumb=i.attributes['preview_url'].value, url=null+i.attributes['sample_url'].value, urlpost=i.attributes['id'].value,source=i.attributes["source"].value,tags=i.attributes["tags"].value)
            except:
                continue
    elif website == "3":
        while True:
            # Pide user agent asi que hay que hacerlo mas complicado porque fuck
            if lastid:
                url = urllib.request.Request("https://3.com/post/index.json?tags="+urllib.parse.quote_plus(search.searchtext)+urllib.parse.quote_plus(lastid)+"&page="+str(page))
            else:
                url = urllib.request.Request("https://3.com/post/index.json?tags="+urllib.parse.quote_plus(search.searchtext)+"&page="+str(page))
            url.add_header('User-agent', 'Personal spider')
            source = urllib.request.urlopen(url).read()
            print(page)
            data = json.loads(source.decode())
            if not data:
                break
            page += 1
            for i in data:
                links.append(i)
        for i in reversed(links):
            if search.image_set.filter(thumb=i['preview_url']).exists():
                continue
            try:
                search.image_set.create(thumb=i['preview_url'], url=i['file_url'], urlpost=i['id'],artist=i['artist'],source=i['source'],tags=i["tags"])
            except:
                continue
    search.working = False
    search.save()

@shared_task
def updateAll():
	for user in User.objects.all():
		for search in user.search_set.all():

			    website = search.website

			    firstimage = search.image_set.latest('id')
			    firstid = firstimage.urlpost
			    if website == "1":
			        lastid = ",id.gte:"+firstid
			    else:
			        lastid = " id:>"+firstid
			    print(firstid)

			    updateSearch(website, user, search, lastid)
