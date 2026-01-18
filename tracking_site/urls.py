from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracking import views as tracking_views

urlpatterns = [
    # HTML Pages
    path('', tracking_views.index, name='home'),
    path('signin/', tracking_views.signin, name='signin'),
    path('signup/', tracking_views.signup, name='signup'),
    path('track/', tracking_views.track_page, name='track'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/', include('tracking.urls')),
    path('auth/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
