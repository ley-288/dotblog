from django.contrib import admin
from django.urls import path, include

from django.conf import settings##
from django.conf.urls.static import static##

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('theblog.urls')), #import our folder
    path('members/', include('django.contrib.auth.urls')), #takes care of all urls for you, login for example
    path('members/', include('members.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)##just set up in our settings.py
