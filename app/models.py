from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#class users(models.Model):
 #   owner = models.OneToOneField(User, related_name='user')
  #  firstname=models.CharField(max_length=50)
   # lastname=models.CharField(max_length=50)

#    def __str__(self):
 #        return self.owner.username

class Onetimelinks(models.Model):
    code=models.CharField(max_length=100,null=False,blank=False)
    token=models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.token

class UploadEmails(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.CharField(max_length=200)

    def __str__(self):
        return self.email

class UploadPhoneNo(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneno = models.IntegerField()

    def __str__(self):
        return (str)(self.phoneno)

class Requests(models.Model):
    requested_by_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_created')
    By_name=models.CharField(max_length=150,null=False,default='user')
    requested_to_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_received')
    to_name=models.CharField(max_length=150,null=False,default='user')

class Posts(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,default='name')
    title=models.TextField(max_length=150,primary_key=True)
    post=models.TextField()
    date=models.DateTimeField(default='')

    def __str__(self):
        return self.title

    def get_post_comments(self):
        posts=Posts.objects.all()
        return Shares.objects.all().filter(post__id=self.id)
    def get_likes(self):
        return Likes.objects.all().filter(liked_post__id=self.id)

class Likes(models.Model):
    liked_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='liked_by')
    liked_by_name=models.CharField(max_length=150,null=False,default='user')
    liked_post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='liked_post')

    class Meta:
        unique_together = ["liked_by","liked_by_name","liked_post"]

    def __str__(self):
        return self.liked_by_name+' liked '+str(self.liked_post)
    def get_details(self):
        return Posts.objects.all().filter(title=self.liked_post)

class Shares(models.Model):
    shared_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='shared_by')
    shared_by_name=models.CharField(max_length=150,null=False,default='user')
    shared_post=models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='shared_post')

    class Meta:
        unique_together = ["shared_by", "shared_by_name", "shared_post"]

    def __str__(self):
        return self.shared_by_name+' shared '+str(self.shared_post)
    def get_details(self):
        return Posts.objects.all().filter(title=self.shared_post)