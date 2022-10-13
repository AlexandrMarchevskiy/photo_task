from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import views
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # photos
    path('', views.gallery, name='gallery'),
    path('photo/<int:pk>/', views.viewphoto, name='photo'),
    path('add/', views.addphoto, name='add'),
    path('photo/<int:pk>/delete', views.deletephoto, name='deletephoto'),

    # API
    path('api/v1/', include('api.urls'))
]

urlpatterns += doc_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
