from django.contrib import admin
from .models import *

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    model = SquadLinkUserModel
    # list_display = [field.name for field in SquadLinkLobby._meta.get_fields()]
    list_display = ('user', 'id', 'user_id', 'game')

    def user_id(self, obj):
        return obj.user.id


admin.site.register(SquadLinkUserModel, UserProfileAdmin)
