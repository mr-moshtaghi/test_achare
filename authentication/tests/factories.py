import factory

from authentication.models import User


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Iterator(['fr@gmail.com', 'it@gmail.com', 'es@gmail.com'])
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')
