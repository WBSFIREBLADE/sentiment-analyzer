from django.urls import path
from . import views as v


urlpatterns = [
    path("",v.register ,  name='home'),
    path('logout', v.logout,name='l_a'),
    path('login',v.login_user, name='login'),
    path('sentiment',v.analyze_sentiment, name='analyze')
]
