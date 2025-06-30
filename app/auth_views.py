from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from app.utils import get_id_token_from_code, authenticate_or_create_user


class LoginWithGoogle(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        if 'code' in request.data.keys():
            code = request.data['code']
            id_token = get_id_token_from_code(code)
            print(f"id_token is {id_token}")
            user_email = id_token['email']
            user = authenticate_or_create_user(user_email)
            token = AccessToken.for_user(user)
            return Response({'access_token': str(token), 'username':user_email})


        return Response("ok")
