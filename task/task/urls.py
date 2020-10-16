from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

'''
URL Patterns here include URL routes to the admin path as well as URL routes mentioned in the app.urls file.
Better to define URL in the app.urls for a particular app for easy debugging.
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls'))
]

'''
Define the static and media URL routes. Currently not used as we don't have any static or media files.
'''
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
