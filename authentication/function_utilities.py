import datetime

from django.core.cache import cache
from django.utils import timezone

from achare import settings
from authentication.models import BanCellphone, BanIp


def get_client_ip(request):
    x_forwarded_for = request.META.get('IP_FORWARDED_FOR_HEADER')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_key_wrong_attempt(key):
    return f"wrong_{key}_attempt"


def wrong_attempt_object(el):
    key = get_key_wrong_attempt(el)
    if not cache.get(key):
        cache.set(key, 0)
    result = cache.incr(key, 1)

    if result > 3:
        cache.delete(key)
        cache.set(f"ban_{el}", True, 60 * 60 * 60)


def wrong_attempt(ip_address, cellphone):
    wrong_attempt_object(ip_address)
    wrong_attempt_object(cellphone)

    # ban_cellphone = BanCellphone.objects.filter(
    #     cellphone=cellphone,
    #     ban_date_time__isnull=True
    # ).first()
    # if not ban_cellphone:
    #     ban_cellphone = BanCellphone.objects.create(cellphone=cellphone)
    #
    # ban_cellphone.number_of_try = ban_cellphone.number_of_try + 1
    # ban_cellphone.save()
    #
    # if ban_cellphone.number_of_try >= settings.NUMBER_OF_TRY_FOR_BAN:
    #     ban_cellphone.ban_date_time = timezone.now() + timezone.timedelta(minutes=settings.BAN_TIME_USER)
    #     ban_cellphone.save()
    #
    # ban_ip = BanIp.objects.filter(
    #     ip_address=ip_address,
    #     ban_date_time__isnull=True
    # ).first()
    #
    # if not ban_ip:
    #     ban_ip = BanIp.objects.create(ip_address=ip_address)
    #
    # ban_ip.number_of_try = ban_ip.number_of_try + 1
    # ban_ip.save()
    #
    # if ban_ip.number_of_try >= settings.NUMBER_OF_TRY_FOR_BAN:
    #     ban_ip.ban_date_time = timezone.now() + timezone.timedelta(minutes=settings.BAN_TIME_USER)
    #     ban_ip.save()


def check_ban_cellphone(cellphone):
    # check cellphone
    if cache.get(f"ban_{cellphone}"):
        return False
    return True
