from rest_framework import generics, authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny, ]
    authentication_classes = (authentication.SessionAuthentication, authentication.TokenAuthentication,)


class ProtectedView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'message': 'This view should be only accessible with Barer Token'})


class ApiLogout(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'status': 'Successfully logged out'
        })
