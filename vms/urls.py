from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    # vendor endpoints
    path('vendors/', vendor_api.as_view(), name='vendor'),
    path('vendors/<int:vendor_id>/', vendor_api.as_view(), name='vendor'),

    # purchase order endpoints
    path('purchase_orders/', purchase_order_api.as_view(), name='purchase_order'),
    path('purchase_orders/<int:po_id>/', purchase_order_api.as_view(), name='purchase_order'),

    # performance endpoint
    path('vendors/<int:vendor_id>/performance/', vendor_performance_api.as_view(), name='vendor_performance'),

    # acknowledge endpoint
    path('purchase_orders/<int:po_id>/acknowledge/', vendor_acknowledge_api.as_view(), name='vendor_acknowledge')
]