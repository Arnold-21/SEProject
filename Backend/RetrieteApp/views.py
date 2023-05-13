from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from .controller import *

User = get_user_model()

# Create view to get the jwt auth token
# Gets the custom token serializer, which will put the neccessary information in the token for the frontend client
class myTokenObtainPariView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# View to register a new account and to activate it
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        error, message = saveUser(request.data)
        if error:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
class RegisterConfirmView(APIView):
    def get(self, request, code, *args, **kwargs):
        error, message = confirmRegistration(code)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#User detail view, which handles get, put and delete requests
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def put(self, request, id, *args, **kwargs):
        error, message = updateUser(request.data, id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)