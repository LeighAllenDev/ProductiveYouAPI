from django.contrib import admin
from django.urls import path, include
from .views import root_route, logout_route
from django.conf import settings
from django.conf.urls.static import static
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('profiles/', include('profiles.urls')),
    path('api/', include('tasks.urls')),
    path('teams/', include('teams.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)