from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView


class AdminBaseAPIView(APIView):
    """
    Endpoint for booking acceptance.

    'id': int - customer booking id
    """

    permission_classes = [IsAuthenticated, IsAdminUser]