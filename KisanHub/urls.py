from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('region.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
