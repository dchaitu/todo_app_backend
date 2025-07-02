from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from app.models import User
from app.utils import get_id_token_from_code, authenticate_or_create_user, exchange_code_for_token


class LoginWithGoogle(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        if 'code' not in request.data:
            return Response({"error": "Code is required"}, status=400)

        code = request.data['code']
        print(f"code is {code}")
        id_token = get_id_token_from_code(code)
        if not id_token:
            return Response({"error": "Invalid code"}, status=400)
        print(f"id_token is {id_token}")
        user_email = id_token['email']
        user = authenticate_or_create_user(user_email, id_token)
        token = AccessToken.for_user(user)
        print("token is "+str(token))
        return Response({'access_token': str(token),
                         'username':user.username if user.username else '',
                         'first_name':id_token['given_name'],
                         'last_name':id_token['family_name'],
                         'email':id_token['email'],
                         'picture':id_token['picture'],
                         'username_set': bool(user.username)
                         })


class GoogleUsername(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print("User data:", request.data)
        username = request.data.get('username')
        if username is None:
            return Response({'error': 'Username is required'})

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        user = request.user

        if isinstance(user, AnonymousUser):
            return Response({"error": "User not authenticated"}, status=401)

        user.username = username
        user.save()

        return Response({
            "username": user.username,
            "message": "Username updated successfully",
        })