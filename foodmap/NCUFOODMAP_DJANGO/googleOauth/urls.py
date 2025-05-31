from django.urls import path
from . import views

app_name = 'googleOauth'

urlpatterns = [
    path('', views.home, name='home'),  # 主頁
    path('login/', views.home, name='login'),  # 登入頁面
    path('logout/', views.logout_view, name='logout')  # 登出
]