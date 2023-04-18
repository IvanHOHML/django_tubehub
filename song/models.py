from django.db import models

# Create your models here.

class Playlist (models.Model):
    url = models.CharField(max_length=2000)
    pub_date = models.DateTimeField("date published")
    status_code = models.IntegerField()
    def __str__(self):
        return self.url