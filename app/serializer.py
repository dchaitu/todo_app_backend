from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Task

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'






class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True
                                   ,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email','password','password2')
        # extra_kwargs =

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password didn't match"
            })
        return attrs

    def create(self, clean_data):

        clean_data.pop('password2')

        user_obj = User.objects.create(
            username=clean_data['username'],
            email=clean_data["email"],
        )
        user_obj.set_password(clean_data['password'])
        user_obj.save()
        return user_obj

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    recaptcha_token = serializers.CharField()

    # def check_user(self, clean_data):
    #     user = authenticate(username=clean_data["email"],
    #                         password=clean_data["password"])
    #
    #     if not user:
    #        raise ValidationError('User not Found')
    #     return user

class UserAddTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title','label', 'status', 'priority')


    def create(self, request):
        import random
        task_ids = list(Task.objects.values_list('task_id', flat=True))
        task_id = f'TASK-{random.randint(1000,9999)}'
        while task_id in task_ids:
            task_id = f'TASK-{random.randint(1000,9999)}'
        print(f'task_id:- {task_id}')
        # user = request['user']
        user = self.context['request'].user

        print(f"request['user']:_ {user.__dict__}")
        task = Task.objects.create(task_id=task_id,
                            title=request['title'],
                            label=request['label'],
                            status=request['status'],
                            priority=request['priority'],
                            user=user
                            )
        return task


