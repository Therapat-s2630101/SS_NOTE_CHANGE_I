from django.urls import path,include
from . import views

#<a href="/lecture/{{note.note.title}}/{{ note.note.id }}"> hard to change
#<a href="{%url 'S&S:lecture' note.note.title note.note.id %}"

#GET /input=652&input=ssss
#POST / 
app_name='S&S'
urlpatterns = [
    path('', views.home, name='home'), # new
    path('accounts/', include('django.contrib.auth.urls')), 
    path('signup/', views.signup, name='signup'),
    path('change-password/', views.change_password, name='change_password'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('upload/',views.upload,name='upload'),
    path('lecture/<str:lecture_title>/<int:lecture_id>/', views.lecture, name='lecture'),
    path('profile/<str:username>/', views.profile, name='profile'),
]