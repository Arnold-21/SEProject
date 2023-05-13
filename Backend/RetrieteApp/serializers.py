from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Token serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['role'] = user.role

        return token