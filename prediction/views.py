from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def predict(request, message, format=None):
    """
    Predict the content of an image.
    """
    return Response({"message": message}, status=status.HTTP_200_OK)

