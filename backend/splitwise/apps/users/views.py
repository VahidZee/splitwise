from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes)
from rest_framework import status


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """
    Logs the requester user out!
    Returns status_code: 200 on success
    """
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)
