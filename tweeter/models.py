from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# class Dislike(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')


class Tweet(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweets')
    likes = GenericRelation(Like)
    # dislikes = GenericRelation(Dislike)

    @property
    def total_likes(self):
        return self.likes.count()

    # @property
    # def total_dislikes(self):
    #     return self.dislikes.count()

    def __str__(self):
        return f'{self.user.username} - {self.title}'


class Comment(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user.username} - {self.tweet.title} - {self.text}'





