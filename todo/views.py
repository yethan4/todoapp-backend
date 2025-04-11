from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_list_or_404

from .models import Task
from .serializers import TaskSerializer

# Create your views here.

class TaskListAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    #permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')
        
        if start and end:
            queryset = queryset.filter(due_date__range=[start, end])
        
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(due_date__date=date)
            
        queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
task_list_view = TaskListAPIView.as_view()

class TaskUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

task_update_view = TaskUpdateAPIView.as_view()

class TaskDestroyAPIView(generics.DestroyAPIView):

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
task_destroy_view = TaskDestroyAPIView.as_view()

