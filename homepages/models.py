from django.db import models

class Tv(models.Model):
    ip_address = models.URLField(max_length=200)

class Slide(models.Model):
    tv = models.ForeignKey(Tv, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    duration = models.IntegerField(default=0)