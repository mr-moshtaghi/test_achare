import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import User, Authenticator


@pytest.mark.django_db
def test_account():
    client = APIClient()
    url_ = reverse("auth:account")
    body = {"cellphone": "09908537607"}
    response = client.post(url_, json.dumps(body), content_type="application/json")
    content = json.loads(response.content)

    assert response.status_code == 200
    assert content.get('cellphone') == "09908537607"
    assert content.get('sms_verified') is False


@pytest.mark.django_db
def test_verify_cellphone(api_account):
    client = APIClient()
    url_ = reverse("auth:verify_cellphone", kwargs={'pk': api_account.temp_token})
    body = {"sms_token": api_account.sms_token}
    response = client.post(url_, json.dumps(body), content_type="application/json")
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content.get('cellphone') == "09908537607"
    assert content.get('sms_verified') is True







@pytest.mark.django_db
def test_login():
    user = User.objects.create_user(
        email="js@js.com", password="js.sj", cellphone="09908537607"
    )

    client = APIClient()
    url_ = reverse("auth:token")
    body = {"cellphone": user.cellphone, "password": "js.sj"}
    response = client.post(url_, json.dumps(body), content_type="application/json")
    auth = json.loads(response.content)
    access = auth.get("access")
    refresh = auth.get("refresh")

    assert access is not None
    assert type(access) == str

    assert refresh is not None
    assert type(refresh) == str
