from django.db import models

from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, related_name='likes', blank=True)


class PostImage(models.Model):
    image = models.ImageField(upload_to='images/post/', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
