from django.contrib import admin
from .models import Lecture,Profile,Lecture_image,Rate

# Register your models here.
admin.site.register(Lecture)
admin.site.register(Profile)
admin.site.register(Lecture_image)
admin.site.register(Rate)