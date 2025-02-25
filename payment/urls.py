from django.urls import path
from . import views

urlpatterns = [
	path('payment_success/', views.payment_success, name="payment"),
	path('check_out/', views.checkout, name="checkOut"),
	path('billing_info/', views.billing_info, name="billing_info"),
	path('processor_order/', views.processor_order, name="processor_order"),
	path('shipped_dash/', views.shipped_dash, name="shipped_dash"),
	path('not_shipped_dash/', views.not_shipped_dash, name="not_shipped_dash"),
	path('orders/<int:pk>', views.orders, name="orders"),
]
