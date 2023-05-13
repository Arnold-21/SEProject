from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
import random
import re

from .serializers import UserSerializer

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
    permitted_data = ["first_name", "last_name", "email"]
    for key in data.keys():
         if key not in permitted_data:
              return (True, "Invalid data")
         
    user = User.objects.get(id=id)
    serializer = UserSerializer(instance=user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    else: return (True, "Invalid data")
        
    return (False, "Update Succesfull")