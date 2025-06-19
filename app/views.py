import json
from http.client import HTTPResponse

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.context_processors import request
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task, User
from .serializer import TaskSerializer, UserLoginSerializer, UserRegisterSerializer, UserAddTasksSerializer, \
    UserSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
# Create your views here.

# @api_view(["GET"])
# def get_data(request):
#     tasks = Task.objects.all()
#     serializers = TaskSerializer(tasks,many=True)
#     return Response(serializers.data)


# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'message': 'Login successful'}, status=200)
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=400)
#     return JsonResponse({'error': 'POST request required'}, status=400)


# @api_view(["GET"])
# def get_user_data(request):
#     print(f"request.user {request.user}")
#     # if request.user.is_authenticated:
#     user_tasks = Task.objects.all()
#     tasks = list(user_tasks.values())
#         # print(({'tasks':tasks, 'user':request.user}))
#     return JsonResponse({'tasks':tasks, 'user':request.user.username})


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
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user_obj = authenticate(username=username,password=password)
            if user_obj:
                # token, _ = Token.objects.get_or_create(user=user_obj)
                refresh = RefreshToken.for_user(user_obj)

                return Response({
                    'refresh': str(refresh),
                    'access':str(refresh.access_token),
                })


        return Response({'data':serializer.errors,
                         'message':"Credentials Not Valid",
                         }, status=401)


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

# call function to import json file
def import_json_data():
    f = open('tasks.json', 'r')
    data = json.load(f)
    tasks = [Task(
        task_id=item['id'],
        title=item['title'],
        label=item['label'],
        status=item['status'],
        priority=item['priority'],
    ) for item in data]
    Task.objects.bulk_create(tasks)


