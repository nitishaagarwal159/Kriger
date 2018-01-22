from time import time
from math import ceil

from django.contrib.auth import get_user_model, login
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from app.tokens import account_activation_token
from .models import Onetimelinks,Requests
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .models import UploadEmails,UploadPhoneNo,Posts,Likes,Shares


class usersSerializer(serializers.ModelSerializer):
   # uname = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model=User
        fields = ('username','id')





class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)



    def create(self, data):
         uname = serializers.ReadOnlyField(source='owner.username')

         user=get_user_model().objects.create(
            username=data['username']
         )


         user.set_password(data['password'])
         user.is_active=False
         user.save()
         return user

    class Meta:
             model = get_user_model()
             fields = ('username', 'password')


class EmailSerializer(serializers.ModelSerializer):
    email=serializers.CharField(label='Username',required=True,allow_blank=False)
    #pwd=serializers.CharField(label='Password',required=True,allow_blank=False)
    class Meta:
        model=User
        fields=[
            'email'
        ]
    def validate(self,data):
        user_obj = None
        email = data.get("email", None)
        user = User.objects.filter(Q(username=email))  # getting the details of the email
        if user.exists() and user.count() == 1:  # if the email exists
            for user in user:
                user = user
                t = ceil(time())  # timestsmp
                Onetimelinks.objects.filter(
                    code=user.pk).delete()  # if any email verifications are pending then the records will be deleted
                u = Onetimelinks(code=user.pk, token=t)  # saving present details
                u.save()
                t = str(t).encode()  # converting to byte
                subject = 'Reset link for password'  # subject of a mail
                message = render_to_string('app/account_activationlink_generation.html',
                                           {  # joins the below contet as a string
                                               'user': user,
                                               'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # encoding
                                               'token': urlsafe_base64_encode(force_bytes(t)),  # encoding
                                           })

                from_mail = settings.EMAIL_HOST_USER
                to_mail = [email]
                send_mail(subject, message, from_mail, to_mail, fail_silently=False)  # sending mail
        else:
            raise serializers.ValidationError(
                "Email is not registered or not valid")  # if the email is not found returns error
        return data

class UploademailSerializer(serializers.ModelSerializer):
    class Meta:
        model=UploadEmails
        fields=['email']

class UploadphoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=UploadPhoneNo
        fields=['phoneno']

class ReceiveRequestSerializer(serializers.ModelSerializer):
    username=serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model=User
        fields=['username','id']

class GetReceiveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Requests
        fields=[
            'requested_by_id',
            'By_name'
        ]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Posts
        fields=[ 'title','post']

class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Likes
        fields=['liked_post']

class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shares
        fields=['shared_post']





