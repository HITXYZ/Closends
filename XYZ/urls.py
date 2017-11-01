from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from closends import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^closends/', include('closends.urls', namespace='closends')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:
    handler404 = views.page_not_found
    handler500 = views.page_error