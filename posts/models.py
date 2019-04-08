from django.db import models
from django.contrib.auth import get_user_model

from django.urls import reverse

USER_MODEL = get_user_model()


class Comment(models.Model):
    comment = models.CharField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)


def upload_location(instance, filename):
    return f'{instance.id}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    post_image = models.ImageField(upload_to=upload_location,
                                   null=True, blank=True)

    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='Likes')
    likes = models.ManyToManyField(USER_MODEL, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:details_view", kwargs={"pk": self.pk})
