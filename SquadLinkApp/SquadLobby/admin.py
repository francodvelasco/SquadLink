from django.contrib import admin
from .models import *

# Register your models here.


class LobbyAdmin(admin.ModelAdmin):
    model = SquadLinkLobby
    # list_display = [field.name for field in SquadLinkLobby._meta.get_fields()]
    list_display = ('squad_name',)


# class DepartmentAdmin(admin.ModelAdmin):
#     model = Department

#     list_display = ('dept_name',)


admin.site.register(SquadLinkLobby, LobbyAdmin)
# admin.site.register(Department, DepartmentAdmin)
