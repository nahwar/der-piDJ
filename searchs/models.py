from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class LogEntry(models.Model):
    entry = models.CharField(max_length=500, default='Error')

    def __str__(self):
        return str(self.entry)


class Search(models.Model):
    owner      = models.ForeignKey(User, on_delete = models.CASCADE)
    website      = models.CharField(max_length       = 100)
    searchtext = models.CharField(max_length       = 1000)
    working    = models.BooleanField(default       = True)

    def __str__(self):
        return str(self.id) + " - " + str(self.searchtext)


class Details(models.Model):
    user   = models.OneToOneField(User, on_delete = models.CASCADE)
    apikey = models.CharField(max_length          = 500, default    = '')

    def __str__(self):
        return str(self.user.username)


class Image(models.Model):
    search  = models.ForeignKey(Search, on_delete = models.CASCADE)
    thumb   = models.CharField(max_length         = 1000, default   = 'Unknown', null = True, blank = True)
    url     = models.CharField(max_length         = 1000, default   = 'Unknown', null = True, blank = True)
    urlpost = models.CharField(max_length         = 1000, default   = 'Unknown', null = True, blank = True)
    artist  = models.CharField(max_length         = 500, default    = 'Unknown', null = True, blank = True)
    source  = models.CharField(max_length         = 1000, default   = 'Unknown', null = True, blank = True)
    tags    = models.CharField(max_length         = 5000, default   = 'None', null    = True, blank = True)

    def __str__(self):
        return str(self.search) + " - " + str(self.id)
