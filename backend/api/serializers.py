from rest_framework import serializers
from .models import Post

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PostSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Post
        fields =  ('id', 'title', 'content','image')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','password']
        extra_kwargs={'password':{'write_only':True,'required':True}}
    
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        user=self.context['request'].user
        return user



# class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer()
    # class Meta:
        # model = User
        # fields = ['username', 'email', 'profile']

    # def create(self, validated_data):
        # profile_data = validated_data.pop('profile')
        # user = User.objects.create(**validated_data)
        # Profile.objects.create(user=user, **profile_data)
        # return user
