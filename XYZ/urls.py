from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from closends.views import exceptions

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^closends/', include('closends.urls', namespace='closends')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:
    handler404 = exceptions.page_not_found
    handler500 = exceptions.page_error
