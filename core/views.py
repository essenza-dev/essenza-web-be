from rest_framework.generics import GenericAPIView
from rest_framework import serializers
from rest_framework.permissions import AllowAny


class EmptySerializer(serializers.Serializer):
    pass


class BaseApiView(GenericAPIView):
    """
    Base API view with common functionality for all API views.
    """

    serializer_class = EmptySerializer
    authentication_classes = []
    permission_classes = [AllowAny]
