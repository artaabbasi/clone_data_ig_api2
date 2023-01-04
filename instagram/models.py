from django.db import models

class Post(models.Model):
    class MediaTypes(models.IntegerChoices):
        CAROUSEL_ALBUM = 0
        IMAGE = 1
        VIDEO = 2
    media_id = models.CharField(max_length=2048, unique=True)
    page_id = models.CharField(max_length=2048)
    created_at = models.DateTimeField()
    like_count = models.IntegerField()
    comment_count = models.IntegerField()
    media_type = models.IntegerField(choices=MediaTypes.choices)
