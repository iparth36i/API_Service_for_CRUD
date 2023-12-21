from datetime import timedelta
from django.db.models import Avg, Count, F
from django.utils import timezone
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError as DRFValidationError, APIException

from .models import Box

from .serializers import BoxSerializer

from .filters import BoxFilter

# Create your views here.

A1 = 100
L1 = 100
L2 = 50
V1 = 1000

class AreaExceededException(APIException):
    status_code = 400
    default_detail = f'Average area of all added boxes should not exceed {A1}.'
    default_code = 'area_exceeded'

class BoxesAddedInWeekExceededException(APIException):
    status_code = 400
    default_detail = f'Total boxes added in a week cannot be more than {L1}.'
    default_code = 'boxes_added_in_week_exceeded'

class BoxesAddedInWeekByUserExceededException(APIException):
    status_code = 400
    default_detail = f'Total boxes added in a week by a user cannot be more than {L2}.'
    default_code = 'boxes_added_in_week_by_user_exceeded'


class BoxAddView(generics.CreateAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        # Set the current user as the creator of the box
        serializer.save(user=self.request.user)

        # Check conditions after adding a box
        self.check_conditions_after_add()

    def check_conditions_after_add(self):
        # Implement condition 1: Average area of all added boxes should not exceed A1
        average_area = Box.objects.aggregate(avg_area=Avg(F('length') * F('breadth') * F('height')))['avg_area']
        if average_area is not None and average_area > A1:
            raise AreaExceededException()

        # Implement condition 3: Total Boxes added in a week cannot be more than L1
        current_week_start = timezone.now() - timedelta(days=timezone.now().weekday())
        boxes_added_this_week = Box.objects.filter(created_at__gte=current_week_start).count()
        if boxes_added_this_week > L1:
            raise BoxesAddedInWeekExceededException()
        
        boxes_added_this_week_by_user = Box.objects.filter(
            user=self.request.user, created_at__gte=current_week_start
        ).count()
        if boxes_added_this_week_by_user > L2:
            raise BoxesAddedInWeekByUserExceededException()

class BoxUpdateView(generics.UpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        # Exclude updating the creator and creation date
        serializer.validated_data.pop('user', None)
        serializer.validated_data.pop('created_at', None)
        serializer.save()

        # Check conditions after updating a box
        self.check_conditions_after_update()

    def check_conditions_after_update(self):
        # Implement condition 1: Average area of all added boxes should not exceed A1
        average_area = Box.objects.aggregate(avg_area=Avg(F('length') * F('breadth') * F('height')))['avg_area']
        if average_area is not None and average_area > A1:
            raise AreaExceededException()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Ensure that a staff user can update any box, but not creator or creation date
        if not request.user.is_staff:
            return Response({"detail": "You don't have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    

class BoxDeleteView(generics.DestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the requesting user is the creator of the box
        if request.user == instance.user:
            self.perform_destroy(instance)

            # Check conditions after deleting a box
            self.check_conditions_after_delete(request)
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You don't have permission to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)
        
    def check_conditions_after_delete(self, request):
        # Implement condition 1: Average area of all added boxes should not exceed A1
        average_area = Box.objects.aggregate(avg_area=Avg(F('length') * F('breadth') * F('height')))['avg_area']
        if average_area is not None and average_area > A1:
            raise AreaExceededException()

        # Implement condition 4: Total Boxes added in a week by a user cannot be more than L2
        current_week_start = timezone.now() - timedelta(days=timezone.now().weekday())
        boxes_added_this_week_by_user = Box.objects.filter(
            user=request.user, created_at__gte=current_week_start
        ).count()
        if boxes_added_this_week_by_user > L2:
            raise BoxesAddedInWeekByUserExceededException()
    

class BoxListView(generics.ListAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Box.objects.all()

        # Filtering logic based on query parameters
        length_more_than = self.request.query_params.get('length_more_than')
        length_less_than = self.request.query_params.get('length_less_than')
        breadth_more_than = self.request.query_params.get('breadth_more_than')
        breadth_less_than = self.request.query_params.get('breadth_less_than')
        height_more_than = self.request.query_params.get('height_more_than')
        height_less_than = self.request.query_params.get('height_less_than')
        area_more_than = self.request.query_params.get('area_more_than')
        area_less_than = self.request.query_params.get('area_less_than')
        volume_more_than = self.request.query_params.get('volume_more_than')
        volume_less_than = self.request.query_params.get('volume_less_than')
        created_by_username = self.request.query_params.get('created_by_username')
        created_after = self.request.query_params.get('created_after')
        created_before = self.request.query_params.get('created_before')

        # Apply filters
        if length_more_than:
            queryset = queryset.filter(length__gt=float(length_more_than))
        if length_less_than:
            queryset = queryset.filter(length__lt=float(length_less_than))
        if breadth_more_than:
            queryset = queryset.filter(breadth__gt=float(breadth_more_than))
        if breadth_less_than:
            queryset = queryset.filter(breadth__lt=float(breadth_less_than))
        if height_more_than:
            queryset = queryset.filter(height__gt=float(height_more_than))
        if height_less_than:
            queryset = queryset.filter(height__lt=float(height_less_than))
        if area_more_than:
            queryset = queryset.filter(area__gt=float(area_more_than))
        if area_less_than:
            queryset = queryset.filter(area__lt=float(area_less_than))
        if volume_more_than:
            queryset = queryset.filter(volume__gt=float(volume_more_than))
        if volume_less_than:
            queryset = queryset.filter(volume__lt=float(volume_less_than))
        if created_by_username:
            queryset = queryset.filter(user__username=created_by_username)
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)
        if created_before:
            queryset = queryset.filter(created_at__lte=created_before)

        return queryset
    

class MyBoxListView(generics.ListAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        # Only staff users can access their created boxes
        user = self.request.user
        queryset = Box.objects.filter(user=user)

        # Filtering logic based on query parameters
        length_more_than = self.request.query_params.get('length_more_than')
        length_less_than = self.request.query_params.get('length_less_than')
        breadth_more_than = self.request.query_params.get('breadth_more_than')
        breadth_less_than = self.request.query_params.get('breadth_less_than')
        height_more_than = self.request.query_params.get('height_more_than')
        height_less_than = self.request.query_params.get('height_less_than')
        area_more_than = self.request.query_params.get('area_more_than')
        area_less_than = self.request.query_params.get('area_less_than')
        volume_more_than = self.request.query_params.get('volume_more_than')
        volume_less_than = self.request.query_params.get('volume_less_than')

        # Apply filters
        if length_more_than:
            queryset = queryset.filter(length__gt=float(length_more_than))
        if length_less_than:
            queryset = queryset.filter(length__lt=float(length_less_than))
        if breadth_more_than:
            queryset = queryset.filter(breadth__gt=float(breadth_more_than))
        if breadth_less_than:
            queryset = queryset.filter(breadth__lt=float(breadth_less_than))
        if height_more_than:
            queryset = queryset.filter(height__gt=float(height_more_than))
        if height_less_than:
            queryset = queryset.filter(height__lt=float(height_less_than))
        if area_more_than:
            queryset = queryset.filter(area__gt=float(area_more_than))
        if area_less_than:
            queryset = queryset.filter(area__lt=float(area_less_than))
        if volume_more_than:
            queryset = queryset.filter(volume__gt=float(volume_more_than))
        if volume_less_than:
            queryset = queryset.filter(volume__lt=float(volume_less_than))

        return queryset

