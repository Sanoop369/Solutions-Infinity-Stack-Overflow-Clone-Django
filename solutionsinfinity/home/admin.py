from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Tags)
admin.site.register(Question)
admin.site.register(Solutions)


#comment these
admin.site.register(User_details)
admin.site.register(Solution_comments)
admin.site.register(Question_comments)
admin.site.register(Notification)

