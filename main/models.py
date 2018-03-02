from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=32, null=True, blank=True)
    def __unicode__(self):
        return self.name

class Component(models.Model):
    c_file = models.FileField(null=True)
    ratings = models.FloatField(default=0)
    monthly_rating = models.FloatField(default=0)
    name = models.CharField(max_length=200)
    github_url = models.URLField()
    user_p = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

class Download(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return str(self.component.name) + str(self.date_time)

class Rating(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True, null=True)
    value = models.IntegerField()
    def __unicode__(self):
        return str(self.component.name) + str(self.date_time)

class Comment(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField()
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    user_p = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.component.name)