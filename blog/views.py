from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template import context
from django.views.decorators.csrf import csrf_exempt
from pytz import unicode
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.models import Post, Category
from blog.permissions import IsAuthorOrReadOnly, IsAuthor
from blog.serializers import PostSerializer, UserSerializer, CategorySerializer


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
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == "PUT":
        print("login user", request.user)
        print("author user", post.author)
        if request.user == post.author:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("You don't have the permission")
    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)

    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        title = request.data["title"]
        author = request.user
        body = request.data["body"]
        category = request.data["category"]
        try:
            post = Post.objects.create(title=title, author=author, body=body, category_id=category)
            post.save()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def User_ID_Search(request):
    return Response({"userid": request.user.id})
