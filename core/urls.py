from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Sirf admin aur aapke main store ke urls yahan hone chahiye
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# Media files load karne ke liye configuration
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)