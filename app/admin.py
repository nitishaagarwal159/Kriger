from django.contrib import admin
from .models import Onetimelinks,UploadEmails,UploadPhoneNo,Requests,Posts,Likes,Shares
#admin.site.register(users)
admin.site.register(Onetimelinks)
admin.site.register(UploadEmails)
admin.site.register(UploadPhoneNo)
admin.site.register(Requests)
admin.site.register(Posts)
admin.site.register(Likes)
admin.site.register(Shares)

# Register your models here.
