from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from blog.models import Post
from blog.serializers import PostSerializer


def index(request):
    return HttpResponse("hello world")

# @csrf_exempt
# def post_list(request):
#     if request.method=="GET":
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     if request.method=="POST":
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
# @csrf_exempt
# def post_detail(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == "GET":
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(post, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#     elif request.method == "DELETE":
#         post.delete()
#         return HttpResponse(status=204)

@api_view(["GET", "POST"])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method=="POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=="GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method=="PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method=="DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

