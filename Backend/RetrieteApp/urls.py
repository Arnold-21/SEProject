from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', myTokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/register/confirm/<int:code>/<int:id>/', RegisterConfirmView.as_view()),
    path('api/user/<int:id>/', UserDetailView.as_view()),
    path('api/recover/<int:code>/<int:id>/', UserPasswordChange.as_view()),
    path('api/recover/', UserPasswordGetCode.as_view()),
    path('api/privatelist/', PrivateBucketListView.as_view()),
    path('api/privatelist/<int:id>/', PrivateBucketListDetail.as_view()),
    path('api/privatelist/public/<int:id>/', PrivateToPublicHandler.as_view()),
    path('api/publiclist/', PublicListView.as_view()),
    path('api/admin/publiclist/', PublicAdminListView.as_view()),
    path('api/admin/publiclist/<int:id>/', PublicAdminListDetail.as_view()),
]

#Static api, to get the images
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)