import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import User, Authenticator
from authentication.tests.factories import BaseUserFactory


@pytest.fixture
def api_client():
    user = User.objects.create_user(email='test_user@js.com', password='pass@1test')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


@pytest.fixture
def api_account(db, transactional_db):
    client = APIClient()
    url_ = reverse("auth:account")
    body = {"cellphone": "09908537607"}
    response = client.post(url_, json.dumps(body), content_type="application/json")
    content = json.loads(response.content)
    return Authenticator.objects.filter(temp_token=content.get("temp_token")).first()


@pytest.fixture
def user1():
    return BaseUserFactory()


@pytest.fixture
def user2():
    return BaseUserFactory()
