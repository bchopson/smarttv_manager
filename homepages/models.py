from django.db import models


class Tv(models.Model):
    id = models.IntegerField(primary_key=True)
    ip_address = models.URLField(max_length=200)
    updated = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=200, default='')

    def __str__(self):
        return "TV%s: %s" % (self.id, self.ip_address)


class Slide(models.Model):
    index = models.IntegerField(default=0)
    tv = models.ForeignKey(Tv, on_delete=models.CASCADE, related_name='slides')
    url = models.URLField(max_length=200)
    duration = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.tv.save()
        super(Slide, self).save(*args, **kwargs)

    def __str__(self):
        return "[index=%s, tv=%s, url=%s, duration=%s]" % (self.index, self.tv.id,
                                                           self.url, self.duration)

    class Meta:
        ordering = ['index']
        unique_together = (("index", "tv"))
