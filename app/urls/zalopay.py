# urls/zalopay_urls.py

from django.urls import path
from app.apis.zalopay_create import ZaloPayCreateOrder
from app.apis.zalopay_callback import ZaloPayCallback
from app.apis.zalopay_status import ZaloPayOrderStatus

urlpatterns = [
    path('zalopay/create-order/', ZaloPayCreateOrder.as_view(), name='zalopay_create_order'),
    path('zalopay/callback/', ZaloPayCallback.as_view(), name='zalopay_callback'),
    path('zalopay/status/<str:app_trans_id>/', ZaloPayOrderStatus.as_view(), name='zalopay_order_status'),
]
