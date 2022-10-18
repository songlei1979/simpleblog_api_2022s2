from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from blog.models import Post
from blog.serializers import PostSerializer


def index(request):
    return HttpResponse("hello world")

@csrf_exempt
def post_list(request):
    if request.method=="GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method=="POST":
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        post.delete()
        return HttpResponse(status=204)

