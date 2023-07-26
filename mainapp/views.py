from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from mainapp.models import (
    ElevatorSystem,
    Elevator,
    ElevatorRequest
)
from mainapp.serializer import (
    ElevatorSystemSerializer,
    ElevatorSerializer,
    ElevatorRequestFullSerializer,
    ElevatorRequestSerializer
)
from mainapp.utils.initalize_elevator import initalize_elevators
# Create your views here.

class ElevatorSystemViewset(viewsets.ViewSet):
    """
        This is a Django view that creates an elevator system and initiates elevators, and also shows
        the elevators associated with a particular elevator system.
        
        :param request: The HTTP request object that contains information about the request being made,
        such as the HTTP method, headers, and data
        :return: The code is a part of a Django REST framework viewset.
    """
    queryset = ElevatorSystem.objects.all()
    serializer_class = ElevatorSystemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        elevator_system = serializer.save()
        initalize_elevators(
            number_of_elevators=serializer.data['number_of_elevator'],
            system_id=elevator_system.id
        )
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def show_elevators(self, request, pk=None):
        system_id = self.kwargs['pk']
        system_obj = ElevatorSystem.objects.get(id=system_id)
        elevators = Elevator.objects.filter(elevator_system=system_obj)
        serializer = ElevatorSerializer(elevators, many=True)
        return Response(serializer.data)

class ElevatorViewSet(viewsets.ModelViewSet):
    """
       This is Django Viewset based Rest_api for the Elevator system .
       This Repo consists of all the api end_point which was mention in urls.py or Readme file uploaded into
       Github and also Demo for this repo as video has been uploaded to github so
       please get reference from that in-case of any confusion.
    """
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['get'])
    def show(self, request, id=None, pk=None):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        elevator = Elevator.objects.get(elevator_system_id=system_id, elevator_number=elevator_number)
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data)


    @action(detail=True, methods=['put', 'patch'])
    def custom_update(self, request, id=None, pk=None):
        system_id = self.kwargs['id']
        elevator_number = self.kwargs['pk']
        elevator = Elevator.objects.get(elevator_system__id=system_id, elevator_number=elevator_number)
        serializer = ElevatorSerializer(elevator, data=request.data, partial=True)  # `partial=True` allows partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    @action(detail=True, methods=['get'])
    def destination(self, request, id=None, pk=None):
        elevator = self.get_object()

        if not elevator.is_operational:
            return Response({'running': False, 'details': 'The Elevator is not operational'})

        requests_pending = ElevatorRequest.objects.filter(elevator=elevator, is_active=True).order_by('request_time')

        if requests_pending.count() == 0:
            return Response({'running': False, 'details': 'The Elevator is not running currently, No pending requests'})

        if requests_pending[0].requested_floor == elevator.current_floor:
            return Response({'running': True, 'details': str(requests_pending[0].destination_floor)})

        return Response({'running': True, 'details': str(requests_pending[0].requested_floor)})
    
    @action(detail=True, methods=['get'])
    def mark_elevator_under_maintainance(self, request, id=None, pk=None):
        elevator = self.get_object()

        if not elevator.is_operational:
            return Response({'running': False, 'details': 'The Elevator had already in under maintanance so we cannot mark it'})
        else:
            elevator.is_operational = False
            elevator.save()
            return Response({'running': True, 'details': 'Marked this elevator is under maintainance sucessully'})

    @action(detail=True, methods=['get'])
    def open_or_close_door(self, request, id=None, pk=None):
        elevator = self.get_object()

        if elevator.is_door_open:
            elevator.is_door_open = False
            elevator.save()
            return Response({'running': True, 'details': 'Elevator Door is Closed Successully because its door was open'})
        else:
            elevator.is_door_open = True
            elevator.save()
            return Response({'running': True, 'details': 'Elevator Door is opend successfully becaise it was Closed '})

    @action(detail=True,methods=['get'])
    def moving_diretion(self,request,id=None,pk=None):
        """
        this will fetch moving direction of an elevator 
        GOING_UP = 1
        NOT_MOVING = 0
        GOING_DOWN = -1
        Response will be in integer for now but it can be mapped with any values if needed based on 
        business requirement
        """
        elevator = self.get_object()
        if not elevator.is_operational:
            return Response({'running': False, 'details': 'The Elevator is not operational'})
        requests_pending = ElevatorRequest.objects.filter(elevator=elevator, is_active=True).order_by('request_time')

        if requests_pending.count() == 0:
            return Response({'running': False, 'details': 'The Elevator is not running currently, No pending requests'})

        return Response({'running': True, 'Moving Direction': elevator.running_status})
        
    @action(detail=True, methods=['get'])
    def req_current_status(self, request, id=None, pk=None):
        elevator = self.get_object()
        elevator_requests = elevator.elevatorrequest_set.all()
        serializer = ElevatorRequestFullSerializer(elevator_requests, many=True)
        return Response(serializer.data)

    
    @action(detail=True, methods=['post'])
    def make_request(self, request, id=None, pk=None):
        elevator = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(elevator=elevator)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    def get_serializer_class(self):
        if self.action == 'make_request':
            return ElevatorRequestSerializer
        return super().get_serializer_class()

