from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from .views import UserViewSet,CustomAuthToken,PostView
# from django.conf.urls import  include



router=routers.DefaultRouter()
router.register('users',UserViewSet)
# router.register('posts',PostView,basename="posts_list")

urlpatterns = [
    path('posts/', views.PostView.as_view(), name= 'posts_list'),
    path('', include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
