import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.function_utilities import get_client_ip, check_ban_cellphone, wrong_attempt
from authentication.models import User, Authenticator
from authentication.permissions import IsIPBanned
from authentication.serializers import CellPhoneSerializer, AuthenticatorSerializer, VerifySmsTokenSerializer, \
    RegisterSerializer, LoginSerializer


class AccountViewSet(ViewSet):
    permission_classes = [IsIPBanned]
    authentication_classes = ()
    serializer_class = AuthenticatorSerializer
    queryset = Authenticator.objects.all()

    def account(self, request):
        serializer = CellPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cellphone = serializer.validated_data['cellphone']

        check_ban_cellphone(cellphone)

        user = User.objects.filter(cellphone=cellphone).first()

        if user:
            raise PermissionDenied(_('The user has already registered'))

        authenticator = self.queryset.filter(
            cellphone=cellphone,
            expired_at__gte=datetime.datetime.now()
        )

        if authenticator:
            raise PermissionDenied(_('The token has been sent to the desired phone number'))

        authenticator = Authenticator.objects.create(cellphone=cellphone)
        authenticator.send_verification_sms()

        return self.__response(authenticator)

    def verify_cellphone(self, request, pk):
        authenticator = self.queryset.filter(temp_token=pk).first()
        if not authenticator:
            raise NotFound('The requested object is not found.')

        if not check_ban_cellphone(authenticator.cellphone):
            raise PermissionDenied('Your IP has been banned')

        if not authenticator.can_verify_cellphone():
            raise PermissionDenied(_('You cannot verify cellphone at this time'))

        serializer = VerifySmsTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['sms_token'] != authenticator.sms_token:
            wrong_attempt(get_client_ip(request), authenticator.cellphone)
            raise PermissionDenied(_('The requested sms token is not valid or expired.'))

        authenticator.verify_cellphone()

        return self.__response(authenticator)

    def register(self, request, pk):
        authenticator = self.queryset.filter(temp_token=pk).first()
        if not authenticator:
            raise NotFound('The requested object is not found.')

        if not check_ban_cellphone(authenticator.cellphone):
            raise PermissionDenied('Your IP has been banned')

        if not authenticator.can_register():
            raise PermissionDenied(_('You cannot register at this time'))

        serializer = RegisterSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        authenticator.register_user(**serializer.validated_data)
        return self.__response(authenticator)

    def __response(self, authenticator):
        authenticator_serializer = self.serializer_class(authenticator)
        return Response(
            data=authenticator_serializer.data
        )


class GetTokenInSignUpView(TokenObtainPairView):
    permission_classes = (IsIPBanned,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not check_ban_cellphone(serializer.validated_data['cellphone']):
            raise PermissionDenied('Your IP has been banned')

        user = User.objects.filter(cellphone=serializer.validated_data['cellphone']).first()
        if not user:
            raise PermissionDenied('cellphone or password is not valid')

        if not user.check_password(serializer.validated_data['password']):
            wrong_attempt(get_client_ip(request), serializer.validated_data['cellphone'])
            raise PermissionDenied('cellphone or password is not valid')

        authenticate(user)
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(token, status=status.HTTP_200_OK)
