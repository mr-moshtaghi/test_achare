import datetime

from django.core.cache import cache
from rest_framework.permissions import BasePermission

from authentication.function_utilities import get_client_ip
from authentication.models import BanIp


class IsIPBanned(BasePermission):
    message = 'Your IP has been banned'

    def has_permission(self, request, view):
        return not cache.get(f"ban_{get_client_ip(request)}")

        # return not BanIp.objects.filter(
        #         ip_address=get_client_ip(request),
        #         ban_date_time__gte=datetime.datetime.now()).first()



