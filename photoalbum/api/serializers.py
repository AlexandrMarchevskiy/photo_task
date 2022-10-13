from rest_framework import serializers
from app.models import Album, Photo
from versatileimagefield.serializers import VersatileImageFieldSerializer


class PhotoSerializer(serializers.ModelSerializer):
    """Вывод фото"""
    created = serializers.ReadOnlyField()

    class Meta:
        model = Photo
        fields = ('__all__')
        read_only_fields = ['user', 'created']

    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__150x150'),
        ]
    )


class PhotoWithoutImageField(serializers.ModelSerializer):
    """Вывод фото без возможности затрагивать поле изображения"""
    created = serializers.ReadOnlyField()

    class Meta:
        model = Photo
        fields = ('title', 'image', 'description', 'created', 'user')
        read_only_fields = ['user', 'created', 'image']

    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__150x150'),
        ]
    )


class AlbumListSerializer(serializers.ModelSerializer):
    """Вывод альбомов"""
    photos = serializers.IntegerField(source='photo_set.count', read_only=True)

    class Meta:
        model = Album
        fields = ('__all__')
        read_only_fields = ['user', 'created']


class AlbumSerializer(serializers.ModelSerializer):
    """Вывод одного альбома с фото"""
    photos = PhotoSerializer(source='photo_set', many=True)

    class Meta:
        model = Album
        fields = ('__all__')
        read_only_fields = ['user', 'created']
