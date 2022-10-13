from django.urls import path

from . import views

urlpatterns = [
    path('albums', views.AlbumList.as_view()),
    path('albums/<int:pk>', views.AlbumView.as_view()),
    path('albums/<int:pk>/edit', views.AlbumRetrieveUpdateDestroy.as_view()),
    path('albums/create', views.AlbumCreate.as_view()),
    path('albums/photo/upload', views.PhotoUpload.as_view()),
    path('albums/photo/<int:pk>', views.PhotoRetrieveUpdateDestroy.as_view()),
    path('albums/photo', views.PhotoList.as_view()),

    # Auth
    path('signup', views.signup),
    path('login', views.login),
]
