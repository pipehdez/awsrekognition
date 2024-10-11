from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from imagetotext.models import OcrAws
from imagetotext.serializers import OcrAwsSerializer

@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def upload_image(request, image, format=None):
    if request.method == 'POST':
        serializer = OcrAwsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)