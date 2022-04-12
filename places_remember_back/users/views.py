from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the model RemembersModels
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all memories
        for the currently authenticated user or administrator
        """
        user = self.request.user
        return User.objects.filter(id=user.id)
