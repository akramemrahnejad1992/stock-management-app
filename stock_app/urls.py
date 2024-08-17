from django.urls import path, include
from .views import register, user_login, user_logout, home, dashboard, stock_lists, stock_data_view
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, UserStockViewSet, generate_token



router = DefaultRouter()
router.register(r'stocks', StockViewSet, basename='stock')  # Stock viewset
router.register(r'user-stocks', UserStockViewSet, basename='user-stock')  # UserStock viewset

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/', home, name='home'),
    path('stocks/', stock_lists, name='stock_lists'),
    path('dashboard/', dashboard, name='dashboard'),
    path('select-new-stock/', stock_data_view, name='select-new-stock'),
    path('generate-token/', generate_token, name='generate_token'),
    path('api/', include(router.urls)),
]