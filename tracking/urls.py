from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # HTML Pages
    path('', views.index, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('track/', views.track_page, name='track-page'),
    
    # API Endpoints
    path('api/shipment/<str:tracking_number>/', views.shipment_detail_json, name='shipment-detail'),
    path('api/shipment/<str:tracking_number>/location/', views.shipment_location_json, name='shipment-location'),
    path('api/shipments/', views.shipments_list, name='shipments-list'),
]
