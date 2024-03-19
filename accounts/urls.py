'''
    @author SABINA 
    @created 17/03/2024 5:30 PM
    @project Backend(MomentGram)
'''
from django.urls import path, include
from .views import *

urlpatterns = [
    path('user-register/', UserRegistrationView.as_view(), name='user-register'),
 ]