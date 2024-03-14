from django.urls import path, include
from . import views
from .views import TransactionList, TransactionDetail


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login, name='login'),
    path('api/logout/', views.logout, name='logout'),
    path('api/transactions/', TransactionList.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionDetail.as_view(), name='transaction_detail'),
    path('dashboard/', views.transaction_dashboard, name='transaction_dashboard'),
]
