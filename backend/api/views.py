from .serializers import PostSerializer,UserSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


# FOR CREATING USERS.
from rest_framework import viewsets
from django.contrib.auth.models import User

#to view post of login user
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class PostView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request, *args, **kwargs):
        # permission_classes = [IsAuthenticatedOrReadOnly]
        # authentication_classes = (TokenAuthentication,)
        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # permission_classes = [IsAuthenticated]
        # authentication_classes = (TokenAuthentication,)
        posts_serializer = PostSerializer(data=request.data)
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class = UserSerializer
    # def get_object(self):
        # pk = self.kwargs.get('pk')
        # if pk == "current":
            # return self.request.user
        # return super(UserViewSet, self).get_object()


# class CurrentViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # def get_object(self):
        # pk = self.kwargs.get('pk')
        # if pk == "current":
            # return self.request.user
        # return super(UserViewSet, self).get_object()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
            # 'username':user.Username
        })


# class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()
# 
    # class Meta:
        # model = User
        # fields = ['username', 'email', 'profile']
# 
    # def create(self, validated_data):
        # profile_data = validated_data.pop('profile')
        # user = User.objects.create(**validated_data)
        # Profile.objects.create(user=user, **profile_data)
        # return user