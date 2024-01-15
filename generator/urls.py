from . import views
from django.urls import path
urlpatterns = [
    path('generate',views.PasswordGeneratorAPIView.as_view(),name='generate'),
     path('signup', views.UserRegistrationView.as_view(), name='signup'),
    path('login', views.UserLoginView.as_view(), name='login'),
]
