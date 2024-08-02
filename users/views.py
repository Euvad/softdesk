from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # Allow any user to create accounts, restrict other operations
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Add custom behavior here if necessary
        age = serializer.validated_data.get('age', None)
        if age is not None and age < 15:
            raise serializers.ValidationError("Users must be at least 15 years old to register.")
        serializer.save()
