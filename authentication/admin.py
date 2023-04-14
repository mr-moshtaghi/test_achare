from django.contrib import admin

from authentication.models import Authenticator, User, BanIp, BanCellphone


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'cellphone', 'first_name', 'last_name', 'is_staff'
    )
    search_fields = (
        'cellphone', 'first_name', 'last_name'
    )


class AuthenticatorAdmin(admin.ModelAdmin):
    list_display = ["cellphone"]


class BanIpAdmin(admin.ModelAdmin):
    list_display = ["ip_address", "ban_date_time"]


class BanCellphoneAdmin(admin.ModelAdmin):
    list_display = ["cellphone", "ban_date_time"]


admin.site.register(Authenticator, AuthenticatorAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(BanIp, BanIpAdmin)
admin.site.register(BanCellphone, BanCellphoneAdmin)
