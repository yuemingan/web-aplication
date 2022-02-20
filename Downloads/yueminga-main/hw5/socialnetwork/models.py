from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    class Meta:
       ordering = ['-creation_time']
    user            = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    text            = models.TextField(max_length=200)
    creation_time   = models.DateTimeField()

    def __str__(self):
        return 'user=' + str(self.user.first_name) + ', text=' + self.text + ', creation_time=' + str(self.creation_time)

class Profile(models.Model):
    bio             = models.CharField(max_length=200)
    user            = models.OneToOneField(User, on_delete=models.PROTECT)
    picture         = models.FileField(blank=True)
    content_type    = models.CharField(max_length=50)
    following       = models.ManyToManyField(User, related_name="followers")
