from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from app.models import Album, Photo

from .permissions import IsOwnerOrReadOnly
from .serializers import AlbumSerializer, PhotoSerializer, PhotoWithoutImageField, AlbumListSerializer


@csrf_exempt
def signup(request):
    """Регистрация пользователя с выдачей токена"""
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(
                {'error': 'That username has already been taken. Please choose a new username'}, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            return JsonResponse(
                {'error': 'Could not login. Please check username and password'}, status=400)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)


class AlbumList(generics.ListAPIView):
    """Вывод списка альбомов"""
    serializer_class = AlbumListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created']

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(user=user)


class AlbumCreate(generics.ListCreateAPIView):
    """Создание альбома"""
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Изменение альбома / Удаление"""
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(user=user)


class PhotoList(generics.ListAPIView):
    """Вывод списка фото"""
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['album']
    ordering_fields = ['created', 'album']

    def get_queryset(self):
        user = self.request.user
        return Photo.objects.filter(user=user)


class PhotoUpload(generics.CreateAPIView):
    """Загрузка фото"""
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PhotoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """Изменение некоторых полей фото"""
    serializer_class = PhotoWithoutImageField
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Photo.objects.filter(user=user)


class AlbumView(generics.RetrieveAPIView):
    """Вывод альбома"""
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Album.objects.filter(user=user)
