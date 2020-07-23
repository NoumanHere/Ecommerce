from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin

handler404 = 'core.views.view_404'

admin.site.site_title = "Mbata's Site"
admin.site.site_header = "Ecommerce"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls', namespace='core')),
    path('', include('pwa.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
