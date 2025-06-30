from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = [
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('tasks/', views.UserTasksAPI.as_view()),
    path('register/', views.RegisterUserAPI.as_view()),
    path('users/', views.UsersAPI.as_view()),
    path('tasks/<int:user_id>/', views.UserTasksByIdAPI.as_view()),
    path('add/', views.AddUserTasks.as_view()),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),
    

]