from django.contrib import admin

# Register your models here.
from .models import ElevatorSystem,Elevator

class ElevatorAdmin(admin.StackedInline):
    model = Elevator


class ElevatorSystemAdmin(admin.ModelAdmin):
    inlines = [ElevatorAdmin]

admin.site.register(ElevatorSystem,ElevatorSystemAdmin)