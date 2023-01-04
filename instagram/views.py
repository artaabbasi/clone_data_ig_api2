from rest_framework import response, status, generics, permissions as perms, decorators
from django.shortcuts import get_object_or_404
from . import models, sample_data, serializers
import requests, json, datetime
from decouple import config

ACCESS_TOKEN = config('ACCESS_TOKEN')
BASIC_URL = config('BASIC_URL')
IG_USER_ID = config('IG_USER_ID')

@decorators.api_view(['GET', ])
@decorators.permission_classes([perms.AllowAny, ]) 
def clone_data(request):
    """
    if you have access token in your .env file
    dont send test param
    else send ?test=1
    """
    page = request.GET.get('page')
    duration = request.GET.get('duration', 30)
    test = int(request.GET.get('test', 0))

    if test:
        dict_content = json.loads(sample_data.sample_res)
    else:
        use_url = BASIC_URL+IG_USER_ID+"?fields=business_discovery.username("+page+"){media{timestamp,comments_count,like_count,media_type}}&duration=&access_token="+ACCESS_TOKEN
        req = requests.get(use_url)
        dict_content = json.loads(req.content)
        

    page_id = dict_content["business_discovery"]["ig_id"] 
    need_medias = []
    now = datetime.datetime.now()
    for media in dict_content["business_discovery"]["media"]["data"]:
        post_timestamp = datetime.datetime.fromisoformat(media["timestamp"]).replace(tzinfo=None)
        timedelta =  now - post_timestamp
        if timedelta.days <= duration :
            values = {
                "page_id":page_id,
                "media_id":media["id"],
                "created_at": post_timestamp,
                "like_count":media["like_count"],
                "comment_count":media["comments_count"],
            }
            if media["media_type"]=="CAROUSEL_ALBUM" : values.update({"media_type":0})
            elif media["media_type"]=="IMAGE" : values.update({"media_type":1})
            else : values.update({"media_type":2})
            try:
                post = models.Post.objects.create(**values)
            except:
                post = models.Post.objects.filter(media_id=values["media_id"]).update(**values)
                post = models.Post.objects.filter(media_id=values["media_id"]).first()

            need_medias.append(post)
        else:
            break
    ser = serializers.PostSerilizer(need_medias, many=True)
    return response.Response({"results":ser.data}, status=status.HTTP_200_OK)