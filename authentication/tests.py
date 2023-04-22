import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import User

from django.urls import reverse



# @pytest.mark.parametrize(
#     'text_input, result', [('5+5', 10), ('1+4', 5)]
# )
# def test_sum(text_input, result):
#     print("&" * 200)
#     print(text_input)
#     print("&" * 200)
#     assert eval(text_input) == result
#
#
# @pytest.mark.parametrize([
#    ('gr', 'Yasou'),
#    ('de', 'Guten tag'),
#    ('fr', 'Bonjour')
# ])
# def test_languages(language_code, text):
#     print(language_code)


#
# @pytest.mark.django_db
# def test_user_create():
#     User.objects.create_user('lennon@thebeatles.com', 'johnpassword')
#     assert User.objects.count() == 1
#
#
# @pytest.mark.django_db
# def test_view(client):
#     print(client)
#     url = reverse('auth:account')
#     response = client.post(url)
#     print(response.data)
#     assert response.status_code == 400
#
#
# import uuid
#
# import pytest
#
#
# @pytest.fixture
# def test_password():
#     return 'strong-test-pass'
#
#
# @pytest.fixture
# def create_user(db, django_user_model, test_password):
#     def make_user(**kwargs):
#         kwargs['password'] = test_password
#         return django_user_model.objects.create_user(**kwargs)
#     return make_user
#
#
# @pytest.mark.django_db
# def test_user_detail(client, create_user):
#     user = create_user(email='someone@gmail.com')
#     assert user
#
#
# @pytest.mark.django_db
# def test_auth_view(client, create_user, test_password):
#     user = create_user(email="s@gmail.com")
#     url = reverse('auth-url')
#     client.login(
#         username=user.username, password=test_password
#     )
#     response = client.get(url)
#     assert response.status_code == 200
