from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
import random
import re

from .serializers import *
from .models import *

User = get_user_model()

#Registering a new user
# The function takes the neccessary information provided, and creates a new user
def saveUser(data):
    #Getting the neccessary data
    password = data["password"]
    email = data["email"]
    first_name = data["first_name"]
    last_name = data["last_name"]

    #Check if the email and the password is correct by the application standards
    try:
            validate_email(email)
    except ValidationError:
            return (True, "Incorrect email format")
    if not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password) or not re.search("[\.,\$\+]", password) or len(password) < 8:
        return (True, "Password need to contain a-z, A-Z, 0-9 and one of the following characters [.,$+]")
    
    #Check if the email already exists
    if User.objects.filter(email=email).count() != 0:
        User.objects.get(email=email).delete()
        return (True, "Email already exists!")
    
    #Creating a random number for the confirmation code, to activate the account at a later date
    random.seed(timezone.now().timestamp())
    confirmationCode = str(random.randint(a=100000, b=999999))
    confirmationTime = timezone.now()

    #Creating than saving the new user account, not activated as yet
    user = User(email=email)
    user.set_password(password)
    user.first_name=first_name
    user.last_name=last_name
    user.role = "Regular"
    user.confirmation_code=confirmationCode
    user.confirmation_start=confirmationTime
    user.is_active=False
    user.is_staff=False
    user.is_superuser=False
    user.save()

    #Sending the confirmation code via email
    send_mail(
        "Account Activation",
        "Your account's activation code: " + confirmationCode,
        "noreply@retriete.com",
        [user.email],
        fail_silently=False,
    )

    return (False, user.id)

#Given the confirmation code sent via email, active the account of the user
def confirmRegistration(code, id):
    #Checking if user object with given confirmation code exists
    try:
        user = User.objects.get(id=id)
    except:
        return (True, "Invalid activation Code")
    if user is None or user.confirmation_code != str(code):
        return (True, "User with given activation code not found")
    
    #Checking if the activation was within 10 minutes
    currentTime = timezone.now()
    if (currentTime - user.confirmation_start).total_seconds()/60 >= 10:
        user.delete()
        return (True, "Activation exceeded 10 minutes, register again")
    
    #Updating the user profile
    user.confirmation_code = None
    user.confirmation_start = None
    user.is_active = True
    user.save()
    return (False, "Activation Successfull")

#Change user data
def updateUser(data, id):
    #Check if neccesarry data is present
    if len(data) > 4:
        return (True, "Invalid data")
    permitted_data = ["first_name", "last_name", "email", "password"]
    for key in data.keys():
        if key not in permitted_data:
            return (True, "Invalid data")
        
    if data.get("email"):
        try:
            validate_email(data.get("email"))
        except ValidationError:
                return (True, "Incorrect email format")
         
    user = User.objects.get(id=id)
    serializer = UserSerializer(instance=user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    else: return (True, "Invalid data")
        
    return (False, "Update Succesfull")

#Send a password code via email
def sendRecoveryCode(email):
    #Check if email is in the database
    if email is None:
        return (True, "Email was not given")
    try:
        user = User.objects.get(email=email)
    except:
        return (True, "User with given email was not found")
    
    #Check if the user is active
    if not user.is_active:
        return (True, "User with given email was not found")
    
    #Get the code for the password reset
    random.seed(timezone.now().timestamp())
    confirmationCode = str(random.randint(a=100000, b=999999))
    confirmationTime = timezone.now()
    user.confirmation_code=confirmationCode
    user.confirmation_start=confirmationTime
    user.save()

    send_mail(
        "Password reset",
        "Your Password reset code: " + confirmationCode,
        "noreply@retriete.com",
        [user.email],
        fail_silently=False,
    )

    return (False, user.id)

#Change user data
def recoverPassword(data, id, code):
    #Check if neccesarry data is present and if it's correct
    if not data.get("password"):
        return (True, "Password not given")
    if not re.search("[a-z]", data.get("password")) or not re.search("[A-Z]", data.get("password")) or not re.search("[0-9]", data.get("password")) or not re.search("[\.,\$\+]", data.get("password")) or len(data.get("password")) < 8:
        return (True, "Password need to contain a-z, A-Z, 0-9 and one of the following characters [.,$+]")
         
    #Check user data, if the password can truly be changed
    user = User.objects.get(id=id)
    if user.confirmation_code != str(code) or user.confirmation_code is None:
        return (True, "Invalid authentification code given!")
    
    currentTime = timezone.now()
    if (currentTime - user.confirmation_start).total_seconds()/60 >= 10:
        user.confirmation_code = None
        user.confirmation_start = None
        return (True, "Password reset exceededed 10 minutes, try again")

    #Change the password
    user.set_password(data.get("password"))
    user.save()
        
    return (False, "Password changed Succesfull")

#Function to filter destination by private bucket list
def getPrivateBucketList(id, page):
    return DestinationSerializer(Destination.objects.filter(userID=id)[(page - 1)*20:page*20], many=True).data

#Function to change a destination to public list
def PrivateToPublic(id):
    #Get the object with given id
    dest: Destination = Destination.objects.get(id=id)
    if dest.isPublic == True:
        return (True, "Destination is already public")
    
    dest.isPublic = True
    dest.save()
    return (False, "Destination added to public list succesfully!")

#Function to filter the public pages
def getPublicList(page):
    return DestinationSerializer(Destination.objects.filter(isPublic=True)[(page - 1)*20:page*20], many=True).data

#Fucntion to save destination
def postDestinationHandler(request, id, version):
    data = request.data
    destData = {}
    destData["title"] = data.get("title")
    destData["description"] = data.get("description")
    destData["arrivalDate"] = data.get("arrivalDate")
    destData["leaveDate"] = data.get("leaveDate")
    destData["image"] = data.get("image")
    destData["location"] = id
    destData["userID"] = request.user.id
    if version == "Public":
        destData["isPublic"] = True

    print(destData)

    serializer = SimpleDestinationSerializer(data=destData)
    if serializer.is_valid():
        serializer.save()
        return (False, serializer.data)
    else:
        return (True, "Invalid parameters")
    
#Fucntion to update Destination
def putDestinationHandler(data, dest):
    destData = {}
    if data.get("title") is not None:
        destData["title"] = data.get("title")
    if data.get("description") is not None:
        destData["description"] = data.get("description")
    if data.get("arrivalDate") is not None:
        destData["arrivalDate"] = data.get("arrivalDate")
    if data.get("leaveDate") is not None:
        destData["leaveDate"] = data.get("leaveDate")
    if data.get("image") is not None:
        destData["image"] = data.get("image")
    if data.get("userID") is not None:
        destData["userID"] = data.get("userID")

    serializer = SimpleDestinationSerializer(instance=dest, data=destData, partial=True)
    if serializer.is_valid():
        serializer.save()
        return (False, serializer.data)
    else:
        return (True, "Invalid parameters")
    
#Fucntion to update Destination for Admin
def putAdminDestinationHandler(data, dest):
    destData = {}
    if data.get("title") is not None:
        destData["title"] = data.get("title")
    if data.get("description") is not None:
        destData["description"] = data.get("description")
    if data.get("arrivalDate") is not None:
        destData["arrivalDate"] = data.get("arrivalDate")
    if data.get("leaveDate") is not None:
        destData["leaveDate"] = data.get("leaveDate")
    if data.get("image") is not None:
        destData["image"] = data.get("image")
    if data.get("userID") is not None:
        destData["userID"] = data.get("userID")
    if data.get("isPublic") is not None:
        destData["isPublic"] = data.get("isPublic")

    serializer = SimpleDestinationSerializer(instance=dest, data=destData, partial=True)
    if serializer.is_valid():
        serializer.save()
        return (False, serializer.data)
    else:
        return (True, "Invalid parameters")
    
    
