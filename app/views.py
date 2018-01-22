from time import time
from math import ceil, floor

from django.db.models import Q
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from app import serializers
from .models import Onetimelinks,Requests,Posts,Likes,Shares,UploadPhoneNo,UploadEmails
from .serializers import usersSerializer,UserRegisterSerializer,EmailSerializer,UploademailSerializer,UploadphoneSerializer,ReceiveRequestSerializer,PostCreateSerializer,LikeCreateSerializer,ShareSerializer,GetReceiveRequestSerializer
from django.contrib.auth.models import User

# Create your views here.

class UserList(ListAPIView):
   serializer_class = usersSerializer
   def get_queryset(self):
        # pass
        query = User.objects.all()
        #serializer = usersSerializer(query, many=True)
        return query


class CreateUserView(APIView):
    #create APIView provide only post method
    model=get_user_model()

    permission_classes = (AllowAny,)
    #serializer_class=UserRegisterSerializer

    def post(self,request,*args,**kwargs):
        data=request.data
        serializer=UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            new_data=serializer.data
            return Response(new_data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)



def verify_link(request,code,token):
    code=urlsafe_base64_decode(force_bytes(code))
    code=code.decode()
    code=int(code)
    token=urlsafe_base64_decode(force_bytes(token))
    token=token.decode()
    requested_time=int(token)
    present_time=int(ceil(time()))
    time_btwn = present_time - requested_time
    time_btwn = floor(time_btwn / 60)
    if (time_btwn >= 500):
        return HttpResponse(' 1 the link is expired or used')
    activelinks = Onetimelinks.objects.all().filter(Q(code=code)).filter(Q(token=token))
    if activelinks.exists():
                u = User.objects.get(pk=code)
                u.is_active=True
                u.save()
                Onetimelinks.objects.filter(code=u.pk).delete()
                return HttpResponse('You can now sign in with your new account')
    else:
                        return HttpResponse('the link is expired or already used')

class SendConfirmation(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = EmailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class UploademailAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploademailSerializer

    def perform_create(self,serializer):
        serializer.save(username=self.request.user)

class GetUploademailAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploademailSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=UploadEmails.objects.filter(username=user)
        return queryset

class UploadphoneAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadphoneSerializer

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)

class GetUploadphoneAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadphoneSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=UploadPhoneNo.objects.filter(username=user)
        return queryset

class storereceivereqAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=ReceiveRequestSerializer
    def post(self,request,*args,**kwargs):
        user=self.request.user.id #id of basic Auth user
        data=request.data
        user_from=int(data['username'])
        if(user_from==user):
            return Response("Error in receiving request")
        else:
            x=User.objects.get(id=user)

            x1=x.username
            y=User.objects.get(id=user_from)
            y1=y.username
            pre_req=Requests.objects.all().filter(requested_by_id=y).filter(requested_to_id=x)
            if pre_req.exists():
                return Response('Request already received')
            else:
                Requests.objects.create(requested_by_id=y,By_name=y1,requested_to_id=x,to_name=x1)
                return Response('Request received')

class getreceivereqAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetReceiveRequestSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=Requests.objects.filter(requested_to_id=user)
        return queryset

class createpostAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        t = datetime.datetime.now()  # getting the present time
        serializer.save(username=self.request.user, date=t,
                        name=self.request.user.username)  # saving the instance of the post

class likecreatedAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Likes.objects.all()
    serializer_class = LikeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(liked_by=self.request.user,liked_by_name=self.request.user.username)

class shareAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Shares.objects.all()
    serializer_class = ShareSerializer

    def perform_create(self, serializer):
        serializer.save(shared_by=self.request.user,shared_by_name=self.request.user.username)

class numoflikes(APIView):
    permission_classes = [AllowAny,]
    def get(self,request,*args,**kwargs):
      like1 = self.kwargs['titleofpost']
      id1 = Likes.objects.filter(liked_post=like1)
      count = id1.count()
      return Response({"no_of_likes": count})

class numofshares(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        share1 = self.kwargs['titleofpost']
        id1 = Shares.objects.filter(shared_post=share1)
        count = id1.count()
        return Response({"no_of_shares": count})

