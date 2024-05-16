from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('eBirth_basic.urls', namespace='basic')),
    path('auth/', include('eBirth_auth.urls', namespace='auth')),
    path('reg/', include('eBirth_reg.urls', namespace='reg')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "National Identification Number, Birth and Death Registration System"
admin.site.site_title = "National Identification Number, Birth and Death Registration System"
admin.site.index_title = "Welcome to National Identification Number, Birth and Death Registration System"