from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from app.utils import get_id_token_from_code, authenticate_or_create_user, exchange_code_for_token


class LoginWithGoogle(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        if 'code' in request.data.keys():
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
                             'username':user_email,
                             'first_name':id_token['given_name'],
                             'last_name':id_token['family_name'],
                             'picture':id_token['picture']
                             })


        return Response("ok")
