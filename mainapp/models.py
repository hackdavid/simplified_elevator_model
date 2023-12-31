from django.db import models

# Create your models here.
class ElevatorSystem(models.Model):
    name = models.CharField(max_length=100)
    number_of_floor = models.IntegerField()
    number_of_elevator = models.IntegerField()

    def __str__(self) -> str:
        return str(self.name)

class Elevator(models.Model):
    '''
    The Elevator class represents an elevator in an elevator system with attributes such as current
    floor, operational status, door status, and running status.
    '''
    class RunningStatus(models.IntegerChoices):
        GOING_UP = 1
        NOT_MOVING = 0
        GOING_DOWN = -1
    
    elevator_system = models.ForeignKey(ElevatorSystem, on_delete=models.CASCADE)
    elevator_number = models.IntegerField()
    current_floor = models.PositiveSmallIntegerField(default=0)
    is_operational = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=True)
    running_status = models.IntegerField(choices=RunningStatus.choices, default=RunningStatus.NOT_MOVING)
    
    def __str__(self) -> str:
        return f"Elevator Number {self.elevator_number}"


class ElevatorRequest(models.Model):
    '''
    The ElevatorRequest class represents a request made for an elevator to a specific floor with a
    destination floor and a timestamp.
    '''
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    requested_floor = models.PositiveSmallIntegerField()
    destination_floor = models.PositiveSmallIntegerField()
    request_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.elevator} is requested at floor {self.requested_floor}"
