from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from remembers.models import RemembersModel
from remembers.permissions import IsOwnerOrSuperUser
from remembers.serializers import RemembersSerializer


class RemembersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the model RemembersModels
    """
    queryset = RemembersModel.objects.all()
    serializer_class = RemembersSerializer
    bbox_filter_include_overlapping = True
    permission_classes = [IsOwnerOrSuperUser]
    filter_backends = SearchFilter, OrderingFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def get_queryset(self):
        """
        This view should return a list of all memories
        for the currently authenticated user or administrator
        """
        user = self.request.user
        if user.is_staff:
            return RemembersModel.objects.all()
        else:
            return RemembersModel.objects.filter(user=user)
