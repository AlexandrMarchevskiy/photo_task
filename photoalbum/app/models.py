from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from versatileimagefield.fields import VersatileImageField


class Album(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=100, null=False, blank=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class Photo(models.Model):
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, blank=False)

    title = models.CharField(max_length=25)
    image = VersatileImageField(
        upload_to='photos/%Y/%m/%d', null=False, blank=False)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image}'

    def get_absolute_url(self):
        return reverse('photo', kwargs={'photo': self.pk})

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
