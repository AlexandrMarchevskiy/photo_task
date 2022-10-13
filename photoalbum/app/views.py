from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

from .models import Photo, Album


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'photos/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                Token.objects.create(user=user)
                login(request, user)
                return redirect('gallery')
            except IntegrityError:
                return render(request, 'photos/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'photos/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'photos/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'photos/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('gallery')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('loginuser')


@login_required
def gallery(request):
    user = request.user
    album = request.GET.get('album')
    if album is None:
        photos = Photo.objects.filter(album__user=user)
    else:
        photos = Photo.objects.filter(
            album__title=album, album__user=user)

    albums = Album.objects.filter(user=user)
    context = {'albums': albums, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


@login_required
def viewphoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


@login_required
def addphoto(request):
    user = request.user

    albums = user.album_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['album'] != 'none':
            album = Album.objects.get(id=data['album'])
        elif data['album_new'] != '':
            album, created = Album.objects.get_or_create(
                user=user,
                title=data['album_new'])
        else:
            album = None

        for image in images:
            Photo.objects.create(
                album=album,
                description=data['description'],
                image=image,
                user=user,
            )

        return redirect('gallery')

    context = {'albums': albums}
    return render(request, 'photos/add.html', context)


@login_required
def deletephoto(request, pk):
    photo = Photo.objects.get(id=pk)
    photo.delete()
    return redirect('gallery')
