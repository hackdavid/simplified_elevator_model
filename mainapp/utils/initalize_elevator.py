from mainapp.models import Elevator, ElevatorSystem

def initalize_elevators(number_of_elevators: int, system_id: int):
    elevator_system_obj = ElevatorSystem.objects.get(id=system_id)
    for i in range(number_of_elevators):
        elevator_object = Elevator.objects.create(
            elevator_system=elevator_object,
            elevator_number=i + 1,
        )
    print("Elevator initiation completed")
