from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Users.urls')),
    path('',include('Dashboard.urls')),
    path('',include('Services.urls')),
    path('',include('Customers.urls')),
    path('',include('Workforce.urls')),
    path('accounts/',include('Accounts.urls')),
    path('works/',include('Works.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)