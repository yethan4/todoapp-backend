from django.utils import timezone

from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken



from .models import CustomUser, Task, List
from .serializers import TaskSerializer, ListSerializer, UserRegistrationSerializer, UserLoginSerializer, CustomUserSerializer

# Create your views here.

class UserRegistrationAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)

user_registration_view = UserRegistrationAPIView.as_view()

# class UserLoginAPIView(generics.GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
        
#         refresh = RefreshToken.for_user(user)
        

#         refresh["username"] = user.username
#         refresh["email"] = user.email
        

#         access_token = refresh.access_token
        

#         response_data = {
#             "tokens": {
#                 "refresh": str(refresh),
#                 "access": str(access_token),
#             }
#         }
        
#         return Response(response_data, status=status.HTTP_200_OK)
    
# user_login_view = UserLoginAPIView.as_view()

class UserLogoutAPIView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
user_logout_view = UserLogoutAPIView.as_view()

class UserInfoAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        return self.request.user
    
user_info_view = UserInfoAPIView.as_view()

class TaskListAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.filter(user=user)
        
        date = self.request.query_params.get('date')
        task_list = self.request.query_params.get('task_list')
        if date or task_list:
            if date:
                queryset = queryset.filter(due_date=date)
            if task_list:
                queryset = queryset.filter(task_list=task_list)
        else:
            today = timezone.now().date()
            queryset = queryset.filter(due_date=today)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
task_list_view = TaskListAPIView.as_view()

class TaskSetCompletedAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found or you don't have permission."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        completed = request.data.get("completed")
        if completed is None:
            return Response(
                {"error": "'completed' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.completed = completed
        task.save(update_fields=['completed']) 
        
        return Response(
            {
                "id": task.pk,
                "completed": task.completed,
                "message": "Task status updated successfully"
            },
            status=status.HTTP_200_OK
        )

task_update_completed_view = TaskSetCompletedAPIView.as_view()

class TaskDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
task_destroy_view = TaskDestroyAPIView.as_view()

class ListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
list_create_view = ListCreateAPIView.as_view()
        
class ListDetailDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ListSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'slug'

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)

list_detail_destroy_view = ListDetailDestroyAPIView.as_view()