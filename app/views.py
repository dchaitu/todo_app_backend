import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task
from .serializer import TaskSerializer, UserLoginSerializer, UserRegisterSerializer, UserAddTasksSerializer, \
    UserSerializer
from rest_framework.decorators import api_view

User = get_user_model()

class UserTasksAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print("request.user.is_authenticated "+ str(request.user.is_authenticated))
        tasks_query = Task.objects.filter(user=request.user)
        tasks_serializer = TaskSerializer(tasks_query, many=True)
        return Response({'tasks':tasks_serializer.data,
                         'user': {
                             "username":request.user.username,
                             "email":request.user.email
                            }
                         })

class RegisterUserAPI(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user_obj = authenticate(username=username,password=password)
            if user_obj:
                refresh = RefreshToken.for_user(user_obj)

                return Response({
                    'refresh': str(refresh),
                    'access':str(refresh.access_token),
                })
            else:
                return Response({'data':serializer.errors,
                                 'message':"Invalid Credentials",
                                 }, status=401)

        return Response(serializer.errors, status=400)


class UserTasksByIdAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)  # Fetch user by user_id
            print(f"user {user}")
            tasks_query = Task.objects.filter(user=user)
            tasks_serializer = TaskSerializer(tasks_query, many=True)
            return Response({
                'tasks': tasks_serializer.data,
                'user': {
                    "username": user.username,
                    "email": user.email
                }
            })
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class AddUserTasks(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddTasksSerializer
        # serializer.save()
        # return Response(serializer.data)



class LogoutAPI(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message':"Logged Out Successfully"})



class UsersAPI(APIView):
    def get(self, request):

        user_query  = User.objects.all()
        user = UserSerializer(user_query, many=True)
        return Response({"users":user.data})



# A
@api_view(["POST"])
def add_data(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response()




