from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    # API Endpoints - accessible from /api/
    path('shipment/<str:tracking_number>/', views.shipment_detail_json, name='shipment-detail'),
    path('shipment/<str:tracking_number>/location/', views.shipment_location_json, name='shipment-location'),
    path('shipments/', views.shipments_list, name='shipments-list'),
]
