
from django.urls import path
from .views import (
    ElevatorSystemViewset,
    ElevatorViewSet
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'system', ElevatorSystemViewset, basename='system')

urlpatterns = [
    path('system/<int:pk>/show_elevators/', ElevatorSystemViewset.as_view({'get': 'show_elevators'}), name='elevator-system-show-elevators'),
    path('system/<int:id>/elevator/<int:pk>/', ElevatorViewSet.as_view({'get': 'show', 'put': 'custom_update', 'patch': 'custom_update'}), name='elevator-show'),
    path('system/<int:id>/elevator/<int:pk>/make_request/', ElevatorViewSet.as_view({'post': 'make_request'}), name='elevator-make-request'),
    path('system/<int:id>/elevator/<int:pk>/destination/', ElevatorViewSet.as_view({'get': 'destination'}), name='elevator-destination'),
    path('system/<int:id>/elevator/<int:pk>/mark_elevator_under_maintainance/', ElevatorViewSet.as_view({'get': 'mark_elevator_under_maintainance'}), name='elevator-is-operational'),
    path('system/<int:id>/elevator/<int:pk>/open_or_close_door/', ElevatorViewSet.as_view({'get': 'open_or_close_door'}), name='elevator-open-or-close_door'),
    path('system/<int:id>/elevator/<int:pk>/moving_diretion/', ElevatorViewSet.as_view({'get': 'moving_diretion'}), name='elevator-direction'),
    path('system/<int:id>/elevator/<int:pk>/req_current_status/', ElevatorViewSet.as_view({'get': 'req_current_status'}), name='elevator-req-current-status'),
] + router.urls

'''
URLs:-
GET/POST: api/system- show all elevator systems or add an elevator system

GET: api/system/{elevator-system-id}/show_elevators- Given an elevator system list all the elevators and their status.

GET/PUT: api/system/{elevator-system-id}/elevator/{elevator-number}/- view and update the details of any elevator of the system

POST: api/system/{elevator-system-id}/elevator/{elevator-number}/make_request- Create a new request for a specific elevator, given its elevator system and elevator number

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/destination- Fetch the next destination floor for a given elevator

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/moving_diretion- Fetch the moving direction for a given elevator

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/mark_elevator_under_maintainance- Fetch the Elevator is operational or not

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/open_or_close_door- Close/Open the Door 

GET: api/system/{elevator-system-id}/elevator/{elevator-number}/req_current_status- List all the requests for a given elevator. Requests already served can be filtered with is_active parameter set false, This is a URL parameter.
'''
