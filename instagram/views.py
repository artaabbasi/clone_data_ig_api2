from rest_framework import response, status, generics, permissions as perms, decorators
from django.shortcuts import get_object_or_404
from . import models, sample_data, serializers
import requests, json, datetime
from decouple import config


@decorators.api_view(['GET', ])
@decorators.permission_classes([perms.AllowAny, ]) 
def clone_data(request):
    access_token = config('ACCESS_TOKEN')
    basic_url = config('BASIC_URL')
    ig_user_id = config('IG_USER_ID')
    page = request.GET.get('page')
    duration = request.GET.get('duration', 30)

    # use_url = basic_url+ig_user_id+"?fields=business_discovery.username("+page+"){media{timestamp,comments_count,like_count,media_type}}&duration=&access_token="+access_token
    # req = requests.get(use_url)
    dict_content = json.loads(sample_data.sample_res)

    page_obj, crt = models.Page.objects.get_or_create(username=page, ig_user_id=dict_content["business_discovery"]["ig_id"] )
    need_medias = []
    now = datetime.datetime.now()
    for media in dict_content["business_discovery"]["media"]["data"]:
        post_timestamp = datetime.datetime.fromisoformat(media["timestamp"]).replace(tzinfo=None)
        timedelta =  now - post_timestamp
        if timedelta.days <= duration :
            values = {
                "page_id":page_obj.id,
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