from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *

# Create view to get the jwt auth token
class myTokenObtainPariView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
