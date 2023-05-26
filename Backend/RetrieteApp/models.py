from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime
import os

# Creating user model and usermanager, (usermanager for django cli usercreation)
class UserManager(BaseUserManager):
    #Creating a normal user, with role: Regular, with neccessary information for the user
    def create_user(self, first_name: str, last_name: str, email: str, role: str = "Regular", password: str = None, is_staff: bool = False, is_superuser: bool = False):
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first_name")
        if not last_name:
            raise ValueError("User must have a last_name")
        
        user = self.model(email = self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.role = role
        user.is_active = True
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user
    
    #Creating an admin user, with the neccesary information and role: Admin
    def create_superuser(self, first_name: str, last_name: str, email: str, password: str):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role="Admin",
            password=password,
            is_staff=True,
            is_superuser=True
        )
        user.save()

        return user

#The custom User django model:
    # First_name, last_name, role for user detail
    # Email, password is for authentification
    # Confirmation_code, confirmation_start is used for both the registration and account recovery
class User(AbstractUser):
    class Role(models.TextChoices):
        REGULAR = "Regular", 'Regular'
        Admin = "Admin", 'Admin'

    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    username = None
    role = models.CharField(max_length=30, choices=Role.choices, default='Regular')
    confirmation_code = models.CharField(max_length=20, blank=True, null=True)
    confirmation_start = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name"]


#Helper function for creating the filepath, with the help of the relative path to the images folder, and time + name for avoiding naming conflicts
def filepath(request, filename):
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    name = "%s%s" % (timeNow, filename)
    return os.path.join('images/', name)

#Geolocaton model
class Geolocation(models.Model):
    country = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    settlement = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=100)

#Destination model
class Destination(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    arrivalDate = models.DateField()
    leaveDate = models.DateField()
    image = models.ImageField(upload_to=filepath, default='images/default.jpg')
    isPublic = models.BooleanField(default=False)
    userID = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True)
    location = models.ForeignKey(Geolocation, related_name="location", on_delete=models.CASCADE, null=True)