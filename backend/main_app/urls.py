import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from frontend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout', views.logout_user, name='logout'),
    path('', views.LoginView.as_view(), name='login'),
    path('schemas/', include('frontend.urls')),
    path('api/', include('backend_api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
