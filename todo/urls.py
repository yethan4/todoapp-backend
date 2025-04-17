from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views 
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# /api/products/
urlpatterns = [
    path('register/', views.user_registration_view, name='register-user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.user_logout_view, name='logout-user'), 
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("user/", views.user_info_view, name="user-info"),
    
    path('tasks/', views.task_list_view, name='task-list'),
    path('tasks/<int:pk>/set-completed/', views.task_update_completed_view, name='task-set-completed'),
    path('tasks/<int:pk>/update/', views.task_update_view),
    path('tasks/<int:pk>/delete/', views.task_destroy_view, name='task-destroy'),
    
    path('lists/', views.list_create_view, name='list-create'),
    path('lists/<slug:slug>/', views.list_detail_destroy_view, name='list-detail-destroy'),
]