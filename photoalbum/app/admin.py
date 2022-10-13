from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Photo, Album


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')
    list_display_links = ('title', 'user', 'created')
    list_filter = ('title', 'user', 'created')


class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'album', 'image', 'title',
        'description', 'created', 'user')
    list_display_links = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" heidth="150"')

    get_image.short_description = 'Изображение'


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)

admin.site.site_title = 'Django Photoalbum'
admin.site.site_header = 'Django Photoalbum'
