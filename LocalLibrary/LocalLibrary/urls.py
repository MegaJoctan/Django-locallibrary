from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views import generic
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


handler404 = 'catalog.views.page_not_foundview'
handler500 = 'catalog.views.server_error_view'
handler403 = 'catalog.views.permission_denied_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/',include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/')),
    path('accounts/',include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
