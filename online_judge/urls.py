from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('problems/', include('problems.urls')),
    path('solutions/', include('solutions.urls')),
    path('compilers/', include('compilers.urls')),
    path('users/', include('users.urls')),
]