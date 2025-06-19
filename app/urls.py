from django.urls import path
from . import views

urlpatterns = [
    # path('', views.get_data),
    # path('/register'),
    path('login/', views.LoginAPI.as_view()),
    path('logout/', views.LogoutAPI.as_view()),
    path('tasks/', views.UserTasksAPI.as_view()),
    path('register/', views.RegisterUserAPI.as_view()),
    path('users/', views.UsersAPI.as_view()),
    # path('add/', views.add_data)
path('tasks/<int:user_id>/', views.UserTasksByIdAPI.as_view()),
    path('add/',views.AddUserTasks.as_view())

]