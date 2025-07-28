from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('problems/', include('problems.urls')),
    path('solutions/', include('solutions.urls')),
    path('compilers/', include('compilers.urls')),
    path('users/', include('users.urls')),
    # Serve frontend index.html
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    # Serve favicon.ico
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)