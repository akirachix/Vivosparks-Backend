from django.urls import path
from .views import user_login, logout, callback, change_password, loginSSO, index

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', logout, name='logout'),
    path('callback/', callback, name='callback'),
    path('change-password/', change_password, name='change_password'),
    path('sso-login/', loginSSO, name='login_sso'),
    path('', index, name='index'),
]
