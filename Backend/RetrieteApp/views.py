from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from .controller import *
from .permissions import *

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
    def get(self, request, code, id, *args, **kwargs):
        error, message = confirmRegistration(code, id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#User detail view, which handles get, put and delete requests
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, isUserObjectPermission]

    def put(self, request, id, *args, **kwargs):
        error, message = updateUser(request.data, id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View to send change password code
class UserPasswordGetCode(APIView):
    def post(self, request, *args, **kwargs):
        error, message = sendRecoveryCode(request.data.get("email"))
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)

#View to actually change the password
class UserPasswordChange(APIView):
    def put(self, request, id, code, *args, **kwargs):
        error, message = recoverPassword(request.data, id, code)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View for accessing private bucket list, get and post
class PrivateBucketListView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        #Check permission and if the page number was provided
        self.check_permissions(request=request)
        pageNumber = request.query_params.get("page")
        if pageNumber is None:
            return Response({'error': "No page number was given"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(getPrivateBucketList(request.user.id, int(pageNumber)), status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        #Add the user to the data, so the frontend doesn't need to send it
        geolocation = {}
        geolocation["country"] = request.data.get("country")
        geolocation["county"] = request.data.get("county")
        geolocation["settlement"] = request.data.get("settlement")
        geolocation["street"] = request.data.get("street")
        geolocation["number"] = request.data.get("number")
        id = 0

        serializer = GeolocationSerializer(data=geolocation)
        if serializer.is_valid():
            location = Geolocation.objects.create(country=request.data.get("country"), county=request.data.get("county"), settlement=request.data.get("settlement"),\
                                          street=request.data.get("street"), number=request.data.get("number"))
            location.save()
            id = location.id
        else:
            return Response({'error': "Incorrect geolocation"}, status=status.HTTP_400_BAD_REQUEST)
        

        error, message = postDestinationHandler(request, id, "Private")
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)
    

# View to update and delete a given bucket list
class PrivateBucketListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, usersDestinationPermission]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, id, *args, **kwargs):
        #Add the user to the data, so the frontend doesn't need to send it
        data = request.data
        geolocation = {}
        if data.get("country") is not None:
            geolocation["country"] = data.get("country")
        if data.get("county") is not None:
            geolocation["county"] = data.get("county")
        if data.get("settlement") is not None:
            geolocation["settlement"] = data.get("settlement")
        if data.get("street") is not None:
            geolocation["street"] = data.get("street")
        if data.get("number") is not None:
            geolocation["number"] = data.get("number")

        dest = Destination.objects.get(id=id)
        location = Geolocation.objects.get(id=dest.location.id)

        serializerLocation = GeolocationSerializer(instance=location, data=geolocation, partial=True)
        if serializerLocation.is_valid():
            serializerLocation.save()
        else:
            return Response({'error': "Incorrect geolocation"}, status=status.HTTP_400_BAD_REQUEST)
        

        error, message = putDestinationHandler(data, dest)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)


#View to add destination to public list
class PrivateToPublicHandler(APIView):
    permission_classes = [IsAuthenticated, usersDestinationPermission]

    def put(self, request, id, *args, **kwargs):
        self.check_permissions(request=request)

        error, message = PrivateToPublic(id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View to get public list for all users
class PublicListView(APIView):
    def get(self, request, *args, **kwargs):
        pageNumber = request.query_params.get("page")
        if pageNumber is None:
            return Response({'error': "No page number was given"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(getPublicList(int(pageNumber)), status=status.HTTP_200_OK)
    
#View for accessing private bucket list, get and post
class PublicAdminListView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated, isAdminRole]

    def get(self, request, *args, **kwargs):
        #Check permission and if the page number was provided
        self.check_permissions(request=request)
        pageNumber = request.query_params.get("page")
        if pageNumber is None:
            return Response({'error': "No page number was given"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(getPublicList(int(pageNumber)), status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        #Add the user to the data, so the frontend doesn't need to send it
         #Add the user to the data, so the frontend doesn't need to send it
        geolocation = {}
        geolocation["country"] = request.data.get("country")
        geolocation["county"] = request.data.get("county")
        geolocation["settlement"] = request.data.get("settlement")
        geolocation["street"] = request.data.get("street")
        geolocation["number"] = request.data.get("number")
        id = 0

        serializer = GeolocationSerializer(data=geolocation)
        if serializer.is_valid():
            location = Geolocation.objects.create(country=request.data.get("country"), county=request.data.get("county"), settlement=request.data.get("settlement"),\
                                          street=request.data.get("street"), number=request.data.get("number"))
            location.save()
            id = location.id
        else:
            return Response({'error': "Incorrect geolocation"}, status=status.HTTP_400_BAD_REQUEST)
        

        error, message = postDestinationHandler(request, id, "Public")
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)
    
# View to update and delete a given public list destination
class PublicAdminListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, isAdminRole]

    def put(self, request, id, *args, **kwargs):
        #Add the user to the data, so the frontend doesn't need to send it
        data = request.data
        geolocation = {}
        if data.get("country") is not None:
            geolocation["country"] = data.get("country")
        if data.get("county") is not None:
            geolocation["county"] = data.get("county")
        if data.get("settlement") is not None:
            geolocation["settlement"] = data.get("settlement")
        if data.get("street") is not None:
            geolocation["street"] = data.get("street")
        if data.get("number") is not None:
            geolocation["number"] = data.get("number")

        dest = Destination.objects.get(id=id)
        location = Geolocation.objects.get(id=dest.location.id)

        serializerLocation = GeolocationSerializer(instance=location, data=geolocation, partial=True)
        if serializerLocation.is_valid():
            serializerLocation.save()
        else:
            return Response({'error': "Incorrect geolocation"}, status=status.HTTP_400_BAD_REQUEST)
        

        error, message = putAdminDestinationHandler(data, dest)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)