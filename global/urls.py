from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('ccmeyers100/', admin.site.urls),
    path('', include('light.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
