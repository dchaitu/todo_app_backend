import json

import requests
import jwt
from urllib.parse import urlencode
from django.conf import settings
from app.models import User, Task


def validate_recaptcha(recaptcha_token):
    url = settings.RECAPTCHA_URL
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_token
    }

    response = requests.post(url, data=data)
    result = response.json()
    print(f"result is {result}")
    print(f"data is {data}")
    return result['success']


def get_id_token_from_code(code):
    token_endpoint = "https://oauth2.googleapis.com/token"
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    redirect_uri = "postmessage"

    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    body = urlencode(data)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(token_endpoint, data=body, headers=headers)

    if response.ok:
        token_data = response.json()
        id_token = token_data.get("id_token")
        return jwt.decode(id_token, verify=False, options={"verify_signature": False})
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return None


def authenticate_or_create_user(user_email):
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        user = User(username=user_email, email=user_email)
        user.save()
    return user


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