from django.db import models
from django.contrib.auth import get_user_model

from django.urls import reverse

USER_MODEL = get_user_model()


def upload_location(post, filename):
    return f'{post.pk}/{filename}'


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

    class Meta:
        ordering = ['-created_timestamp']


class Comment(models.Model):
    comment = models.TextField(max_length=300)
    created_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    author = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment if len(self.comment) < 10 else self.comment[:10]

    class Meta:
        ordering = ['-created_timestamp']

