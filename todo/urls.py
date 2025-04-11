from django.urls import path

from . import views 

# /api/products/
urlpatterns = [
    path('', views.task_list_view),
    path('<int:pk>/update/', views.task_update_view),
    path('<int:pk>/delete/', views.task_destroy_view)
]