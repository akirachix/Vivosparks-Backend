from django.urls import path
from .views import VirtualMoneyView, VirtualMoneyDetailView

urlpatterns = [
     path('virtualmoney/', VirtualMoneyView.as_view(), name='virtualmoney-list'),
     path('virtualmoney/<int:id>/', VirtualMoneyDetailView.as_view(), name='virtualmoney-detail'),
   

]