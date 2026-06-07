from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]

# serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)