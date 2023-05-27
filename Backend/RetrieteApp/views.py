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
class myTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# View to register a new account and to activate it
# Creates a new account, which is not activated, so it cannot be used, until confirmation
# It either gives back a an error message, if some information is not correct, or success, with the user id, if everything went according to plan
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        error, message = UserController.saveUser(request.data)
        if error:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View to confirm an account, gets the user id, and the code, sent to email via the url
#If the user id and code doesnt match an error message is sent to the frontend
#Othervise a success is sent
class RegisterConfirmView(APIView):
    def get(self, request, code, id, *args, **kwargs):
        error, message = UserController.confirmRegistration(code, id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#User detail view, which handles get, put and delete requests
#The functionalities handled by the view, are account_modification, account_deletion and seeing account_detail
#The account holder only, has permission to theese functionalities
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticated, isUserObjectPermission]

    def put(self, request, id, *args, **kwargs):
        error, message = UserController.updateUser(request.data, id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View to recover an account
#The user gives an email, if the email has an account attached, a code will be sent to the email, and a success message as response
#If the email doesnt have an account attached, an error message will be sent back
class UserPasswordGetCode(APIView):
    def post(self, request, *args, **kwargs):
        error, message = UserController.sendRecoveryCode(request.data.get("email"))
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)

#The view gets the code and user id from url, and a password in the request body
#If the id and code doesnt match, and error will be sent back
#Otherwise the password will be changed, and a success message will be sent back
class UserPasswordChange(APIView):
    def put(self, request, id, code, *args, **kwargs):
        error, message = UserController.recoverPassword(request.data, id, code)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View which handles the get and post requests for a private bucket list
#Only authenticated users can get access to these functionalities
class PrivateBucketListView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    #If the page number is not given, an appropiate error message will be sent back
    #Otherwise the users destinations
    def get(self, request, *args, **kwargs):
        #Check permission and if the page number was provided
        self.check_permissions(request=request)
        pageNumber = request.query_params.get("page")
        if pageNumber is None:
            return Response({'error': "No page number was given"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DestinationController.getPrivateBucketList(request.user.id, int(pageNumber)), status=status.HTTP_200_OK)
    
    #Post request first checks if all given data is valid, than creates the objects for the destination
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
        

        error, message = DestinationController.postDestinationHandler(request, id, "Private")
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)
    

# View to update, delete and see a given bucket list
#Only the users whose destinations are under question can change these parts
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
        

        error, message = DestinationController.putDestinationHandler(data, dest)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)


#View to add destination to public list
#Only the users which are the owners of the destination object can access this functionality
#If something fails, and appropiate error message is sent, otherwise a success message
class PrivateToPublicHandler(APIView):
    permission_classes = [IsAuthenticated, usersDestinationPermission]

    def put(self, request, id, *args, **kwargs):
        self.check_permissions(request=request)

        error, message = DestinationController.PrivateToPublic(id)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": message}, status=status.HTTP_200_OK)
    
#View to get public list for all users
#If something fails, and appropiate error message is sent, otherwise the destination list
class PublicListView(APIView):
    def get(self, request, *args, **kwargs):
        pageNumber = request.query_params.get("page")
        if pageNumber is None:
            return Response({'error': "No page number was given"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DestinationController.getPublicList(int(pageNumber)), status=status.HTTP_200_OK)
    
#View for accessing the public destination list, with get and post requests
#These functionalities are only available for admin users
class PublicAdminListView(generics.ListCreateAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated, isAdminRole]

    #If something fails, and appropiate error message is sent, otherwise the destination list
    def get(self, request, *args, **kwargs):
        #Check permission and if the page number was provided
        self.check_permissions(request=request)
        pageNumber = request.query_params.get("page")
        if pageNumber is None:
            return Response({'error': "No page number was given"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(DestinationController.getPublicList(int(pageNumber)), status=status.HTTP_200_OK)
    
    #Checks if everything is correct with the sent data, if not an error message is sent, otherwise the created destination list
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
        

        error, message = DestinationController.postDestinationHandler(request, id, "Public")
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)
    
# View to update, delete and see a given public list destination
#Theses functionalities are onlly available to admin users
#If something fails, and appropiate error message is sent, otherwise the appropiate response
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
        

        error, message = DestinationController.putAdminDestinationHandler(data, dest)
        if error:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_200_OK)