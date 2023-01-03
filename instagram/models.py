from django.db import models

class Page(models.Model):
    username = models.CharField(max_length=1024, unique=True)
    ig_user_id = models.CharField(max_length=2048, unique=True)


class Post(models.Model):
    class MediaTypes(models.IntegerChoices):
        CAROUSEL_ALBUM = 0
        IMAGE = 1
        VIDEO = 2
    media_id = models.CharField(max_length=2048, unique=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    media_type = models.IntegerField(choices=MediaTypes.choices)
