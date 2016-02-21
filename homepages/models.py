from django.db import models

class Tv(models.Model):
    id = models.IntegerField(primary_key=True)
    ip_address = models.URLField(max_length=200)
    def __str__(self):
        return "TV%s: %s" % (self.id, self.ip_address)

class Slide(models.Model):
    tv = models.ForeignKey(Tv, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    duration = models.IntegerField(default=0)
    def __str__(self):
        return "[tv=%s, url=%s, duration=%s]" % (self.tv.id, self.url, self.duration)